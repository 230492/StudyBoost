from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('flashcards/create/', views.create_flashcard_set, name='create_flashcard_set'),
    path('flashcards/<slug:slug>/add/', views.add_flashcard, name='add_flashcard'),
    path('flashcards/', views.flashcards, name="flashcards"),
    path('flashcards/<slug:slug>/', views.flashcardset_detail, name='flashcardset_detail'),
    path('sessions/', views.sessions, name="sessions"),
    path('calendar/', views.calendar, name="calendar"),
    path('calendar-events/', views.calendar_events, name='calendar_events'),
    path('flashcards/<slug:slug>/generate/', views.generate_flashcards, name='generate_flashcards'),
]
