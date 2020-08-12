from Manager import Manager
from Order import Order
import Database
import json
import time
from datetime import datetime


class OrderManager(Manager):
    def __init__(self, menu_manager):
        super().__init__()
        self.menu_manager = menu_manager
        self._load()

    def _load(self):
        for ID, data in Database.orders.items():
            self.types.append(Order(json.loads(data['order_items']), self.menu_manager, data['type'], data['customer_id'], data['customer_name'], data['status'], data['total'], data['date'], data['time'], ID))

    def add(self, order_items, type, customer_id = '', customer_name = ''):
        order = Order(json.loads(order_items), self.menu_manager, type, customer_id, customer_name)
        super().add(order)
        return order.ID

    def ready(self, id):
        super().get(id).status = 'ready'
        Database.orders[id]['status'] = 'ready'

    def delivered(self, id):
        super().remove(id)
        Database.orders[id]['status'] = 'delivered'

    def remove(self, id):
        super().remove(id)
        Database.orders[id]['status'] = 'cancelled'

    def read(self):
        res = []
        for obj in self.types:
            elements = dict(obj.__dict__)
            del(elements['menu_manager'])
            del(elements['receipt'])
            res.append(elements)
        return res

    def check_if_late(self):
        now = time.mktime(datetime.now().timetuple())
        for obj in self.types:
            elements = dict(obj.__dict__)
            datetime_object = time.mktime(datetime.strptime(elements['creation_date'], '%Y-%m-%d %H:%M:%S.%f').timetuple())
            if int(now-datetime_object)/60 > 5:
                obj.status = "late"

if __name__ == "__main__":
    from MenuManager import MenuManager
    menu = MenuManager()
    m = OrderManager(menu)
    print(m.read())
    m.add([(1, 2)], "take-away")
    print(m.types[0].get_receipt())
    print(m.read())
