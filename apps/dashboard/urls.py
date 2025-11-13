from django.urls import path

from apps.dashboard.views import (
    MyAssignedTablesView,
    CurrentOrdersView,
    CustomerReviews,
    AddCustomerReview
)

urlpatterns = [
    path('my-assigned-tables/', MyAssignedTablesView.as_view(), name='my-assigned-tables'),
    path('current-orders/', CurrentOrdersView.as_view(), name='current-orders'),
    path('customer-reviews/', CustomerReviews.as_view(), name='customer-reviews'),
    path('add-customer-review/', AddCustomerReview.as_view(), name='add-customer-review'),
]
