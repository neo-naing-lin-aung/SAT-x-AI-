"""URL Patterns for Core App."""

from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # About Page 
    path('about/', views.about, name='about'),
    # Study tools 
    path('tools/', views.study_tools, name='tools'),
    # Credit Page
    path('credit-source/', views.credit, name='credit'),
    # AI Assistant Page
    path('ai-assistant/', views.ai_assistant, name='ai_assistant'),
    # Profile Page
    path('profile/', views.profile, name='profile'),
    # Practice Page
    path('practice/', views.practice, name='practice'),
    # Practice Question Page
    path('practice/<int:practice_id>/<int:question_number>', views.question, name='question'),
    # Practice Result
    path('practice/<int:practice_id>/result/', views.practice_result, name="practice_result"),
    # Progress 
    path('progress/', views.progress, name='progress'),
    # Review
    path('practice/<int:practice_id>/review/<int:question_number>/', views.review, name='review'),
    # AI Chat
    path('ai-chat/', views.ai_chat, name='ai_chat'),
]