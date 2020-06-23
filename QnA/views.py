from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib import auth
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from QnA import models
from QnA.forms import LoginForm, QuestionForm, AnswerForm, RegistrationForm, EditForm


def paginate(object_list, request, per_page=5):
    page_num = request.GET.get('page') or 1
    paginator = Paginator(object_list, per_page)
    return paginator, page_num


def index(request):
    popular_tags = models.Tag.objects.popular()
    paginator, page_num = paginate(models.Question.objects.new(), request, 5)
    return render(request, 'main_page.html', {
        'user': request.user,
        'questions': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })


def question(request, qid):
    popular_tags = models.Tag.objects.popular()
    single_question = get_object_or_404(models.Question, pk=qid)
    if request.user.is_authenticated:
        form = AnswerForm(request.user.profile)
        return render(request, 'question_page.html', {
            'question': single_question,
            'popular_tags': popular_tags,
            'form': form,
        })
    return render(request, 'question_page.html', {
        'question': single_question,
        'popular_tags': popular_tags,
    })


def login(request):
    popular_tags = models.Tag.objects.popular()
    redirect_reference = request.GET.get('continue')

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login_page.html', {
            'popular_tags': popular_tags,
            'form': form,
            'redirect_reference': redirect_reference
        })

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = auth.authenticate(request, **form.cleaned_data)
        if user is not None:
            auth.login(request, user)
            return redirect(redirect_reference)
        else:
            form.add_error(None, 'Login or password is incorrect')
    return render(request, 'login_page.html', {
        'popular_tags': popular_tags,
        'form': form,
        'redirect_reference': redirect_reference
    })


def signup(request):
    popular_tags = models.Tag.objects.popular()
    redirect_reference = request.GET.get('continue')
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'signup_page.html', {
            'popular_tags': popular_tags,
            'form': form,
            'redirect_reference': redirect_reference,
        })

    form = RegistrationForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        user = auth.authenticate(request, **form.cleaned_data)
        if user is not None:
            auth.login(request, user)
            return redirect(redirect_reference)
        else:
            form.add_error(None, 'Login or password is incorrect')
        return redirect(redirect_reference)

    return render(request, 'signup_page.html', {
        'popular_tags': popular_tags,
        'form': form,
        'redirect_reference': redirect_reference,
    })


def questions_tags(request, tid):
    popular_tags = models.Tag.objects.popular
    tag = get_object_or_404(models.Tag, pk=tid)
    paginator, page_num = paginate(tag.all_questions(), request, 5)
    return render(request, 'question_tag_page.html', {
        'user': request.user,
        'tag': tag,
        'question': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })


def hot_question(request):
    popular_tags = models.Tag.objects.popular()
    paginator, page_num = paginate(models.Question.objects.popular(), request, 5)
    return render(request, 'hot_question_page.html', {
        'user': request.user,
        'questions': paginator.get_page(page_num),
        'page': paginator.page(page_num),
        'popular_tags': popular_tags,
    })


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('continue'))


@login_required(redirect_field_name="continue")
def ask(request):
    popular_tags = models.Tag.objects.popular()
    if request.method == 'GET':
        form = QuestionForm(request.user.profile)
        return render(request, 'ask_page.html', {
            'form': form,
            'popular_tags': popular_tags,
        })

    form = QuestionForm(request.user.profile, data=request.POST)
    if form.is_valid():
        single_question = form.save()
        return redirect(reverse('question', kwargs={'qid': single_question.pk}))
    return render(request, 'ask_page.html', {
        'user': request.user,
        'form': form,
        'popular_tags': popular_tags,
    })


@login_required(redirect_field_name="continue")
def answer(request, qid):
    form = AnswerForm(request.user.profile, data=request.POST)
    if form.is_valid():
        a = form.save(qid)
        return redirect(reverse('question', kwargs={'qid': qid}) + '#answer-' + str(a.pk))


@login_required()
def profile_edit(request):
    popular_tags = models.Tag.objects.popular()
    if request.method == "GET":
        form = EditForm()
        return render(request, 'setting_page.html', {
            'popular_tags': popular_tags,
            'form': form,
        })
    form = EditForm(request.POST, request.FILES)

    if form.is_valid():
        form.save(request.user)
        return redirect(reverse('index'))
    else:
        form.add_error(None, 'Check input data')

    return render(request, 'setting_page.html', {
        'popular_tags': popular_tags,
        'form': form,
    })


@login_required
def correct_answer(request, aid):
    user = request.user.profile
    answer = models.Answer.objects.get(pk=aid)
    if answer.question.author == user:
        answer.is_correct = True
        answer.save()
        return JsonResponse({'is_correct': 'True'})
    return HttpResponse.status_code(403)


@login_required
def like_dislike(request, vid, content_type, oid):
    vid = vid-1 if vid == 0 else vid
    if content_type == 'answer':
        obj = models.Answer.objects.get(pk=oid)
    elif content_type == 'question':
        obj = models.Question.objects.get(pk=oid)
    else:
        return HttpResponse.status_code(400)

    try:
        vote_obj = models.LikeDislike.objects.get(content_type=models.ContentType.objects.get_for_model(obj), object_id=obj.pk, user=request.user.profile)
        if vid != vote_obj.vote:
            vote_obj.vote = vid
            vote_obj.save()
    except models.LikeDislike.DoesNotExist:
        obj.votes.create(user=request.user.profile, vote=vid)

    return JsonResponse({'Like': obj.likes(),
                         'Dislike': obj.dislikes(),
                         'Rating': obj.sum_rating()})
