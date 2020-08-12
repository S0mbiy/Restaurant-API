from RestaurantType import RestaurantType
import Database


class MenuItem(RestaurantType):
    def __init__(self, number, name, price, ingredients, category, labels, availability=True):
        super().__init__()
        self.number = number
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.availability = availability
        self.category = category
        self.labels = labels
        Database.add_menu_item(number, name, price, ingredients, category, labels, availability)

    def set_availability(self, val):
        self.availability = val
        Database.menu[self.number]['availability'] = val

    def set_price(self, val):
        self.price = val
        Database.menu[self.number]['price'] = val
