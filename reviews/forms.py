from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User


class RegisterForm(ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class LoginForm(ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']


class ReviewForm(forms.Form):
    RATING_CHOICES=( 
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )

    title = forms.CharField(max_length=64)
    summary = forms.CharField(widget=forms.Textarea)
    rating = forms.ChoiceField(choices=RATING_CHOICES)

