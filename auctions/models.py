from django.contrib.auth.models import AbstractUser
from django.db import models


# each time you change anything in auctions/models.py, you’ll need to first run 
# python manage.py makemigrations and then python manage.py migrate


# User is in quotes as it has not yet been defined before the Listing model, lazy reference
class Bids(models.Model):
    pass

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    text_description = models.CharField(max_length=128)
    starting_bid = models.PositiveIntegerField()
    image_url = models.CharField(max_length=128)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdBy",default=None, null=True, blank=True)
    bids = models.ManyToManyField(Bids, blank=True, related_name="Bids")
    # category (not sure)

    
    def __str__(self):
        return f"{self.title} has been added"
    


class Comments(models.Model):
    pass
    # related to listing