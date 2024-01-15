from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SimpleRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )




class UploadCSVForm(forms.Form):
    file = forms.FileField()
