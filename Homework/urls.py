"""Homework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Homework import settings
from QnA import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:qid>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('tag/<slug:tid>/', views.questions_tags, name='tag'),
    path('hot_questions/', views.hot_question, name='hot'),
    path('logout/', views.logout_view, name='logout'),
    path('answer/<int:qid>/', views.answer, name='answer'),
    path('correct_answer/<int:aid>/', views.correct_answer, name='correct_answer'),
    path('vote/<int:vid>/<str:content_type>/<int:oid>/', views.like_dislike, name='votes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
