from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in.')
        return HttpResponseRedirect('/')
    form = UserLoginForm()

    if request.method == 'POST':
        next_page = request.POST.get('next')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome back {username}')
            return HttpResponseRedirect(next_page) if next_page else HttpResponseRedirect('/')

    context = {
        'form': form,
        'title': 'Log In'
    }
    return render(request, 'accounts/login_user.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, f'You have been logged out successfully!')
        return redirect('login')

    context = {
        'title': 'Log out'
    }
    return render(request, 'accounts/logout.html', context)


def registration(request):
    if request.user.is_authenticated:
        messages.info(request, f'You can not register when you are already logged in. Log out first.')
        return redirect('logout')
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {username}.Your account was successfully created!')
            return HttpResponseRedirect('/')
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'accounts/register.html', context)
