from Manager import Manager
from Reservation import Reservation
import Database


class ReservationManager(Manager):
    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for ID, data in Database.reservations.items():
            self.add(data['table'], data['date'], data['time'], data['customer_id'], data['num_people'], data['petitions'], data['type'], ID)

    def add(self, table, date, time, customer_id, num_people, petitions, type, ID=None):
            super().add(Reservation(table, date, time, customer_id, num_people, petitions, type, ID))

    def remove(self, id):
        super().remove(id)
        del Database.reservations[id]


if __name__ == "__main__":
    m = ReservationManager()
    print(m.read())
