# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import User


class RegistrationForm(ModelForm):
    username = forms.CharField(required=True)
    fieldbook_book = forms.CharField(required=True, label="Fieldbook ID")
    email = forms.EmailField(required=True, label="Email Address")
    password = forms.CharField(required=True ,widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True,widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
