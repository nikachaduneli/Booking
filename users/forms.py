from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=((None, '----'),
                                          ('Place Owner', 'Place Owner'),
                                          ('Costumer', 'Costumer')))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'user_type', 'phone_number', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']
