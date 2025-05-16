
from django import forms
from .models import FlashcardSet, Flashcard

class FlashcardSetForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ['title', 'description']

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2}),
            'answer': forms.Textarea(attrs={'rows': 2}),
        }


from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a goal...'
            })
        }
        
        
class FlashcardPromptForm(forms.Form):
    topic = forms.CharField(widget=forms.Textarea, label="Enter topic or text")