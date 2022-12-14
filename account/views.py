from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from .models import Account
from django.conf import settings


def home(request):
    
    return render(request, 'account/home.html', {'name':'rabinweb'})


def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("product:products")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                return redirect("product:products")
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
            return redirect("product:products")
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)



def logout_view(request):
    logout(request)
    return redirect('product:products')



def edit_account_view(request, *args, **kwrags):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwrags.get('user_id')
    account = Account.objects.get(pk=user_id)
    
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit this profile")
    dic = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
            initial={
                'id' : account.id,
                'email' : account.email,
                'username' : account.username,
                'profile_image' : account.profile_image,
            }
            )
            dic['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                'id' : account.id,
                'email' : account.email,
                'username' : account.username,
                'profile_image' : account.profile_image,
            }           
        )
        dic['form'] = form
        dic['user'] = account
        
    dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/profile.html',dic)