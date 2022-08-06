from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('1', 'Place Owner'),
                                           ('2', 'Costumer')))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'user_type', 'phone_number', 'password1', 'password2']
