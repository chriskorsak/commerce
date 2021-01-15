from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add-remove-watchlist/<int:listing_id>", views.add_remove_watchlist, name="add-remove-watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("listing-categories", views.listing_categories, name="listing-categories"),
    path("category/<str:category>", views.category, name="category"),
    path("close-listing/<int:listing_id>", views.close_listing, name="close-listing")
]
