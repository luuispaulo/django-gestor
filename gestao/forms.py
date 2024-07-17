# forms.py
from django import forms

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    tenant_name = forms.CharField(max_length=50)

class FormHomePage(forms.Form):
    email = forms.EmailField(label=False)