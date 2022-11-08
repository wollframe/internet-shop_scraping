from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .scraping import collect_products


from .models import User, Goods
from .forms import GForm


def index(request):
    return render(request, "auctions/index.html", {
      "goods": Goods.objects.all(),  
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def product(request, g_id):
    a = Goods.objects.get(pk = g_id)
    context = {
        'product' : a,
    }
    return render(request, 'auctions/product.html', context)



@login_required   
def create(request):
        if request.method == 'POST':
            form = GForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("create"))
        form = GForm()
        context = {
        'form': form,
        }
        return render(request, "auctions/create.html", context)



def fill_database(request):
    if request.method == 'POST':
        try:
            collect_products()
        except:
            err = 'ERROR'
            print(err)
            return render(request, "auctions/fill_products.html", {'message': str(err)})
    return render(request, "auctions/fill_products.html" ,{'message': None})