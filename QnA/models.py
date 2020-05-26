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
        return self.annotate(num_of_answers=Count('question_answer')).order_by('-num_of_answers')

    def answers(self, qid):
        question = self.get(id=qid)
        return question.question_answer.all()


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(num_of_questions=Count('Questions')).order_by('-num_of_questions')[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    nickname = models.CharField(max_length=50)


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Don\'t like'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name='Vote', choices=VOTES)
    user = models.ForeignKey(Profile, verbose_name="Profile", on_delete=models.CASCADE, related_name='users_like')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='question_author')

    title = models.CharField(max_length=64)

    description = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='questions_rating')

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={"qid": self.id})

    def __unicode__(self):
        return self.title

    def all_tags(self):
        return list(self.question_tag.all())

    def all_answers(self):
        return list(self.question_answer.all())

    def num_of_answers(self):
        return len(list(self.question_answer.all()))

    def sum_rating(self):
        return self.votes.sum_rating()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="answer_author")

    description = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='answers_rating')

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

    def all_questions(self):
        return self.Questions.all()
