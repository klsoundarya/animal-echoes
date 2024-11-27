# quiz/views.py
from django.shortcuts import render, get_object_or_404, render
from .models import Quiz, Question, UserAnswer
from django.http import HttpResponseRedirect
from django.urls import reverse

# View to list quizzes
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# View to display questions
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        # Get user answer and save it
        question_id = request.POST['question_id']
        selected_answer = request.POST['selected_answer']
        question = get_object_or_404(Question, pk=question_id)
        is_correct = selected_answer == question.correct_answer
        
        # Save the answer
        UserAnswer.objects.create(user=request.user, question=question, selected_answer=selected_answer, is_correct=is_correct)
        
        # Redirect to next question or result
        next_question = questions.filter(id__gt=question.id).first()
        if next_question:
            return HttpResponseRedirect(reverse('quiz_detail', args=[quiz.id]))
        else:
            return HttpResponseRedirect(reverse('quiz_result', args=[quiz.id]))
    
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

# View to show results
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__quiz=quiz)
    score = user_answers.filter(is_correct=True).count()
    total = user_answers.count()
    
    return render(request, 'quiz/quiz_result.html', {'score': score, 'total': total, 'quiz': quiz})
