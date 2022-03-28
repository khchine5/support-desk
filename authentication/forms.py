from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_staff",
        )


class LoginForm(forms.Form):
    username = forms.CharField(label="Your username", max_length=100)
    password = forms.CharField(
        label="Your password", max_length=100, widget=forms.PasswordInput()
    )
