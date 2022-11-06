from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question

def index_view(request):
    return render(request, 'polls/index.html')

def poll_list(request):
    questions = Question.objects.all()
    context = {'questions':questions}
    return render(request, 'polls/poll-list.html', context)        

def vote_view(requests, pk):
    question = get_object_or_404(Question, id=pk)
    
    if requests.method == 'POST':
        try:
            choice_id = requests.POST['choice']
            seletcted_item = question.choice_set.get(id=choice_id)
        except:
            return render(requests, 'polls/vote.html', {'question':question, 'error_message':"You didn't select a choice!"})  
        else:
            seletcted_item.vote_count += 1
            seletcted_item.save()
            return HttpResponseRedirect(reverse('polls:result', kwargs={'pk':question.id}))

    context = {'question':question}
    return render(requests, 'polls/vote.html', context)   

def result_view(requests, pk):
    question = get_object_or_404(Question, id=pk)
    context = {'question':question}
    return render(requests, 'polls/result.html', context)