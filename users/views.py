from django.shortcuts import render, redirect
from .forms import CustomUserCreationFrom
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('polls:poll-list')

        messages.error(request, 'Unsuccessful registration. Invalid information.')

    form = CustomUserCreationFrom()
    return render(request, 'users/register.html', {'form':form})        

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, f"You are logged in {username}.")
                return redirect("polls:poll-list")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
            
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'users/login.html', context)                    

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out")    
    return redirect('polls:index')