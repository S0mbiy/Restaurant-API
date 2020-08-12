from RestaurantType import RestaurantType
class Manager:
    def __init__(self):
        self.types = list()

    def add(self, obj):
        self.types.append(obj)

    def read(self):
        res = []
        for obj in self.types:
            res.append(obj.__dict__)
        return res

    def search(self, column, val):
        res = []
        for obj in self.types:
            if (obj.__dict__[column] == val):
                res.append(obj.__dict__["ID"])
        return res

    def get(self, id):
        for obj in self.types:
            if (obj.__dict__["ID"] == id):
                return obj

    def update(self, id, obj):
        for o in self.types:
            if (o.__dict__["ID"] == id):
                o.__dict__ = obj.__dict__
                break

    def remove(self, id):
        for o in self.types:
            if (o.__dict__["ID"] == id):
                self.types.remove(o)
                break

if __name__ == "__main__":
    m = Manager()
    m.add(RestaurantType())
    m.add(RestaurantType())
    m.add(RestaurantType())
    print(m.read())

