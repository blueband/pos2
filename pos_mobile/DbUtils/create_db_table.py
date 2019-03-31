from DbUtils import dbconn
conn = dbconn.con()

def admin_login():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Admin_login
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,  username VARCHAR, pin INTEGER, security_question TEXT)''')

# this function creates table that stores reps login details
def rep_login():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Rep_login
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, pin INTEGER)''')

# this function creates table that stores information about the admin
def admin_reg():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Admin_Details
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, adminID INTEGER REFERENCES Admin_login(ID) ON UPDATE CASCADE,surname TEXT, first_name TEXT, 
             mobile no VARCHAR, address VARCHAR, next_of_kin_name VARCHAR)''')

# this function creates table that stores information about the rep
def reps_reg():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Rep_Details
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, repID INTEGER REFERENCES Rep_login(ID) ON UPDATE CASCADE, surname TEXT, first_name TEXT, 
            mobile VARCHAR, address VARCHAR, next_of_kin_name TEXT)''')


def customer_account():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS customer
            (id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT, first_name TEXT, 
            mobile_phone VARCHAR, email TEXT, address VARCHAR)''')

# this function creates table that stores information about the capital used to start the business
def my_capital():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS My_Capital
        (ID INTEGER PRIMARY KEY AUTOINCREMENT, Capital FLOAT, Loan FLOAT)''')


def shopconfig():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS shopconfig
        (ID INTEGER PRIMARY KEY AUTOINCREMENT, shop_name VARCHAR, Owner_name varchar, owner_phone INTEGER, email VARCHAR, shop_init_capital, shop_address VARCHAR)''')

# this function creates table that keeps record of stock
def product_table():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Products
    (ID INTEGER PRIMARY KEY AUTOINCREMENT, p_name TEXT, 
    p_quantity FLOAT, p_cost FLOAT, p_selling_price FLOAT, stock_lowAt INTEGER)''')

# this function creates table that keeps record of sales made
def order_table():
    for_navigate = conn.cursor()
    for_navigate.execute("PRAGMA foreign_keys=ON")
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS sales_order(saleID INTEGER PRIMARY KEY AUTOINCREMENT, 
    productID INTEGER REFERENCES Products(ID) ON UPDATE CASCADE, customerID INTEGER REFERENCES customers(id) ON UPDATE CASCADE, order_quantity FLOAT, price FLOAT, transactID INTEGER REFERENCES transact_table(transactID) ON UPDATE CASCADE, sales_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')


def transaction_table():
    # records of all successful transaction
    for_navigate = conn.cursor()
    for_navigate.execute("PRAGMA foreign_keys=ON")
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS transact_table(transactID INTEGER PRIMARY KEY AUTOINCREMENT, 
        transact_code VARCHAR, transact_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')
# def receipt():
#     for_connect = sqlite3.connect('stock_DB.sqlite')
#     for_navigate = for_connect.cursor()
#     for_navigate.execute('''CREATE TABLE IF NOT EXISTS
#         Receipt_gen(ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         product_sold TEXT, quantity FLOAT, pricePERunit FLOAT, cost FLOAT, staff TEXT, time
#


# this function creates table that keeps record of admin expenses
def ownerExpenses_table():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS 
    Owners_Expenses(ID INTEGER PRIMARY KEY AUTOINCREMENT, Expenses TEXT, 
    cost FLOAT)''')

# this function creates table that keeps record of rep expenses
def repExpenses_table():
    for_navigate = conn.cursor()
    for_navigate.execute('''CREATE TABLE IF NOT EXISTS Reps_Expenses(ID INTEGER PRIMARY KEY AUTOINCREMENT, Expenses TEXT, 
        cost FLOAT)''')

def on_start_program_run():
    try:
        admin_login()
        rep_login()
        admin_reg()
        reps_reg()
        customer_account()
        my_capital()
        product_table()
        transaction_table()
        order_table()
        ownerExpenses_table()
        repExpenses_table()
        shopconfig()

        print('I was able to create neccessary Table Successfully')
    except conn.Error as e:
        print(e.args[0])
#on_start_program_run()