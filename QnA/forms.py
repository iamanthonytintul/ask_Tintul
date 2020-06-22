from django import forms
import re

from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist

from Homework import settings
from QnA import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is None or password is None or len(username) > 20 or len(password) < 8:
            raise forms.ValidationError("Login or password is incorrect")

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if ' ' in username:
    #         raise forms.ValidationError('Username contains whitespaces')
    #     if len(username) > 20:
    #         raise forms.ValidationError('Too long username')
    #     else:
    #         return username
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if ' ' in password:
    #         raise forms.ValidationError('Password contains whitespaces')
    #     if len(password) < 8:
    #         raise forms.ValidationError('Too short password')
    #     else:
    #         return password


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=50)

    class Meta:
        model = models.Question
        fields = ['title', 'description']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags is not None:
            tags = tags.split(',')
        for t in tags:
            t = t.strip()
            if re.fullmatch(r'([\w]-?)+', t) is None:
                raise forms.ValidationError('Error, please check input data')
        return tags

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self):
        tags = self.cleaned_data.get('tags')

        q = models.Question.objects.create(author=self.author, title=self.cleaned_data.get('title'),
                                           description=self.cleaned_data.get('description'))
        for t in tags:
            tag = models.Tag.objects.get_or_create(tag_name=t)[0]
            q.tags.add(tag)
            tag.save()

        return q


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['answer_text']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, qid):
        a = models.Answer.objects.create(author=self.author, answer_text=self.cleaned_data.get('answer_text'),
                                         question=models.Question.objects.get(pk=qid))
        return a


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    avatar = forms.ImageField(required=False)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password should contains at least 8 characters")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']
        if password is not None and confirm_password != password:
            raise forms.ValidationError("Repeated password doesn't match")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            models.User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('This username already exists')

    def save(self):
        u = models.User(email=self.cleaned_data['email'], username=self.cleaned_data['username'])
        u.set_password(self.cleaned_data['password'])
        u.save()
        p = models.Profile.objects.create(user=u, nickname=self.cleaned_data['nickname'])
        avatar = self.cleaned_data.get('avatar')
        if avatar is not None:
            filename = FileSystemStorage().save(avatar.name, avatar)
            avatar_url = FileSystemStorage().url(filename)
            p.avatar = avatar_url
        u.save()
        p.save()
        return p

class EditForm(forms.Form):
    email = forms.EmailField(required=False)
    nickname = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    def save(self, user):
        email = self.cleaned_data.get('email')
        nickname = self.cleaned_data.get('nickname')
        avatar = self.cleaned_data.get('avatar')
        if email is not None and email != '':
            user.email = email
        if nickname is not None and nickname != '':
            user.profile.nickname = nickname
        if avatar is not None:
            filename = FileSystemStorage().save(avatar.name, avatar)
            avatar_url = FileSystemStorage().url(filename)
            user.profile.avatar = avatar_url
        user.profile.save()
        user.save()
        return user.profile
