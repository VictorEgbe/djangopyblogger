from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .forms import UserLoginForm, UserRegistrationForm
from .tokens import account_activation_token


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in.')
        return HttpResponseRedirect('/')
    form = UserLoginForm(request)

    if request.method == 'POST':
        next_page = request.POST.get('next')
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
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
        messages.info(
            request, f'You can not register when you are already logged in. Log out first.')
        return redirect('logout')
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/activation.html', {
                'user': user,
                'token': account_activation_token.make_token(user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'domain': current_site.domain
            })
            to_email = [form.cleaned_data.get('email')]
            mail_subject = 'Activate your PyBlogger account'
            email = EmailMessage(mail_subject, message, to=to_email)
            email.send()
            return render(request, 'accounts/activation_info.html')
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def activation(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=user_id)
        token = account_activation_token.check_token(user, token)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None and token:
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, f"Welcome {user.username}, your account activated successfully. You are now logged in.")
        return HttpResponseRedirect('/')
    else:
        return render(request, 'accounts/invalid_link.html', {'title': 'Invalid link'})


@login_required
def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            password = form.cleaned_data.get('new_password2')
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f'Your password was changed successfully!')
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, f'Something went wrong!')
                return redirect('login')
    context = {'title': 'Change password', 'form': form}
    return render(request, 'accounts/password_change.html', context)


class UserResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    extra_context = {'title': 'Password Reset'}


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    extra_context = {'title': 'Password Reset Confirm'}
    # success_url = '/accounts/login/' # This also works.


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    extra_context = {'title': 'Password Reset Done'}


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    extra_context = {'title': 'Password Reset Completed'}
