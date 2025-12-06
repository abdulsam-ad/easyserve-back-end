from django.db import models

from apps import restaurants
from apps.userprofile.models import UserProfile
from coresite.mixin import AbstractTimeStampModel


PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
)

ORDER_STATUS = (
    ("TO_PREPARE", "To Prepare"),
    ("PREPARING", "Preparing"),
    ("PREPARED", "Prepared"),
    ("SERVED", "Served"),
)

ORDER_TYPES = (
    ("DINE_IN", "Dine In"),
    ("TAKEAWAY", "Takeaway"),
    ("DELIVERY", "Delivery"),
)

class OrderItem(AbstractTimeStampModel):
    order = models.ForeignKey('restaurants.Orders', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    menu_item = models.ForeignKey('restaurants.MenuItem', on_delete=models.CASCADE, related_name='menu_item_order_items')
    quantity = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # def __str__(self):
    #     return self.menu_item.name + ' - ' + str(self.quantity) + ' pcs'

    def __str__(self):
        return self.menu_item.name

class Orders(AbstractTimeStampModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default="DINE_IN")
    table = models.ForeignKey('restaurants.Table', on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name="orders")
    waiter = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name="waiter_orders")
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default="TO_PREPARE"
    )

    billing_first_name = models.CharField(max_length=255, blank=True, null=True)
    billing_last_name = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)
    billing_phone = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.CharField(max_length=500, blank=True, null=True)
    shipping_address = models.CharField(max_length=500, blank=True, null=True)

    # Common fields
    ordered_date = models.DateTimeField(null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Pending")
    order_cancelled = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)

    @property
    def total_items(self):
        return self.menu_item.count()
    
    def __str__(self):
        return f"Order {self.id}"
