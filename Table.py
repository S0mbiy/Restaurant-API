from RestaurantType import RestaurantType
import Database


class Table(RestaurantType):
    def __init__(self, table_num, capacity, type, occupied=False):
        super().__init__()
        self.occupied = occupied
        self.table_num = table_num
        self.capacity = capacity
        self.type = type
        self.reservations = []
        Database.add_table(table_num, capacity, type, occupied)

    def set_occupied(self, val):
        self.occupied = val
        Database.tables[self.table_num]['occupied'] = val

    def add_reservation(self, rsrv):
        self.reservations.append(rsrv)
        self.reservations = self.reservations.sort()


