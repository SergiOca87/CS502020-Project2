from django.contrib.auth.models import AbstractUser
from django.db import models


# each time you change anything in auctions/models.py, you’ll need to first run 
# python manage.py makemigrations and then python manage.py migrate

class User(AbstractUser):
    # Watchlist (related to listings)
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    text_description = models.CharField(max_length=128)
    starting_bid = models.PositiveIntegerField()
    image_url = models.CharField(max_length=128)
    # category (not sure)

    
    def __str__(self):
        return f"{self.title} has been added"
    

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass
    # related to listing