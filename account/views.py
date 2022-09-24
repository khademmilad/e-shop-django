from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import AccountAuthenticationForm

def home(request):
    
    return render(request, 'account/home.html', {'name':'rabinweb'})


def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("account:home")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                return redirect("account:home")
    else:
        form = AccountAuthenticationForm()

    context = {
        "login_form": form
    }

    return render(request, "account/login.html", context)