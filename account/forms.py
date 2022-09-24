from django import forms
from django.contrib.auth import authenticate
from .models import Account


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='email', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login!")