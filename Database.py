users = {"juan": "juan1", "sergio": "sergio1", "mary": 'mary1', "paul":"paul1", "mike":"mike1"}
employees = {"mary": {'name':"Mary", 'age':30, 'gender':'F', 'position':'Chef', 'start_date':'21/10/2010', 'labour_hours':'9-17', 'password':'mary1'},
             "paul": {'name':"paul", 'age':30, 'gender':'M', 'position':'Waiter', 'start_date':'21/10/2010', 'labour_hours':'9-17', 'password':'paul1'},
             "mike": {'name':"Mike", 'age':30, 'gender':'M', 'position':'Waiter', 'start_date':'21/10/2010', 'labour_hours':'9-17', 'password':'mike1'}
             }
customers = {"juan":{'name':'Juan', 'gender':'M', 'age':30, 'address':'Ballarad Rd 101', 'email':'juan@email.com', 'phone':'0401020304', 'password':'juan1'}}
administrators = {"sergio": {'name':'sergio', 'password':'sergio1'}}

menu = {
    1: {'name':'Coffee', 'price':5, 'ingredients':'Coffee beans, Hot water', 'category':'beverage', 'labels':'', 'availability': True},
    2: {'name':'Eggs', 'price':10, 'ingredients':'Eggs', 'category':'breakfast', 'labels':'gluten-free', 'availability': False}
}

tables = {
    1: {'capacity':10, 'type':'smokers', 'occupied':False},
    2: {'capacity':5, 'type':'bar', 'occupied':False},
    3: {'capacity':6, 'type':'non-smokers', 'occupied':False},
    4: {'capacity':4, 'type':'couches', 'occupied':True}
}

reservations = {

}

orders = {

}

def add_customer(name, gender, age, address, email, phone, user, password):
    if(users.get(user)==None):
        users[user] = password
        customers[user] = {'name':name, 'gender':gender, 'age':age, 'address':address, 'email':email, 'phone':phone, 'password':password}

def add_administrator(name, user, password):
    if(users.get(user)==None):
        users[user] = password
        administrators[user] = {'name':name, 'password':password}

def add_employee(name, age, gender, position, start_date, labour_hours, user, password):
    if(users.get(user)==None):
        users[user] = password
        employees[user] = {'name':name, 'age':age, 'gender':gender, 'position':position, 'start_date':start_date, 'labour_hours':labour_hours, 'password':password}

def add_menu_item(number, name, price, ingredients, category, labels, availability):
    if(menu.get(number)==None):
        menu[number] = {'name':name, 'price':price, 'ingredients':ingredients, 'category':category, 'labels':labels, 'availability': availability}

def add_table(table_num, capacity, type, occupied):
    if(tables.get(table_num)==None):
        tables[table_num] = {'capacity':capacity, 'type':type, 'occupied':occupied}

def add_reservation(ID, table, date, time, customer_id, num_people, petitions, type):
    if(reservations.get(ID)==None):
        reservations[ID] = {'table':table, 'date':date, 'time':time, 'customer_id':customer_id, 'num_people':num_people, 'petitions':petitions, 'type':type}

def add_order(ID, order_items, total, date, time, type, status, customer_id, customer_name):
    if(orders.get(ID)==None):
        orders[ID] = {'order_items':order_items, 'total':total, 'date':date, 'time':time, 'type':type, 'status':status, 'customer_id':customer_id, 'customer_name':customer_name}
