from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404
from QnA import models


def paginate(object_list, request, per_page=5):
    page_num = request.GET.get('page') or 1
    paginator = Paginator(object_list, per_page)
    return paginator, page_num


def side_bar_info():
    tags = models.Tag.objects.popular()
    return tags


def index(request):
    popular_tags = side_bar_info()
    questions = models.Question.objects.new()
    paginator, page_num = paginate(questions, request, 5)
    return render(request, 'main_page.html', {
        'registered_user': 'Ivan',
        'questions': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })


def ask(request):
    popular_tags = side_bar_info()
    return render(request, 'ask_page.html', {
        'registered_user': 'Ivan',
        'text_fields': ['Title', 'Tags', ],
        'text_areas': ['Question', ],
        'popular_tags': popular_tags,
    })


def question(request, qid):
    popular_tags = side_bar_info()
    question_ = get_object_or_404(models.Question, pk=qid)
    return render(request, 'question_page.html', {
        'registered_user': 'Ivan',
        'question': question_,
        'popular_tags': popular_tags,
    })


def login(request):
    popular_tags = side_bar_info()
    return render(request, 'login_page.html', {
        'popular_tags': popular_tags,
    })


def signup(request):
    popular_tags = side_bar_info()
    return render(request, 'signup_page.html', {
        'text_fields': ['Login', 'Email', 'Nickname', ],
        'password_fields': ['Password', 'Repeat password', ],
        'text_areas': ['Question', ],
        'popular_tags': popular_tags,
    })


def questions_tags(request, tid):
    popular_tags = side_bar_info()
    tag = get_object_or_404(models.Tag, pk=tid)
    question = tag.all_questions()
    paginator, page_num = paginate(question, request, 5)
    return render(request, 'question_tag_page.html', {
        'registered_user': 'Ivan',
        'tag': tag,
        'question': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })


def setting(request):
    popular_tags = side_bar_info()
    return render(request, 'setting_page.html', {
        'registered_user': 'Ivan',
        'text_fields': ['Login', 'Email', 'Nickname'],
        'popular_tags': popular_tags,
    })


def hot_question(request):
    popular_tags = side_bar_info()
    hot_questions = models.Question.objects.popular()
    paginator, page_num = paginate(hot_questions, request, 5)
    return render(request, 'hot_question_page.html', {
        'registered_user': 'Ivan',
        'questions': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })