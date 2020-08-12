import requests
import json

USER = '';

def display(elements):
    if not elements:
        print("There are no elements to display.\n")
    for element in elements:
        for key, val in element.items():
            print(key, ": ", val, ", ", end="")
        print("")
    print("")

def customer():
    # authenticate user
    customer_id = requests.post('http://127.0.0.1:2000/get_customer_var', {'user': USER, 'var':'ID'}).text
    if customer_id == "Error":
        print("Error getting user id.\n")
        return
    while True:
        print("1. Make reservation")
        print("2. See Menu")
        print("3. Make order")
        print("4. Log out")
        cmmd = input("Enter number of desired command.\n")
        if (cmmd == "1"):
            try:
                date = input("Enter desired date:\n")
                time = input("Enter desired hour:\n")
                num_people = int(input("Enter number of people:\n"))
                petitions = input("Enter especial petitions, if any:\n")
                type = input("Enter desired type of table (smokers, non-smokers, bar, couches), if any:\n")
                # display suited tables for reservation
                tables = json.loads(requests.post('http://127.0.0.1:2000/get_option_tables', {'capacity': num_people, 'type': type}).text)
                display(tables)
                table_num = int(input("Enter table number:\n"))
                table_numbers = []
                for table in tables:
                    table_numbers.append(table['Num'])
                if table_num not in table_numbers:
                    print("That table number is not available, try again.\n")
                    continue
            except Exception as e:
                print("Wrong data input, try again.\n", e)
                continue
            # make reservation with provided details
            requests.post('http://127.0.0.1:2000/make_reservation', {'table_num': table_num, 'date':date, 'time':time, 'num_people': num_people, 'petitions':petitions, 'type':type, 'customer_id':customer_id})
            print("Successful making of reservation.\n")
        elif (cmmd == "2"):
            # display menu items
            menu = json.loads(requests.get('http://127.0.0.1:2000/get_menu').text)
            display(menu)
        elif (cmmd == "3"):
            orders = []
            tkaway = input("Type 1 if order is take away.\n")
            tkaway = True if tkaway == "1" else False
            while(True):
                order = input("Type item number to add to order, type 0 when done.\n")
                if(order is "0"):
                    break
                else:
                    try:
                        order = int(order)
                        qtty = input("Type desired quantity.\n")
                        qtty = int(qtty)
                        orders.append((order, qtty))
                    except:
                        print("Invalid menu item or amount")
            payment = input("Type your credit card number\n")
            cvv = input("Type credit card cvv\n")
            exp = input("Type credit card expiration mm/yy\n")
            # Make order request
            resp = requests.post('http://127.0.0.1:2000/make_order', data={'order_items': json.dumps(orders),'type': tkaway, 'customer_id': customer_id, 'customer_name': ''})
            if resp.status_code != 200:
                print('Error making order: {}'.format(resp.status_code))
            else:
                order_id = resp.text
                print("Placement of order successful.\n")
                # display receipt
                resp = requests.post('http://127.0.0.1:2000/get_receipt', data={'ID': order_id})
                if resp.status_code != 200:
                    print('Error making order: {}'.format(resp.status_code))
                else:
                    receipt = resp.text
                    if receipt != "Error":
                        print(receipt)
                    else:
                        print("Error downloading receipt.\n")

        elif (cmmd == "4"):
            return
        else:
            print("Invalid option.")

