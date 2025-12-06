from apps import userprofile, restaurants
from coresite.mixin import AbstractTimeStampModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(AbstractTimeStampModel):
    order = models.OneToOneField(
        'restaurants.Orders',
        on_delete=models.CASCADE,
        related_name='review'
    )
    
    user = models.ForeignKey(
        'userprofile.UserProfile',
        on_delete=models.SET_NULL,
        related_name='customer_reviews',
        null=True,
        blank=True,
    )

    waiter = models.ForeignKey(
        'userprofile.UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='waiter_reviews',
        help_text='Assign waiter if dine-in service was provided.',
    )
    
    created_by = models.CharField(max_length=20, choices=[("customer","Customer"),("waiter","Waiter")])
    
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review {self.id}: {self.rate} stars"

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
