from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
    "listings": Listing.objects.all()
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

@login_required(login_url='login')
def create_listing(request):
  if request.method == "POST":
    user = request.user
    title = request.POST["title"]
    price = request.POST["price"]
    description = request.POST["description"]
    photo = request.POST["photo"]
    category = request.POST["category"]

    # create new listing object with above variables gathered from create listing form:
    listing = Listing(user=user, title=title, price=price, description=description, photo=photo, category=category)

    # save listing object to database:
    listing.save()

  # form = CreateEntryForm() 
  # return render(request, "auctions/create-listing.html", {'form': form} )
  return render(request, "auctions/create-listing.html")

def listing(request, listing_id):
  listing = Listing.objects.get(pk=listing_id)
  return render(request, "auctions/listing.html", {
    "listing": listing
  })

def add_remove_watchlist(request, listing_id):
  if request.method == "POST":
    #get user and listing from listing id
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    #add/remove listing to user's watchlist
    if user.watchlist.filter(pk=listing_id):
      user.watchlist.remove(listing)
      # message = "Removed from watchlist"
    else:
      user.watchlist.add(listing)
      # message = "Added to watchlist"

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
  user = request.user
  watchlist = user.watchlist.all()
  return render(request, "auctions/watchlist.html", {
    "watchlist": watchlist
  })

