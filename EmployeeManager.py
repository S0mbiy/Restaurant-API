from Manager import Manager
import Database
from Employee import Employee


class EmployeeManager(Manager):

    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for user, data in Database.employees.items():
            self.types.append(Employee(data['name'], data['age'], data['gender'], data['position'], data['start_date'], data['labour_hours'], user, data['password']))

    def add(self, name, age, gender, position, start_date, labour_hours, user, password):
        super().add(Employee(name, age, gender, position, start_date, labour_hours, user, password))

    def remove(self, id):
        user = self.get(id).user
        del Database.employees[user]
        super().remove(id)
