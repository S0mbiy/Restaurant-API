from User import User
import Database
class Administrator(User):
    def __init__(self, name, user, password):
        super().__init__(user, password)
        self.name = name
        Database.add_administrator(name, user, password)

