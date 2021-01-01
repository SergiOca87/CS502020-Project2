from django.contrib.auth.models import AbstractUser
from django.db import models


# each time you change anything in auctions/models.py, you’ll need to first run 
# python manage.py makemigrations and then python manage.py migrate


# User is in quotes as it has not yet been defined before the Listing model, lazy reference
class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")

class Bid(models.Model):
    amount = models.PositiveIntegerField(default=None, null=True, blank=True)
    bid_by = models.ForeignKey(User, related_name="bid_by", on_delete=models.CASCADE, default=None, null=True, blank=True)
    bid_on = models.ForeignKey('Listing', related_name="bid_on", on_delete=models.CASCADE, default=None, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField('Listing', blank=True, related_name="listings")

class Comment(models.Model):
    text = models.CharField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", default=None, null=True, blank=True)
    comment_on = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="comment_on", default=None, null=True, blank=True)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    text_description = models.CharField(max_length=128)
    starting_bid = models.PositiveIntegerField()
    image_url = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", default=None, null=True, blank=True)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    highest_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="highest_bid")
    is_active = models.BooleanField(default=True, null=True, blank=True)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_by", default=None, null=True, blank=True)
