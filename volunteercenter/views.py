from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from django.http import JsonResponse
from .serializers import UserSerializer, deliverySerializer, prescriptionSerializer, welfareSerializer
from .models import User, Delivery, Prescription, Welfare

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == "handler":
            return HttpResponseRedirect(reverse("call_handler_index"))
        elif request.user.user_type == "operator":
            return HttpResponseRedirect(reverse("operator_index"))
        else:
            return render(request, "volunteercenter/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def call_handler_index(request):
    if request.user.is_authenticated:
        return render(request, "volunteercenter/callhandler.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def operator_index(request):
    if request.user.is_authenticated:
        return render(request, "volunteercenter/operator.html")
    else:
        return HttpResponseRedirect(reverse("login"))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "volunteercenter/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "volunteercenter/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "volunteercenter/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "volunteercenter/register.html", {
                "message": "Username address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "volunteercenter/register.html")
