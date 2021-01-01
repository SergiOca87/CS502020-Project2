from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Category, Comment

class NewBidForm(forms.Form):
    amount = forms.IntegerField(label='Bid Amount')

class NewCommentForm(forms.Form):
    text = forms.CharField(label='Comment Text', widget=forms.Textarea)

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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

@login_required
def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        url = request.POST["url"]
        user = User.objects.get(id=request.POST["user_id"])
        category = request.POST["category"]
        f = Listing(title = title, text_description=description, starting_bid=bid, image_url=url, created_by=user)
        c = Category(name = category)
        f.save()
        c.save()
        c.listings.add(f)
        c.save()
       
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/add.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    current_user = request.user
    user_watchlist = Listing.objects.filter(watchlist=request.user.id)
    in_watchlist = False
    listing_bids = Bid.objects.filter(bids=listing)
    comments = list(listing.comments.all())

    if request.method == "POST":
        if 'closeListing' in request.POST and request.POST['closeListing']:
            listing.is_active = False
            listing.won_by = User.objects.get(id=listing.highest_bid.bid_by.id)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        elif 'addToWatchlist' in request.POST and request.POST['addToWatchlist']:
            current_user.watchlist.add(listing)
            return HttpResponseRedirect(reverse("index"))
        elif 'removeFromWatchlist' in request.POST and request.POST['removeFromWatchlist']:
            current_user.watchlist.remove(listing)
            return HttpResponseRedirect(reverse("index"))
        elif 'comment' in request.POST and request.POST['comment']:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                text = comment_form.cleaned_data["text"]
                f = Comment( text = text, author = current_user)
                f.save()
                listing.comments.add(f)
                listing.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "created_by": listing.created_by,
                    "message": "Thank you, the bid was placed correctly",
                    "bid_form": NewBidForm(),
                    "comment_form": NewCommentForm(),
                    "comments": comments
                })  

        elif 'bid' in request.POST and request.POST['bid']:
            bid_form = NewBidForm(request.POST)
            if bid_form.is_valid():
                amount = bid_form.cleaned_data["amount"]

                if amount <= listing.starting_bid:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "created_by": listing.created_by,
                        "message": "The bid must be higher than the starting price",
                        "bid_form": NewBidForm(),
                        "comment_form": NewCommentForm(),
                        "comments": comments
                    })  
                elif amount <= listing.highest_bid.amount :
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "created_by": listing.created_by,
                        "message": "The bid must be higher than the current bid",
                        "bid_form": NewBidForm(),
                        "comment_form": NewCommentForm(),
                        "comments": comments
                    })  
                else:
                    f = Bid( amount = amount, bid_by = current_user, bid_on = listing )
                    f.save()
                    listing.bids.add(f)
                    listing.highest_bid = Bid.objects.get(id=f.id)
                    listing.save()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "created_by": listing.created_by,
                        "message": "Thank you, the bid was placed correctly",
                        "bid_form": NewBidForm(),
                        "comment_form": NewCommentForm(),
                        "comments": comments
                    })  


    elif listing in user_watchlist:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "in_watchlist": True,
            "created_by": listing.created_by,
            "bid_form": NewBidForm(),
            "comment_form": NewCommentForm(),
            "comments": comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "created_by": listing.created_by,
            "bid_form": NewBidForm(),
            "comment_form": NewCommentForm(),
            "comments": comments
        })

@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlist=request.user.id)
    current_user = request.user
    print( listings )
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = list(category.listings.all())
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })