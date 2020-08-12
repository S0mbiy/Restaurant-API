from RestaurantType import RestaurantType


class Receipt(RestaurantType):
    def __init__(self, menu_manager,order_items, total, type):
        super().__init__()
        self.menu_manager = menu_manager
        self.order_items = order_items
        self.total = total
        self.type = type
        self.receipt = self._make_receipt()

    def _make_receipt(self):
        receipt = "Receipt:\n"
        receipt += "Take-away: " + self.type + "\nOrder:\n"
        for order_item in self.order_items:
            menu_item = self.menu_manager.get(self.menu_manager.search('number', order_item[0])[0])
            receipt += (menu_item.name + "\tqtty: " + str(order_item[1]) + "\t$" + str(menu_item.price*order_item[1]) + '\n')
        receipt += "Total = " + str(self.total)
        return receipt
