from django.urls import path

from apps.dashboard.views import MyAssignedTablesView, CurrentOrdersView

urlpatterns = [
    path('my-assigned-tables/', MyAssignedTablesView.as_view(), name='my-assigned-tables'),
    path('current-orders/', CurrentOrdersView.as_view(), name='current-orders'),
]
