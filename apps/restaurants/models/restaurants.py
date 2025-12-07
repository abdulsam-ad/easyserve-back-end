from django.db import models

from apps import restaurants, userprofile
from coresite.mixin import AbstractTimeStampModel


class Restaurant(AbstractTimeStampModel):
    """
    Model representing a restaurant.
    """
    owners = models.ManyToManyField(
        'userprofile.UserProfile',
        related_name='owned_restaurants',
        blank=True
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cuisine = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name

class RestaurantImage(AbstractTimeStampModel):
    """
    Model representing an image of a restaurant.
    """
    restaurant = models.ForeignKey("restaurants.Restaurant",
                                   related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.restaurant.name}"
