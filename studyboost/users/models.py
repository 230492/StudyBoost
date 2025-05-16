# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    study_field = models.CharField(max_length=100, blank=True)
    study_place = models.CharField(max_length=100, blank=True)
    study_year = models.PositiveIntegerField(null=True, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"
 

    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField()
    points = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_awarded = models.BooleanField(default=False)
    points_awarded = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.author.user.username} to '{self.question.title}'"
