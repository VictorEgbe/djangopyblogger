from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Enter a valid and unique email adress. Email is required')
    first_name = forms.CharField(
        max_length=100, help_text='This field is required')
    last_name = forms.CharField(
        max_length=100, help_text='This field is required')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                'A user with that email already exist.')
        return email


class UserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive"),
                code="inactive",
                )
        return None






# class UserLoginFormTesting(forms.Form):
#     username = forms.CharField(max_length=100,)
    # password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
    #     'type': 'password'}),
    #     help_text='Verify that you are using the correct letter casing'
    # )

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not User.objects.filter(username=username).exists():
    #         raise forms.ValidationError(
    #             'No user matched the username provided')
    #     return username

    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if not user:
    #         raise forms.ValidationError(
    #             'Wrong password! Please verify your password.')
    #     return password