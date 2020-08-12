import Database


class StatisticsManager():

    def order_statistics(self):
        n = 0
        total = 0
        for ID, order in Database.orders.items():
            if order["status"] != "cancelled":
                total += order["total"]
                n += 1
        if n != 0:
            return (total/n, n)
        return (0, 0)


if __name__ == "__main__":
    s = StatisticsManager()
    print(s.order_statistics())
