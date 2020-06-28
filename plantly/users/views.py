from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # user has submitted form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('journal-home') #name we gave route in url patterns
    else: # user JUST navigated to this page, show them a blank form
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
