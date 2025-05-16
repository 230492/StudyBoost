# Register your models here.

from django.contrib import admin
from .models import UserProfile, Question, Answer

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)