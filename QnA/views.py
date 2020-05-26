from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404
from QnA import models


def paginate(object_list, request, per_page=5):
    p = Paginator(object_list, per_page)
    return p


def index(request):
    questions = models.Question.objects.new()
    p = paginate(questions, request, 5)
    page_num = request.GET.get('page')
    if page_num is None:
        page_num = 1
    page_obj = p.get_page(page_num)

    # like_dislike = models.LikeDislike.objects.all()

    return render(request, 'main_page.html', {
        'registered_user': 'Ivan',
        'questions': page_obj,
        'page': p.page(page_num),
    })


def ask(request):
    return render(request, 'ask_page.html', {
        'registered_user': 'Ivan',
        'text_fields': ['Title', 'Tags', ],
        'text_areas': ['Question', ],
    })


def question(request, qid):
    question_ = get_object_or_404(models.Question, pk=qid)

    return render(request, 'question_page.html', {
        'registered_user': 'Ivan',
        'question': question_,
    })


def login(request):
    return render(request, 'login_page.html', {})


def signup(request):
    return render(request, 'signup_page.html', {
        'text_fields': ['Login', 'Email', 'Nickname', ],
        'password_fields': ['Password', 'Repeat password', ],
        'text_areas': ['Question', ],
    })


def questions_tags(request, tid):
    tag = get_object_or_404(models.Tag, pk=tid)
    questions = tag.Questions.all()
    p = paginate(questions, request, 5)
    page_num = request.GET.get('page')
    if page_num is None:
        page_num = 1
    page_obj = p.get_page(page_num)
    return render(request, 'question_tag_page.html', {
        'registered_user': 'Ivan',
        'tag': tag,
        'page': p.page(page_num)
    })


def setting(request):
    return render(request, 'setting_page.html', {
        'registered_user': 'Ivan',
        'text_fields': ['Login', 'Email', 'Nickname'],
    })


def hot_question(request):
    hot_questions = models.Question.objects.popular()
    p = paginate(hot_questions, request, 5)
    page_num = request.GET.get('page')
    if page_num is None:
        page_num = 1
    page_obj = p.get_page(page_num)

    return render(request, 'hot_question_page.html', {
        'registered_user': 'Ivan',
        'questions': page_obj,
        'page': p.page(page_num),
    })