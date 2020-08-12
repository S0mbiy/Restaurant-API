from Manager import Manager
from MenuItem import MenuItem
import Database


class MenuManager(Manager):
    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for num, data in Database.menu.items():
            self.types.append(MenuItem(num, data['name'], data['price'], data['ingredients'], data['category'], data['labels'], data['availability']))

    def add(self, number, name, price, ingredients, category, labels, availability=True):
        super().add(MenuItem(number, name, price, ingredients, category, labels, availability))

    def remove(self, id):
        num = self.get(id).number
        del Database.menu[num]
        super().remove(id)

if __name__ == "__main__":
    m = MenuManager()
    print(m.read())
    m.get(m.search('number', 1)[0]).set_price(11)
    print(m.read())
