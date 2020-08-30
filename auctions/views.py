from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing

class NewBidForm(forms.Form):
    bid = forms.IntegerField()

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        url = request.POST["url"]
        f = Listing(title = title, text_description=description, starting_bid=bid, image_url=url)
        f.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/add.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": NewBidForm()
    })

def addToWatchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    # Render the user watchlist?
    # Then render listings that are related to that user somehow...?

# def placeBid(request):
#     if request.method == "POST":
#         listing = Listing.objects.get(id=listing_id)
#         form = NewBidForm(request.POST)
#         if form.is_valid():
#             bid = form.cleaned_data["bid"]

#             # Check if bid is lower than current price 
#             if bid <= listing.current_price:
#                 return render(request, "auctions/listing.html", {
#                     "listing": listing,
#                     "form": NewBidForm(),
#                     "message": "Bid was lower than current listing price"
#                 })
#             else :
#                 # Create the bid
#                 f = Bids(amount=bid)
#                 f.save

#                 # Add bid amount to listing current price
#                 listing.current_price += bid
#                 return render(request, "auctions/listing.html", {
#                     "listing": listing,
#                     "form": NewBidForm(),
#                     "message": "Bid was successful"
#                 })
#     else:
#         return render(request, "auctions/listing.html", {
#             "listing": listing,
#             "form": NewBidForm(),
#             "message": "There was a problem with the proided amount"
#         })
    # else:
    #     listing = Listing.objects.get(id=listing_id)
    #     return render(request, "auctions/listing.html", {
    #         "listing": listing,
    #         "form": NewBidForm()
    #     })
    