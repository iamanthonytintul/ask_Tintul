from django.db import models
from django.contrib.auth.models import  User
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from django.db.models import Sum


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
        return self.annotate(num_of_questions=Count('question_tag')).order_by('-num_of_questions')[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='upload/')
    nickname = models.CharField(max_length=50, null=True)


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    votes = ((DISLIKE, 'Don\'t like'), (LIKE, 'Like'))

    vote = models.SmallIntegerField(verbose_name='Vote', choices=votes)
    user = models.ForeignKey(Profile, verbose_name="Profile", on_delete=models.CASCADE, related_name='users_like')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()



class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=255)
    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tid': self.tag_name})

    def all_questions(self):
        return self.question_tag.all()


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='question_author')

    title = models.CharField(max_length=30)

    description = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='questions_rating')

    tags = models.ManyToManyField(Tag, related_name='question_tag')

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={"qid": self.id})

    def all_tags(self):
        return self.tags.all()

    def all_answers(self):
        return self.question_answer.all()

    def num_of_answers(self):
        return len(self.question_answer.all())

    def likes(self):
        return len(self.votes.filter(vote=1))

    def dislikes(self):
        return len(self.votes.filter(vote=-1))

    def sum_rating(self):
        like = len(self.votes.filter(vote=1))
        dislike = len(self.votes.filter(vote=-1))
        return like - dislike


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="answer_author")

    answer_text = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(LikeDislike, related_query_name='answers_rating')

    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='question_answer')

    is_correct = models.BooleanField(default=False)

    def likes(self):
        return len(self.votes.filter(vote=1))

    def dislikes(self):
        return len(self.votes.filter(vote=-1))

    def sum_rating(self):
        like = len(self.votes.filter(vote=1))
        dislike = len(self.votes.filter(vote=-1))
        return like-dislike
