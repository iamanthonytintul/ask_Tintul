from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from django.db.models import Sum
from datetime import datetime

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class AnswerManager(models.Manager):
    pass


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-creation_time')

    def popular(self):
        # self.annotate(num_likes=Count('question_likes'))
        return self.annotate(num_of_answers=Count('question_answer')).order_by('-num_of_answers')

    def all_tags(self):
        question_tags = {}
        for q in self.get_queryset():
            question = self.get(id=q.id)
            question_tags[q.id] = list(question.question_tag.all())
        return question_tags

    def tag(self, qid):
        question = self.get(id=qid)
        return list(question.question_tag.all())

    def num_of_answers(self):
        return Count('question_answer')

    def answers(self, qid):
        question = self.get(id=qid)
        return question.question_answer.all()


class TagManager(models.Manager):
    def question_by_tag(self, tid):
        tag = self.get(id=tid)
        return tag.Questions.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    nickname = models.CharField(max_length=50)


class LikeDislike(models.Model):
    like = 1
    dislike = -1

    votes = ((dislike, 'don\'t like it'), (like, 'like it'))

    vote = models.SmallIntegerField(verbose_name='Vote', choices=votes)
    user = models.ForeignKey(Profile, verbose_name="Profile", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='question_author')

    title = models.CharField(max_length=64)

    description = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='questions')

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={"qid": self.id})

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="answer_author")

    description = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='answers')

    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='question_answer')

    objects = AnswerManager()


class Tag(models.Model):
    tag_name = models.CharField(max_length=25)
    Questions = models.ManyToManyField(Question, related_name='question_tag')

    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tid': self.tag_name})

    def __unicode__(self):
        return self.tag_name
