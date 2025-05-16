from django.urls import path
from . import views
from .views import profile_view

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('ask/', views.ask_question, name='ask_question'),
    path('questions/', views.questions_list, name='questions_list'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('questions/award_points/<int:answer_id>/', views.award_points, name='award_points'),
    path('questions/close_question/<int:question_id>/', views.close_question, name='close_question'),
    path('questions/open_question/<int:question_id>/', views.open_question, name='open_question'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]



