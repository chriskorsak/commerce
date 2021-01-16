from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
# from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
    # "listings": Listing.objects.all()
    "listings": Listing.objects.filter(status=True)
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
    # .title() capitalizes each word
    title = request.POST["title"].title()
    price = float(request.POST["price"])
    description = request.POST["description"]
    photo = request.POST["photo"]
    category = request.POST["category"].capitalize()

    # create new listing object with above variables gathered from create listing form:
    listing = Listing(user=user, title=title, price=price, description=description, photo=photo, category=category)

    # save listing object to database:
    listing.save()

    # automatically add listing to listing creator's watchlist
    user.watchlist.add(listing)
    
    messages.add_message(request, messages.INFO, 'Listing created!', extra_tags='alert alert-primary')
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

  return render(request, "auctions/create-listing.html")

def listing(request, listing_id):
  #get listing from listing id
  listing = Listing.objects.get(pk=listing_id)
  #get all bids on listing to display on page
  bids = listing.bids.all()
  # get user
  user = request.user
  # get creator of listing
  listing_creator = listing.user
  # get all listing comments
  comments = listing.comments.all()

  #only if user is logged in:

  #message if listing on user's watchlist
  if request.user.is_authenticated:
    if user.watchlist.filter(pk=listing_id):
      watchlist_message = "Watching item"
    else:
      watchlist_message = "Not watching item"

    #create variable which allows listing creator to use 'end listing' button on listing page
    if user == listing_creator:
      user_is_creator = True
    else:
      user_is_creator = False

    #find max bid for listing using 'latest' function
    if bids:
      max_bid = bids.latest('price')
    else:
      max_bid = None
    
    return render(request, "auctions/listing.html", {
      "listing": listing,
      "watchlist_message": watchlist_message,
      "bids": bids,
      "comments": comments,
      "user_is_creator": user_is_creator,
      "max_bid": max_bid
    })
  else:
    return render(request, "auctions/listing.html", {
      "listing": listing
    })

@login_required(login_url='login')
def add_remove_watchlist(request, listing_id):
  if request.method == "POST":
    #get user and listing from listing id
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    #add/remove listing to user's watchlist
    if user.watchlist.filter(pk=listing_id):
      user.watchlist.remove(listing)
    else:
      user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
  user = request.user
  watchlist = user.watchlist.all()
  return render(request, "auctions/watchlist.html", {
    "watchlist": watchlist
  })

@login_required(login_url='login')
def bid(request, listing_id):
  if request.method == "POST":
    #get user, listing from listing id, price from bid form on listing page
    listing = Listing.objects.get(pk=listing_id)
    price = float(request.POST["price"])
    bidder = request.user

    # automatically add listing to listing bidder's watchlist
    bidder.watchlist.add(listing)
    
    # if no bids yet, check to make sure first bid at least equals starting price
    if listing.bids.count() == 0:
      # apply listing, price and bidder to new bid object
      bid = Bid(listing=listing, price=price, bidder=bidder)
      #convert listing price to float for comparison (is this correct way to do???)
      listing.price = float(listing.price)
      #check to see if bid is greater than current price or bids
      if bid.price >= listing.price:
        #update listing price with newest bid
        listing.price = bid.price
        #save listing and bid objects
        listing.save()
        bid.save()

        messages.add_message(request, messages.INFO, 'Bid successful!', extra_tags='alert alert-primary')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
      else:
        messages.add_message(request, messages.INFO, 'Bid is not high enough.', extra_tags='alert alert-warning')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    #if there's already bids on listing, check to make sure GREATER than current price   
    else:
      # apply listing, price and bidder to new bid object
      bid = Bid(listing=listing, price=price, bidder=bidder)
      #check to see if bid is greater than current price or bids
      if bid.price > listing.price:
        #update listing price with newest bid
        listing.price = bid.price
        #save listing and bid 
        listing.save()
        bid.save()

        messages.add_message(request, messages.INFO, 'Bid successful!', extra_tags='alert alert-info')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
      else:
        messages.add_message(request, messages.INFO, 'Bid is not high enough.', extra_tags='alert alert-warning')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required(login_url='login')
def comment(request, listing_id):
  if request.method == "POST":
    #get comment from form, user, listing from listing id
    comment_text = request.POST["comment_text"]
    user = request.user
    listing = Listing.objects.get(pk=listing_id)

    #create new Comment object with comment text, listing_id, and user
    comment = Comment(user=user, comment=comment_text, listing=listing)
    #save comment to database
    comment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def listing_categories(request):
  categories = []
  #get all active listings with a category
  listings = Listing.objects.filter(status=True).exclude(category="")
  #iterate through listings and extract and add to categories list if unique
  for listing in listings:    
    if listing.category not in categories:
      categories.append(listing.category)
  
  #sort categories
  categories.sort()

  return render(request, "auctions/listing-categories.html", {
    "categories": categories
  })

def category(request, category):
  #get all listings with this category
  listings = Listing.objects.filter(category=category, status=True)
  return render(request, "auctions/category.html", {
    "listings": listings,
    "category": category
  })

def close_listing(request, listing_id):
  if request.method == "POST":
    #get user and compare to user who created listing
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing_creator = listing.user

    if user == listing_creator:
      messages.add_message(request, messages.INFO, 'Auction closed!', extra_tags='alert alert-info')
      # change listing status to False (which means auction is closed)
      listing.status = False
      listing.save()

      return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))