from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    # path("add/<int:user_id>", views.add, name="add"),
    path("<int:listing_id>", views.listing, name="listing"),
    # path("<int:listing_id>", views.listing, name="addToWatchlist"),
    # path("<int:listing_id>", views.listing, name="closeListing")
]
