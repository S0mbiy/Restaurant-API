from RestaurantType import RestaurantType
import Database


class Reservation(RestaurantType):
    def __init__(self, table, date, time, customer_id, num_people, petitions, type, ID=None):
        super().__init__(ID)
        self.table = table
        self.date = date
        self.time = time
        self.customer_id = customer_id
        self.num_people = num_people
        self.petitions = petitions
        self.type = type
        Database.add_reservation(self.ID, table, date, time, customer_id, num_people, petitions, type)

