from django.shortcuts import render, get_object_or_404
from .models import Flashcard, FlashcardSet
from .forms import FlashcardSetForm, FlashcardForm
from django.shortcuts import redirect
# Create your views here.

def main_page(request):
    return render(request, 'website/index.html')

def flashcards(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'website/flashcards.html', {'sets':sets})

def flashcardset_detail(request, slug):
    flashcard_set = get_object_or_404(FlashcardSet, slug=slug)
    return render(request, 'website/flashcardset_detail.html', {
        'set': flashcard_set,
        'flashcards': flashcard_set.flashcards.all()
    })

# def sessions(request):
#     return render(request, 'website/sessions.html')

from django.shortcuts import render, redirect
from .models import Goal
from .forms import GoalForm

def sessions(request):
    form = GoalForm()

    # Handle form submission to add a new goal
    if request.method == 'POST' and 'add_goal' in request.POST:
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website:sessions')

    # Handle the toggling of goal completion status
    if request.method == 'POST' and 'toggle_goal' in request.POST:
        selected_goal_id = request.POST.get('selected_goal_id')
        if selected_goal_id:
            goal = Goal.objects.get(id=selected_goal_id)
            goal.is_completed = not goal.is_completed  # Toggle completion status
            goal.save()
        return redirect('website:sessions')

    # Get the selected goal ID from the dropdown to keep selection state
    selected_goal_id = request.POST.get('selected_goal_id')

    # Include all goals, sort incomplete first, then by created_at
    all_goals = Goal.objects.all().order_by('is_completed', 'created_at')

    return render(request, 'website/sessions.html', {
        'goals': all_goals,
        'form': form,
        'selected_goal_id': selected_goal_id,
    })


def create_flashcard_set(request):
    if request.method == 'POST':
        form = FlashcardSetForm(request.POST)
        if form.is_valid():
            flashcard_set = form.save(commit=False)
            flashcard_set.save()
            return redirect('website:flashcards')
    else:
        form = FlashcardSetForm()

    return render(request, 'website/create_flashcard_set.html', {'form': form})

def add_flashcard(request, slug):
    flashcard_set = get_object_or_404(FlashcardSet, slug=slug)

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.flashcard_set = flashcard_set
            flashcard.save()
            return redirect('website:flashcardset_detail', slug=slug)
    else:
        form = FlashcardForm()

    return render(request, 'website/add_flashcard.html', {
        'form': form,
        'set': flashcard_set
    })
    
    
from django.shortcuts import render, get_object_or_404
from .models import FlashcardSet

def flashcardset_detail(request, slug):
    flashcard_set = get_object_or_404(FlashcardSet, slug=slug)
    flashcards = flashcard_set.flashcards.values('question', 'answer')
    
    return render(request, 'website/flashcardset_detail.html', {
        'set': flashcard_set,
        'flashcards': list(flashcards),
    })

import openai
from django.conf import settings
from .forms import FlashcardPromptForm

openai.api_key = settings.OPENAI_API_KEY

def generate_flashcards(request, slug):
    flashcard_set = FlashcardSet.objects.get(slug=slug)
    form = FlashcardPromptForm()

    if request.method == "POST":
        form = FlashcardPromptForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data["topic"]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Create 5 flashcards (question and answer) based on this topic:\n\n{topic}",
                    }
                ]
            )

            output = response.choices[0].message["content"]
            # Example parsing (simple Q: A: format)
            for block in output.split("\n\n"):
                if "Q:" in block and "A:" in block:
                    q = block.split("Q:")[1].split("A:")[0].strip()
                    a = block.split("A:")[1].strip()
                    Flashcard.objects.create(set=flashcard_set, question=q, answer=a)

            return redirect('website:flashcardset_detail', slug=slug)

    return render(request, 'website/generate_flashcards.html', {
        "form": form,
        "set": flashcard_set
    })

    
def calendar(request):
    return render(request, 'website/calendar.html')


from django.http import JsonResponse
from .models import Goal
from django.utils.timezone import now, timedelta

def calendar_events(request):
    events = []

    # Example: using goal creation date (you can also create a separate model for calendar events)
    for goal in Goal.objects.all():
        events.append({
            "title": goal.title,
            "start": goal.created_at.strftime("%Y-%m-%d"),
            "color": "#f39c12" if not goal.is_completed else "#27ae60",  # Orange for open, green for complete
        })

    return JsonResponse(events, safe=False)


