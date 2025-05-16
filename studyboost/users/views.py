from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("website:main_page")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("website:main_page")
    else:
        form = AuthenticationForm()
    
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("website:main_page")
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    profile = request.user.userprofile  # Get the related UserProfile
    points = profile.points  # Access custom field
    user_questions = Question.objects.filter(owner=request.user)
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'points': points,
        'user_questions': user_questions
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib import messages

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.owner = request.user
            question.save()
            return redirect('users:question_detail', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'users/ask_question.html', {'form': form})


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)
    is_owner = question.owner == request.user
    form = AnswerForm()

    if request.method == "POST" and not question.is_closed:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user.userprofile
            answer.save()

    return render(request, 'users/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'is_owner': is_owner
    })
    
    
@login_required
def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.is_closed:
        messages.error(request, "This question has been closed.")
        return redirect('users:question_detail', question_id=question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
    return redirect('users:question_detail', question_id=question.id)


@login_required
def award_points(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question

    if question.owner == request.user and not answer.is_awarded:
        answer.is_accepted = True
        answer.is_awarded = True
        answer.save()

        # Award points to the answer's author
        answer.author.points += question.points
        answer.author.save()

    return redirect('users:question_detail', question_id=question.id)

@login_required
def close_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if question.owner == request.user:
        question.is_closed = True
        question.save()

    return redirect('users:question_detail', question_id=question.id)

@login_required
def open_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if question.owner == request.user:
        question.is_closed = False
        question.save()

    return redirect('users:question_detail', question_id=question.id)

def questions_list(request):
    questions = Question.objects.filter(is_closed=False).order_by('-created_at')
    return render(request, 'users/questions_list.html', {'questions': questions})


from django.shortcuts import render
from .models import UserProfile

def leaderboard(request):
    # Get all UserProfiles sorted by points in descending order
    users = UserProfile.objects.all().order_by('-points')

    return render(request, 'users/leaderboard.html', {'users': users})
