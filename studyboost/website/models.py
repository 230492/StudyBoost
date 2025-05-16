from django.db import models
from django.utils.text import slugify

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError

class FlashcardSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while FlashcardSet.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        # Ensure the flashcard count doesn't exceed 50
        if self.pk and self.flashcards.count() > 50:
            raise ValidationError("A flashcard set can't contain more than 50 flashcards.")

    class Meta:
        verbose_name = "Flashcard Set"
        verbose_name_plural = "Flashcard Sets"


class Flashcard(models.Model):
    flashcard_set = models.ForeignKey(FlashcardSet, related_name='flashcards', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question[:50] + ('...' if len(self.question) > 50 else '')

    class Meta:
        verbose_name = "Flashcard"
        verbose_name_plural = "Flashcards"


class Goal(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title