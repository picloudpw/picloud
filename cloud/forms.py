from django import forms
from .models import *
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'subject', 'type', 'image', 'link', 'file')


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', )


class SigninForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', )


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('avatar', 'program', )