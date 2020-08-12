from flask import Flask
from flask import request
from AdminManager import AdminManager
from CustomerManager import CustomerManager
from EmployeeManager import EmployeeManager
from MenuManager import MenuManager
from OrderManager import OrderManager
from ReservationManager import ReservationManager
from StatisticsManager import StatisticsManager
from TableManager import TableManager
import Database
import sched, time
import threading
import json


app = Flask(__name__)

class Restaurant():
    def __init__(self):
        self.admin = AdminManager()
        self.customer = CustomerManager()
        self.employee = EmployeeManager()
        self.menu = MenuManager()
        self.order = OrderManager(self.menu)
        self.reservation = ReservationManager()
        self.statistics = StatisticsManager()
        self.table = TableManager()


res = Restaurant()

@app.route('/login', methods=['POST'])
def login():
    user = request.values.get('user')
    password = request.values.get('password')
    DBpasswd = Database.users.get(user)
    if(DBpasswd is not None and password==DBpasswd):
        employee = Database.employees.get(user)
        if(Database.customers.get(user)is not None):
            return "Customer"
        elif(employee is not None):
            return employee["position"]
        elif(Database.administrators.get(user)is not None):
            return "Administrator"
    return "Error"

@app.route('/reservation_arrived', methods=['POST'])
def mark_reservation():
    ID = request.values.get('ID')
    if res.reservation.search("ID", ID):
        number_list = res.table.search('table_num', int(res.reservation.get(ID).table))
        res.table.get(number_list[0]).set_occupied(True)
        res.reservation.remove(ID)
        return "OK"
    return "Error"

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    ID = request.values.get('ID')
    if res.reservation.search("ID", ID):
        res.reservation.remove(ID)
        return "OK"
    return "Error"

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    t = request.values.get('table_num')
    d = request.values.get('date')
    tm = request.values.get('time')
    c = request.values.get('customer_id')
    n = request.values.get('num_people')
    p = request.values.get('petitions')
    ty = request.values.get('type')
    res.reservation.add(t, d, tm, c, n, p, ty)
    return "OK"

@app.route('/make_order', methods=['POST'])
def make_order():
    order_items = request.values.get('order_items')
    type = request.values.get('type')
    customer_id = request.values.get('customer_id')
    customer_name = request.values.get('customer_name')
    ID = res.order.add(order_items, type, customer_id, customer_name)
    return ID

@app.route('/make_customer', methods=['POST'])
def make_customer():
    name = request.values.get('name')
    gender = request.values.get('gender')
    age = request.values.get('age')
    address = request.values.get('address')
    email = request.values.get('email')
    phone = request.values.get('phone')
    user = request.values.get('user')
    password = request.values.get('password')
    res.customer.add(name, gender, age, address, email, phone, user, password)
    return "OK"

@app.route('/make_employee', methods=['POST'])
def make_employee():
    name = request.values.get('name')
    gender = request.values.get('gender')
    age = request.values.get('age')
    position = request.values.get('position')
    start_date = request.values.get('start_date')
    labour_hours = request.values.get('labour_hours')
    user = request.values.get('user')
    password = request.values.get('password')
    res.employee.add(name, age, gender, position, start_date, labour_hours, user, password)
    return "OK"

@app.route('/make_admin', methods=['POST'])
def make_admin():
    name = request.values.get('name')
    user = request.values.get('user')
    password = request.values.get('password')
    res.admin.add(name, user, password)
    return "OK"

@app.route('/check_user', methods=['POST'])
def check_user():
    u = request.values.get('user')
    if(Database.users.get(u)==None):
        return "OK"
    return "Error"

@app.route('/get_receipt', methods=['POST'])
def get_receipt():
    ID = request.values.get('ID')
    if res.order.search("ID", ID):
        return res.order.get(ID).get_receipt()
    return "Error"

@app.route('/change_order_status', methods=['POST'])
def change_order_status():
    o = request.values.get('order')
    status = request.values.get('status')
    if res.order.search("ID", o):
        if status=="ready":
            res.order.ready(o)
        elif status=="delivered":
            res.order.delivered(o)
        else:
            return "Error"
        return "OK"
    return "Error"

@app.route('/get_statistics', methods=['GET'])
def get_statistics():
    stats = res.statistics.order_statistics()
    return "Avergae spend per order: " + str(stats[0]) + ", Total Orders: " + str(stats[1])

@app.route('/get_reservations', methods=['GET'])
def get_reservations():
    return json.dumps(res.reservation.read())

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return json.dumps(res.order.read())

@app.route('/get_menu', methods=['GET'])
def get_menu():
    return json.dumps(res.menu.read())

@app.route('/get_tables', methods=['GET'])
def get_tables():
    return json.dumps(res.table.read())

@app.route('/table_status', methods=['POST'])
def table_status():
    table_num = int(request.values.get('table_num'))
    occupied = bool(int(request.values.get('occupied')))
    if res.table.search("table_num", table_num):
        number_list = res.table.search('table_num', table_num)
        res.table.get(number_list[0]).set_occupied(occupied)
        return "OK"
    return "Error"

@app.route('/get_option_tables', methods=['POST'])
def get_option_tables():
    cap = int(request.values.get('capacity'))
    type = request.values.get('type')
    return json.dumps(res.table.find_table(cap, type))

@app.route('/get_customer_var', methods=['POST'])
def get_customer_var():
    u = request.values.get('user')
    var = request.values.get('var')
    q = res.customer.search('user', u)
    if q:
        return res.customer.get(q[0]).__dict__[var]
    return "Error"

@app.route('/get_admin_var', methods=['POST'])
def get_admin_var():
    u = request.values.get('user')
    var = request.values.get('var')
    q = res.admin.search('user', u)
    if q:
        return res.admin.get(q[0]).__dict__[var]
    return "Error"

@app.route('/get_employee_var', methods=['POST'])
def get_employee_var():
    u = request.values.get('user')
    var = request.values.get('var')
    q = res.employee.search('user', u)
    if q:
        return res.employee.get(q[0]).__dict__[var]
    return "Error"

s = sched.scheduler(time.time, time.sleep)

def loop():
    s.enter(60, 1, loop)
    res.order.check_if_late()


threading.Thread(target=loop).start()
threading.Thread(target=app.run, kwargs={'port': 2000}).start()
s.run()
