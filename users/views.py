from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm


def index(request):         #отображение главной страницы

    return render(
        request,
        "index.html"    #да главная страница это index, а не main
    )


def register(request):      #рег

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("index")

    else:

        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form
        }
    )


def user_login(request):        #вход

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("index")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "users/login.html",
        {
            "form": form
        }
    )


def user_logout(request):       #выход

    logout(request)

    return redirect("index")