from pickle import FALSE
import mysql.connector

username = "hello"
password = "123456"

access_granted = FALSE
print("\n\n")

while access_granted == False:
    Checkuser = input("Enter username here:- ")
    Checkpass = input("Enter Your Password:- ")

    if Checkpass == password and Checkuser == username:
        access_granted = True
        print("\n\n\n")
        start = input("Enter Any Key To Start The Program...")

    elif Checkpass == "exit" or Checkuser == "exit":
        break

    else:
        print("\nTry Again\n")


while access_granted:
    try:
        mydb = mysql.connector.connect(user="root", password="123456")
        database = "myshop"
        mycursor = mydb.cursor()
        mycursor.execute("show databases")
    except Exception as error:
        print(error, 'here')

    database_exist = False
    for db in mycursor:
        if db[0] == database:
            database_exist = True

    if database_exist == False:
        print("databse doesn't exist therefore creating databse...")
        mycursor.execute(f'create database {database}')
        print("databse created succesfully")
        mydb = mysql.connector.connect(
            user="root", password="123456", database=database)
        print("connection established successfully")
        mycursor = mydb.cursor()

    elif database_exist == True:
        print("databse exist therefore connecting...")
        mydb = mysql.connector.connect(
            user="root", password="123456", database=database)
        print("connection established successfully")
        mycursor = mydb.cursor()

    try:
        mycursor.execute(
            "create table products(Serial INT unique auto_increment not null, Name varchar(50) not null, Price int not null, Quantity int not null, SKU varchar(4) unique, Primary key(SKU))")
        mycursor.execute(
            "create table bills(Serial int unique auto_increment not null, Customer varchar(50), Amount int not null, date )")
    except:
        try:
            mycursor.execute(
                "create table bills(Serial int unique auto_increment not null, Customer varchar(50), Amount int not null, date varchar(50) not null)")
        except:
            print("tables are found...")
    finally:
        print("tables succesfully connected")

    def add_Product():
        name_product = input("Enter Name Of The Product:- ")
        price_product = int(input("Enter Price Of The Product:- "))
        quantity_product = int(input("Enter Quantity Of The Product:- "))
        SKU_product = input("Enter SKU Of The Product:- ")
        add_product = (
            "INSERT INTO products" "(name, price, quantity, sku)" "VALUES(%s, %s, %s, %s)")
        data_product = (name_product, price_product,
                        quantity_product, SKU_product)
        try:
            mycursor.execute(add_product, data_product)
            print("Product Added Successfully ----")
        except:
            print("Following SKU or Product Already exist")
        mydb.commit()

    def delete_Product():
        SKU_product = (input("Enter SKU Of The Product:- "))
        delete_product = (f'DELETE FROM products WHERE SKU="{SKU_product}"')
        try:
            mycursor.execute(delete_product)
            print("Product Deleted Successfully ----")
        except:
            print("Following SKU or Product Doesn't exist")
        mydb.commit()

    def increase_Product_quantity():
        SKU_product = input("Enter SKU Of The Product:- ")
        increase_qtyby = int(input("Enter The Addition Of Quantity:- "))
        select_query = (f'SELECT * FROM products WHERE SKU="{SKU_product}"')

        try:
            mycursor.execute(select_query)
            result = mycursor.fetchall()
            current_qty = result[0][3]
            new_qty = int(current_qty) + int(increase_qtyby)
            mycursor.execute(
                f'UPDATE products SET quantity={new_qty} WHERE SKU="{SKU_product}"')
            print("Product Quantity Successfully Updated")
        except:
            print("The Following SKU or Product Doesn't Exist")
        mydb.commit()

    def decrease_Product_quantity():
        SKU_product = input("Enter SKU Of The Product:- ")
        decrease_qtyby = int(input("Enter The Subtraction Of Quantity:- "))
        select_query = (f'SELECT * FROM products WHERE SKU="{SKU_product}"')

        try:
            mycursor.execute(select_query)
            result = mycursor.fetchall()
            current_qty = result[0][3]
            new_qty = int(current_qty) - int(decrease_qtyby)
            mycursor.execute(
                f'UPDATE products SET quantity={new_qty} WHERE SKU="{SKU_product}"')
            print("Product Quantity Successfully Updated")
        except:
            print("The Following SKU or Product Doesn't Exist")
        mydb.commit()

    def create_invoice():
        customer_name = input("Enter The Customer Name:- ")
        price = 0
        n = int(input("Enter No. Products Bought:- "))
        items = []
        items_qty = []

        for i in range(n):
            sku = input("Enter SKU of the product Bought:- ")
            items.append(sku)
            qty = int(input("Enter The Quantity Of The Product:- "))
            items_qty.append(qty)

        for i in range(n):
            try:
                mycursor.execute(
                    f'SELECT * FROM products WHERE SKU="{items[i]}"')
                result = mycursor.fetchall()
                product_price = result[0][2]
                price += items_qty[i] * product_price

                decrease_qtyby = items_qty[i]
                current_qty = result[0][3]
                new_qty = int(current_qty) - int(decrease_qtyby)
                mycursor.execute(
                    f'UPDATE products SET quantity={new_qty} WHERE SKU="{items[i]}"')

            except:
                print("SKU or Product Doesn't exist")
        mycursor.execute(
            f'INSERT INTO bills (customer, Amount, date) VALUES("{customer_name}", {price}, CURRENT_TIMESTAMP)')

        print(f'Amount To Be Paid:- {price}\n\n')
        money_in = int(input("Enter The Amount Given By Customer:- "))
        return_money = money_in - price

        print(
            f'\nTotal Amount To Be Paid:- {price}\nMoney Given By The Customer:- {money_in}\nBalance Of The Customer:- {return_money}')

        mydb.commit()

    while True:
        print('\n\n')
        print("---------------------------------")
        print("----Welcome to MyStoreHelper-----\n")
        print("Select your desirable operation:-")
        print("Press 1: to add or delete any product")
        print("Press 2: to create an invoice")
        print("Press 3: to edit products quantity")
        print("Press 4: to save changes to the database")
        print("Press 5: to exit")

        option = int(input("Enter Your Option:- "))
        print("\n\n")

        if option == 1:
            action = input("Want to add or delete a product? Enter(A/D)\n")
            if action == "A" or action == 'a':
                add_Product()
            elif action == 'D' or action == 'd':
                delete_Product()
            end = input("\n\nEnter any key to go back to the main menu")

        elif option == 2:
            create_invoice()
            end = input("\n\nEnter any key to go back to the main menu")

        elif option == 3:
            action = input(
                "Want to increase or decrease a product quantity? Enter(I/D)\n")
            if action == "I" or action == 'i':
                increase_Product_quantity()
            elif action == 'D' or action == 'd':
                decrease_Product_quantity()
            end = input("\n\nEnter any key to go back to the main menu")

        elif option == 4:
            mydb.commit()
            print("\n\nAll the data is successfully saved in the database")
            end = input("\n\nEnter any key to go back to the main menu")

        elif option == 5:
            mydb.commit()
            mydb.close()
            print("\n\nThank You For Using MyStoreHelper \nHave a Nice Day")
            break

        else:
            print("Try again and Enter a valid option")
