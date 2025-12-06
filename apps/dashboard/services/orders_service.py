from apps.restaurants.models import ORDER_STATUS
from apps.dashboard.repositories import OrdersRepository

LABEL_TO_VALUE = {label: value for value, label in ORDER_STATUS}


class OrderService:
    @staticmethod
    def change_status(order, label):
        value = LABEL_TO_VALUE.get(label)

        if value is None:
            raise ValueError(f"Invalid status '{label}'")

        return OrdersRepository.update_status(order, value)
