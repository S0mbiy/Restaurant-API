from Manager import Manager
from Table import Table
import Database


class TableManager(Manager):
    def __init__(self):
        super().__init__()
        self._load()

    def _load(self):
        for num, data in Database.tables.items():
            self.types.append(Table(num, data['capacity'], data['type'], data['occupied']))

    def add(self, table_num, capacity, type, occupied=False):
        super().add(Table(table_num, capacity, type, occupied))

    def remove(self, id):
        num = self.get(id).table_num
        del Database.tables[num]
        super().remove(id)

    def find_table(self, capacity, type):
        opt = []
        for table in self.types:
            if table.capacity >= capacity and not table.occupied:
                if table.type == type or type == '':
                    opt.append({"Num": table.table_num, "Type": table.type})
        return opt


