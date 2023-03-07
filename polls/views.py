from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question


def index_view(request):
    return render(request, 'polls/index.html')

@login_required(login_url="users:login")
def poll_list(request):
    questions = Question.objects.all()
    context = {'questions':questions}
    return render(request, 'polls/poll-list.html', context)        

@login_required(login_url="users:login")
def vote_view(request, pk):
    question = get_object_or_404(Question, id=pk)
    
    if request.method == 'POST':
        try:
            choice_id = request.POST['choice']
            seletcted_item = question.choices.get(id=choice_id)
        except:
            messages.error(request, "You didn't select a choice!")
            return render(request, 'polls/vote.html', {'question':question})  
        else:
            question.voter.add(request.user)
            seletcted_item.vote_count += 1
            seletcted_item.save()
            return HttpResponseRedirect(reverse('polls:result', kwargs={'pk':question.id}))

    context = {'question':question}
    return render(request, 'polls/vote.html', context)   

@login_required(login_url="users:login")
def result_view(request, pk):
    question = get_object_or_404(Question, id=pk)
    context = {'question':question}
    return render(request, 'polls/result.html', context)