def waiter():
    # authenticate user
    employee_id = requests.post('http://127.0.0.1:2000/get_employee_var', {'user': USER, 'var':'ID'}).text
    if employee_id == "Error":
        print("Error getting employee id.\n")
        return
    while True:
        print("1. Manage reservations")
        print("2. Manage orders")
        print("3. Manage tables")
        print("4. Log out")
        cmmd = input("Enter number of desired command.\n")

        if (cmmd == "1"):
            while True:
                # display reservations
                reservations = json.loads(requests.get('http://127.0.0.1:2000/get_reservations').text)
                display(reservations)
                print("1. Reservation arrived")
                print("2. Cancel Reservation")
                print("3. Back")
                rsv_cmmd = input("Enter number of desired command.\n")
                if rsv_cmmd == "1":
                    rsv = input("Enter reservation ID.\n")
                    # Mark table as occupied and remove reservation from list
                    keys = {"ID": rsv}
                    resp = requests.post('http://127.0.0.1:2000/reservation_arrived', data=keys)
                    if resp.status_code != 200:
                        print('Error setting reservation arrival: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Reservation marked as arrived.\n')
                        else:
                            print('Error setting reservation arrival.\n')
                elif rsv_cmmd == "2":
                    rsv = input("Enter reservation ID.\n")
                    keys = {"ID": rsv}
                    # Remove reservation
                    resp = requests.post('http://127.0.0.1:2000/cancel_reservation', data=keys)
                    if resp.status_code != 200:
                        print('Error cancelling reservation: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Reservation cancelled.\n')
                        else:
                            print('Error cancelling reservation.\n')
                elif rsv_cmmd == "3":
                    break
                else:
                    print("Invalid option.")
        elif cmmd == "2":
            while True:
                # display orders
                orders = json.loads(requests.get('http://127.0.0.1:2000/get_orders').text)
                display(orders)
                print("1. Mark as delivered")
                print("2. Reload")
                print("3. Back")
                rsv_cmmd = input("Enter number of desired command.\n")
                if rsv_cmmd == "1":
                    order_id = input("Type order ID to mark as ready.\n")
                    # mark order as delivered
                    resp = requests.post('http://127.0.0.1:2000/change_order_status', data={'order': order_id, 'status': 'delivered'})
                    if resp.status_code != 200:
                        print('Error changing status to delivered: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Order status changed to delivered.\n')
                        else:
                            print('Error changing status to delivered.\n')
                elif rsv_cmmd == "2":
                    continue
                elif rsv_cmmd == "3":
                    break
                else:
                    print("Invalid option.")
        elif cmmd == "3":
            while True:
                # display tables
                tables = json.loads(requests.get('http://127.0.0.1:2000/get_tables').text)
                display(tables)
                print("1. Mark as occupied")
                print("2. Mark as free")
                print("3. Reload")
                print("4. Back")
                rsv_cmmd = input("Enter number of desired command.\n")
                if rsv_cmmd == "1":
                    table_num = input("Type table num to mark as occupied.\n")
                    # change table to occupied
                    resp = requests.post('http://127.0.0.1:2000/table_status', data={'table_num': table_num, 'occupied': 1})
                    if resp.status_code != 200:
                        print('Error marking table as occupied: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Table marked as occupied.\n')
                        else:
                            print('Error marking table as occupied.\n')
                elif rsv_cmmd == "2":
                    table_num = input("Type table num to mark as free.\n")
                    # change table to free
                    resp = requests.post('http://127.0.0.1:2000/table_status', data={'table_num': table_num, 'occupied': 0})
                    if resp.status_code != 200:
                        print('Error marking table as free: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Table marked as free.\n')
                        else:
                            print('Error marking table as free.\n')
                elif rsv_cmmd == "3":
                    continue
                elif rsv_cmmd == "4":
                    break
                else:
                    print("Invalid option.")
        elif (cmmd == "4"):
            return
        else:
            print("Invalid option.")

def chef():
    # authenticate user
    employee_id = requests.post('http://127.0.0.1:2000/get_employee_var', {'user': USER, 'var':'ID'}).text
    if employee_id == "Error":
        print("Error getting employee id.\n")
        return
    while True:
        print("1. Manage orders")
        print("2. Log out")
        cmmd = input("Enter number of desired command.\n")

        if (cmmd == "1"):
            while True:
                # display orders
                orders = json.loads(requests.get('http://127.0.0.1:2000/get_orders').text)
                display(orders)
                print("1. Mark ready")
                print("2. Reload")
                print("3. Go back")
                ordr_cmmd = input("Enter number of desired command.\n")
                if ordr_cmmd == "1":
                    order_id = input("Type order ID to mark as ready.\n")
                    # change order status to ready
                    resp = requests.post('http://127.0.0.1:2000/change_order_status', data={'order': order_id, 'status': 'ready'})
                    if resp.status_code != 200:
                        print('Error changing status to ready: {}'.format(resp.status_code))
                    else:
                        if(resp.text!="Error"):
                            print('Order status changed to ready.\n')
                        else:
                            print('Error changing status to ready.\n')
                elif ordr_cmmd == "2":
                    continue
                elif ordr_cmmd == "3":
                    break
                else:
                    print("Invalid option.")
        elif (cmmd == "2"):
            return
        else:
            print("Invalid option.")

def admin():
    # authenticate user
    admin_id = requests.post('http://127.0.0.1:2000/get_admin_var', {'user': USER, 'var':'ID'}).text
    if admin_id == "Error":
        print("Error getting admin id.\n")
        return
    while True:
        print("1. Add employee")
        print("2. Add admin")
        print("3. Get statistics")
        print("4. Log out")
        cmmd = input("Enter number of desired command.\n")

        if (cmmd == "1"):
            try:
                while True:
                    user = input("Type new user name.\n")
                    # check if user is available for use
                    resp = requests.post('http://127.0.0.1:2000/check_user', data={'user': user})
                    if resp.status_code != 200:
                        print('Error checking user: {}'.format(resp.status_code))
                    else:
                        if(resp.text=="Error"):
                            print("Username not available.\n")
                        else:
                            break
                password = input("Type new password.\n")
                name = input("Type employee's name.\n")
                gender = input("Type employee's gender.\n")
                age = int(input("Enter employee's age.\n"))
                position = input("Enter employee's position.\n")
                start_date = input("Enter employee's start_date.\n")
                labour_hours = input("Enter employee's labour hours.\n")
                # add a new employee
                resp = requests.post('http://127.0.0.1:2000/make_employee', data={'name': name, 'gender': gender, 'age': age, 'position': position, 'start_date': start_date, 'labour_hours': labour_hours, 'user': user, 'password': password})
                if resp.status_code != 200:
                    print('Error adding new employee: {}'.format(resp.status_code))
                else:
                    print("New employee added.\n")
            except:
                print("Incorrect data input.\n")

        elif (cmmd == "2"):
            try:
                while True:
                    user = input("Type new user name.\n")
                    # check if user is available
                    resp = requests.post('http://127.0.0.1:2000/check_user', data={'user': user})
                    if resp.status_code != 200:
                        print('Error checking user: {}'.format(resp.status_code))
                    else:
                        if(resp.text=="Error"):
                            print("Username not available.\n")
                        else:
                            break
                password = input("Type new password.\n")
                name = input("Type admin's name.\n")
                # add new admin
                resp = requests.post('http://127.0.0.1:2000/make_admin', data={'name': name, 'user': user, 'password': password})
                if resp.status_code != 200:
                    print('Error adding new admin: {}'.format(resp.status_code))
                else:
                    print("New admin added.\n")
            except:
                print("Incorrect data input.\n")
        elif (cmmd == "3"):
            # display statistics
            stats = requests.get('http://127.0.0.1:2000/get_statistics').text
            print("Stats:")
            print(stats)
            print()
        elif (cmmd == "4"):
            return
        else:
            print("Invalid option.")

