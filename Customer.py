from User import User
import Database
class Customer(User):
    def __init__(self, name, gender, age, address, email, phone, user, password):
        super().__init__(user, password)
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.email = email
        self.phone = phone
        Database.add_customer(name, age, gender, address, email, phone, user, password)


