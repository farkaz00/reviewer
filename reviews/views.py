from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


from reviews.forms import RegisterForm, LoginForm, ReviewForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        return HttpResponse("Registered")

    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login(request):
    if request.method != "POST":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    
    username = request.POST.get("username", False)
    password = request.POST.get("password", False)
    user = authenticate(request, username=username, password=password)
    print(username, password)

    if user is None:
        return HttpResponse("Invalid login")

    login(request, user)
    return HttpResponse("Authenticated")


def logout(request):
    return HttpResponse('Logged out')


def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        return HttpResponse("Reviewed")

    form = ReviewForm()
    return render(request, "review.html", {"form": form})


def list_reviews(request):
    return HttpResponse('List reviews')


def index(request):
    return HttpResponse("Hi Reviewer!!")


def welcome(request):
    template = loader.get_template('welcome.html')
    context = {}
    return HttpResponse(template.render(context, request))
