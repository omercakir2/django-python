from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Member

class MemberRegistrationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class MemberLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
