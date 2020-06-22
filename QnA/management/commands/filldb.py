from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from QnA.models import Question, Tag, Profile, Answer, LikeDislike
from random import choice, random
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--profiles', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--likes', type=int)

    def fill_profiles(self, cnt):

        for i in range(cnt):
            random_tail = f.random_int(min=1, max=100000)
            username = f.name() + str(random_tail)
            username = str.replace(username, ' ', '').lower()
            u = User(username=username)
            u.save()
            Profile.objects.create(
                user=u, nickname=f.name(),
            )

    def fill_tags(self, cnt):
        for i in range(cnt):
            try:
                Tag.objects.create(
                    tag_name=f.word(),
                )
            except:
                pass

    def fill_answers(self, cnt):
        profile_ids = Profile.objects.get_queryset().count()
        first_id = list(Profile.objects.get_queryset()[:1].values())
        first_id = first_id[0]['id']
        for i in range(cnt):
            a = Answer.objects.create(
                description=' '.join(f.sentences(f.random_int(min=2, max=5))),
            )
            profile_count = f.random_int(min=first_id, max=first_id+profile_ids-1)
            Profile.objects.get(pk=profile_count).answer_author.add(a)

    def fill_questions(self, cnt):
        profile_ids = Profile.objects.get_queryset().count()
        first_id = list(Profile.objects.get_queryset()[:1].values())
        first_id = first_id[0]['id']
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        answer_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            q = Question.objects.create(
                description=' '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:64],
            )
            tags_count = f.random_int(min=1, max=10)
            for j in range(tags_count):
                q.tags.add(Tag.objects.get(pk=choice(tag_ids)))

            answer_count = f.random_int(min=1, max=25)
            for j in range(answer_count):
                q.question_answer.add(Answer.objects.get(pk=choice(answer_ids)))

            profile_count = f.random_int(min=first_id, max=first_id+profile_ids-1)
            Profile.objects.get(pk=profile_count).question_author.add(q)

    def fill_likes(self, cnt):
        profile_ids = Profile.objects.get_queryset().count()
        first_id = list(Profile.objects.get_queryset()[:1].values())
        first_id = first_id[0]['id']
        answer_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            votes = [-1, 1]
            vote = choice(votes)
            profile_count = f.random_int(min=first_id, max=first_id+profile_ids-1)
            l = LikeDislike.objects.create(user=Profile.objects.get(pk=profile_count),
                                           content_object=Question.objects.get(pk=choice(question_ids)), vote=vote)
            l.save()
            vote = choice(votes)
            profile_count = f.random_int(min=first_id, max=first_id+profile_ids-1)
            l = LikeDislike.objects.create(user=Profile.objects.get(pk=profile_count),
                                           content_object=Answer.objects.get(pk=choice(answer_ids)), vote=vote)
            l.save()

    def handle(self, *args, **options):
        # self.fill_profiles(options.get('profiles', 10))
        # self.fill_answers(options.get('answers', 10))
        # self.fill_tags(options.get('tags', 10))
        # self.fill_questions(options.get('questions', 10))
        self.fill_likes(options.get('likes', 140))