def actions(role):
    print("Hello " + USER + ".\n")
    if(role=="Waiter"):
        waiter()
    elif(role=="Customer"):
        customer()
    elif(role == "Chef"):
        chef()
    elif(role == "Administrator"):
        admin()
    return "END"



if __name__=="__main__":
    while(True):
        print("1. See Menu")
        print("2. Make Order")
        print("3. Make account")
        print("4. Log in")
        cmmd = input("Enter number of desired command.\n")

        if (cmmd == "1"):
            print('Menu:')
            # display menu
            menu = json.loads(requests.get('http://127.0.0.1:2000/get_menu').text)
            display(menu)

        elif (cmmd == "2"):
            orders = []
            tkaway = input("Type 1 if order is take away.\n")
            tkaway = True if tkaway == "1"  else False
            while(True):
                order = input("Type item number to add to order, type 0 when done.\n")
                if(order is "0"):
                    break
                else:
                    try:
                        order = int(order)
                        qtty = input("Type desired quantity.\n")
                        qtty = int(qtty)
                        orders.append((order, qtty))
                    except:
                        print("Invalid menu item or amount")
            name = input("Type your name.\n")
            payment = input("Type your credit card number\n")
            cvv = input("Type credit card cvv\n")
            exp = input("Type credit card expiration mm/yy\n")
            # Make order request
            resp = requests.post('http://127.0.0.1:2000/make_order', data={'order_items': json.dumps(orders),'type': tkaway, 'customer_id': '', 'customer_name': name})
            if resp.status_code != 200:
                print('Error making order: {}'.format(resp.status_code))
            else:
                order_id = resp.text
                print("Placement of order successful.\n")
                # display receipt
                resp = requests.post('http://127.0.0.1:2000/get_receipt', data={'ID': order_id})
                if resp.status_code != 200:
                    print('Error making order: {}'.format(resp.status_code))
                else:
                    receipt = resp.text
                    if receipt != "Error":
                        print(receipt)
                    else:
                        print("Error downloading receipt.\n")

        elif cmmd == "3":
            try:
                while True:
                    user = input("Type new user name.\n")
                    # check user is available
                    resp = requests.post('http://127.0.0.1:2000/check_user', data={'user': user})
                    if resp.status_code != 200:
                        print('Error checking user: {}'.format(resp.status_code))
                    else:
                        if(resp.text=="Error"):
                            print("Username not available.\n")
                        else:
                            break
                password = input("Type new password.\n")
                name = input("Type your name.\n")
                gender = input("Type your gender.\n")
                age = int(input("Enter your age.\n"))
                address = input("Enter your address.\n")
                email = input("Enter email.\n")
                phone = str(int(input("Enter phone.\n")))
                # add new customer
                resp = requests.post('http://127.0.0.1:2000/make_customer', data={'name': name, 'gender': gender, 'age': age, 'address': address, 'email': email, 'phone': phone, 'user': user, 'password': password})
                if resp.status_code != 200:
                    print('Error making user: {}'.format(resp.status_code))
                else:
                    print("New user created.\n")
            except:
                print("Incorrect data input.\n")


        elif (cmmd == "4"):
            user = input("Enter Username.\n")
            password = input("Enter Password.\n")
            # Login request
            keys = {"user": user, "password": password}
            resp = requests.post('http://127.0.0.1:2000/login', data=keys)
            if resp.status_code != 200:
                print('Error logging in: {}'.format(resp.status_code))
            else:
                if(resp.text!="Error"):
                    print('Logged in successfully.\n')
                    USER = user
                    while(True):
                        session = actions(resp.text)
                        if(session=="END"):
                            break
                else:
                    print('Error logging in.\n')

        else:
            print("Invalid option.")



