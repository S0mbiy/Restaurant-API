from User import User
import Database
class Employee(User):
    def __init__(self, name, age, gender, position, start_date, labour_hours, user, password):
        super().__init__(user, password)
        self.name = name
        self.age = age
        self.gender = gender
        self.position = position
        self.start_date = start_date
        self.labour_hours = labour_hours
        Database.add_employee(name, age, gender, position, start_date, labour_hours, user, password)


