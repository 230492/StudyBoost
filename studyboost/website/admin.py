from django.contrib import admin
from .models import Flashcard, FlashcardSet, Goal

# Register your models here.

admin.site.register(FlashcardSet)
admin.site.register(Flashcard)
admin.site.register(Goal)