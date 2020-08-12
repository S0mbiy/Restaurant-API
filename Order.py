from RestaurantType import RestaurantType
import Database
from datetime import datetime
from Receipt import Receipt
import json


class Order(RestaurantType):
    def __init__(self, order_items, menu_manager, type, customer_id = '', customer_name = '', status = "pending", total = None, date = None, time = None, ID = None):
        super().__init__(ID)
        self.order_items = order_items # List of tuples with menuItem id and quantity
        self.menu_manager = menu_manager
        if total is None:
            self.total = self._total()
        else:
            self.total = total
        if date is None:
            self.date = str(datetime.today())
        else:
            self.date = date
        if time is None:
            self.time = str(datetime.now().time())
        else:
            self.time = time
        self.type = type
        self.receipt = Receipt(menu_manager, self.order_items, self.total, type)
        self.status = status
        self.customer_id = customer_id
        self.customer_name = customer_name
        Database.add_order(self.ID, json.dumps(self.order_items), self.total, self.date, self.time, type, status, customer_id, customer_name)

    def _total(self):
        total = 0
        for order_item in self.order_items:
            menu_item = self.menu_manager.get(self.menu_manager.search('number', order_item[0])[0])
            total += menu_item.price * order_item[1]
        return total

    def get_receipt(self):
        return self.receipt.receipt



