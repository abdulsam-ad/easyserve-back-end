from django.db import models
from apps import restaurants

from coresite.mixin import AbstractTimeStampModel


class Category(AbstractTimeStampModel):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        related_name='categories',
        on_delete=models.CASCADE,
    )

    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'name'],
                name='unique_category_per_restaurant'
            )
        ]

    def __str__(self):
        return self.name
