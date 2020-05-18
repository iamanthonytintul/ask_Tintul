from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger

# Create your views here.

questions = [
    {'id': i, 'title': f'Question #{i}'}
    for i in range(1, 36)
]
questions_tags = {
    i: {'tag_id': i, 'title': 'bender'}
    for i in range(1, 5)
}

def paginate(object_list, request, per_page=10):
    p = Paginator(object_list, per_page)
    return p

def index(request):
    p = paginate(questions, request, 5)
    page_num = request.GET.get('page')

    if page_num == None:
        page_num = 1

    page_obj = p.get_page(page_num)

    # try:
    #     questions = p.page(page)
    # except PageNotAnInteger:
    #     questions = p.page(1)
    return render(request, 'main_page.html', {
        'registred_user': 'Ivan',
        'questions': page_obj,
        'page': p.page(page_num),
    })


def ask(request):
    return render(request, 'ask_page.html', {
        'registred_user': 'Ivan',
        'text_fields': ['Title', 'Tags', ],
        'text_areas': ['Question', ],
    })


def question(request, qid):
    question = questions[qid]
    return render(request, 'question_page.html', {
        'registred_user': 'Ivan',
        'question': question,
        'answers': range(5)
    })

def login(request):
    return render(request, 'login_page.html', {})

def signup(request):
    return render(request, 'signup_page.html', {
        'text_fields': ['Login', 'Email', 'Nickname', ],
        'password_fields': ['Password', 'Repeat password', ],
        'text_areas': ['Question', ],
    })

def questions_tags(request, tag_id):
    question_tags = questions_tags.get(tag_id)
    return render(request, 'question_tag_page.html', {
        'registred_user': 'Ivan',
        'questions-by-tag': question_tags,
    })

def setting(request):
    return render(request, 'setting_page.html', {
        'registred_user': 'Ivan',
        'text_fields': ['Login', 'Email', 'Nickname'],
        })
