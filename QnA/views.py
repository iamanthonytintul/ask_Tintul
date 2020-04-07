from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

questions = {
    i: {'id': i, 'title': f'Question #{i}'}
    for i in range(1, 5)
}
questions_tags = {
    i: {'tag_id': i, 'title': 'bender'}
    for i in range(1, 5)
}

def index(request):
    return render(request, 'index.html', {
        'registred_user': 'Ivan',
        'questions': questions.values(),
    })


def ask(request):
    return render(request, 'ask.html', {
        'registred_user': 'Ivan',
        'text_fields': ['Title', 'Tags', ],
        'text_areas': ['Question', ],
    })


def question(request, qid):
    question = questions.get(qid)
    return render(request, 'question.html', {
        'registred_user': 'Ivan',
        'question': question,
        'answers': range(5)
    })

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {
        'text_fields': ['Login', 'Email', 'Nickname', ],
        'password_fields': ['Password', 'Repeat password', ],
        'text_areas': ['Question', ],
    })

def questions_tags(request, tag_id):
    question_tags = questions_tags.get(tag_id)
    return render(request, 'question_tag.html', {
        'registred_user': 'Ivan',
        'questions-by-tag': question_tags,
    })

def setting(request):
    return render(request, 'setting.html', {
        'registred_user': 'Ivan',
        'text_fields': ['Login', 'Email', 'Nickname'],
        })

