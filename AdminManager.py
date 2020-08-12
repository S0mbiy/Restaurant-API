from Manager import Manager
import Database
from Administrator import Administrator


class AdminManager(Manager):

    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for user, data in Database.administrators.items():
            self.types.append(Administrator(data['name'], user, data['password']))

    def add(self, name, user, password):
        super().add(Administrator(name, user, password))

    def remove(self, id):
        user = self.get(id).user
        del Database.administrators[user]
        super().remove(id)



if __name__ == "__main__":
    m = AdminManager()
    print(m.read())
    m.remove(m.search('user', 'sergio')[0])
    print(m.read())
