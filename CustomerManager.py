from Manager import Manager
import Database
from Customer import Customer


class CustomerManager(Manager):
    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for user, data in Database.customers.items():
            self.types.append(Customer(data['name'], data['gender'], data['age'], data['address'], data['email'], data['phone'], user, data['password']))

    def add(self, name, gender, age, address, email, phone, user, password):
        super().add(Customer(name, gender, age, address, email, phone, user, password))

    def remove(self, id):
        user = self.get(id).user
        del Database.customers[user]
        super().remove(id)
