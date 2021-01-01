from django.contrib import admin

from .models import Listing
from .models import Bid
from .models import Comment
from .models import Category

admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)

# Register your models here.
