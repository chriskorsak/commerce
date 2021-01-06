from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  # watchlist = models.ManyToManyField(Listing)

  def __str__(self):
    return f"{self.username} ({self.first_name} {self.last_name})"

# Need at least these three models for specification:

class Listing(models.Model):
  # foreign key refers to the User object
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  title = models.CharField(max_length=64)
  price = models.DecimalField(max_digits=8, decimal_places=2)
  description = models.TextField(max_length=256)
  date = models.DateField(auto_now_add=True)
  photo = models.URLField(max_length=200, blank=True)

  # returns a string representation of the Listing object
  def __str__(self):
    return f"User:{self.user} Item:{self.title} Price:{self.price} Date Listed:{self.date}"

class Bid(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=8, decimal_places=2)
  bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return f"Listing:{self.listing} price:{self.price}"

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  date = models.DateField(auto_now_add=True)
  comment = models.CharField(max_length=256)
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

  def __str__(self):
    return f"Date:{self.date} Comment:{self.comment} Listing:{self.listing}"



