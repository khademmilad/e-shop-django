from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import AccountAuthenticationForm, RegistrationForm
from .models import Account


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


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("account:home")
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)



def logout_view(request):
    logout(request)
    return redirect('account:home')


def profile_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse('Somthing went wrong!')
    
    print('account', account)
        
    context['user'] = account

    return render(request, 'account/profile.html', context)