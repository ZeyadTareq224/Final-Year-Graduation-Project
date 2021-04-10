from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Answer, Question, UpVote, DownVote
from .forms import QuestionForm, AnswerForm
from django.contrib import messages


def list_questions(request):
    questions = Question.objects.all()
    
    context = {'questions': questions}
    return render(request, 'questions/index.html', context)


def create_question(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('questions')

    context = {'form': form}
    return render(request, 'questions/QuestionForm.html', context)


def question_details(request, pk):
    question = get_object_or_404(Question, id=pk)
    answers = Answer.objects.filter(question=question).order_by("-created_at")

    answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.instance.user = request.user
            answer_form.instance.question = question
            answer_form.save()
            messages.success(request, "Answer Added Successfuly.")
            return redirect("question-details", question.id)

    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
        
    }
    return render(request, 'questions/question_details.html', context)


def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user==question.user:
        form = QuestionForm(instance=question)
        if request.method=="POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                messages.success(request, "Question updated successfully.")
                return redirect('question-details', question_id)
    context = {
        'form': form
    }
    return render(request, 'questions/QuestionForm.html', context)


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    print("hahahahah")
    if request.user == question.user:
        if request.method == "POST":
            question.delete()
            messages.success(request, "Question deleted successfully.")
            return redirect('questions')
    context = {
            'question': question,
            'question_id': question_id
        }
    return render(request, 'questions/delete_question.html', context)


def upvote(request, answer_id, question_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user

    upvotes = UpVote.objects.filter(user=user, answer=answer)
    downvotes = DownVote.objects.filter(user=user, answer=answer)
    if (not downvotes):
        if request.method == "POST" and (not upvotes):
            upvote = UpVote(user=user, answer=answer)
            upvote.save()
            messages.success(request, "Answer Upvoted successfully.")
            return redirect("question-details", question_id)
        else:
            if request.method == "POST":
                user_vote = UpVote.objects.filter(user=user, answer=answer)
                user_vote.delete()
                messages.success(request, "Your Upvote deleted successfully.")
                return redirect("question-details", question_id)
    else:
        messages.info(request, "You downvoted this answer in order to upvote it, please delete your downvote first.")
        return redirect("question-details", question_id)            
    return redirect("question-details", question_id)
    


def downvote(request, answer_id, question_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    downvotes = DownVote.objects.filter(user=user, answer=answer)
    upvotes = UpVote.objects.filter(user=user, answer=answer)
    if (not upvotes):
        if request.method == "POST" and (not downvotes):
            downvote = DownVote(user=user, answer=answer)
            downvote.save()
            messages.success(request, "Answer Downvoted successfuly.")
            return redirect("question-details", question_id)
        else:
            if request.method == "POST":
                user_vote = DownVote.objects.filter(user=user, answer=answer)
                user_vote.delete()
                messages.success(request, "Your Downvote deleted successfully.")
                return redirect("question-details", question_id)
    else:
        messages.warning(request, "You upvoted this answer in order to downvote, it please delete your upvote first.")
        return redirect("question-details", question_id)           
    return redirect("question-details", question_id)


def update_answer(request, answer_id, question_id):
    
    answer = get_object_or_404(Answer, id=answer_id)
    form = AnswerForm(instance=answer)
    if request.method == "POST" and request.user == answer.user:
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your answer updated successfully.")
            return redirect("question-details", question_id)
    context = {
        'form': form,
        'question_id': question_id,
        }
    return render(request, 'questions/answer_form.html', context)

def delete_answer(request, answer_id, question_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.method == "POST" and request.user == answer.user:
        answer.delete()
        messages.success(request, "Your answer deleted successfully.")
        return redirect("question-details", question_id)
    context = {
        'question_id': question_id,
    }    
    return render(request, 'questions/delete_answer.html', context)


def search(request):
    if request.method == "GET":
        query = request.GET.get('search_query', None)
        if query:
            questions = Question.objects.filter(title__icontains=query)
            
            context = {'questions':questions}
            return render(request, 'questions/question_search.html', context)
        return render(request, 'questions/question_search.html')
