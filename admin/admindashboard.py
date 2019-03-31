from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from collections import OrderedDict
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import hashlib
from kivy.uix.label import Label

from kivy.lang.builder import Builder
from datetime import date

from DbUtils import dbconn
from utils.datatable import DataTable

Builder.load_file('admin/admindashboard.kv')

class admindashboardwindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = dbconn.con()
        self.page_title = self.ids.page_title
        self.info = self.ids.info_label

        #Global Shop Data
        self.get_capital_sales_expenses()
        self.shop_name = ''
        self.Owner_name = ''
        self.shop_address = ''
        self.shop_init_capital = str(4500)
        self.email = ''
        self.owner_phone = ''
        self.total_sellings_cost = 0
        self.total_unit_cost = 0
        self.current_income = 0
        self.current_profit = 0





        # ALL Stock Display Screen
        screen_all_products = self.ids.scrn_all_stock
        products = self.get_products()
        productstable = DataTable(table=products)
        screen_all_products.add_widget(productstable)

        # ALL Customers Display Screen
        screen_all_customers = self.ids.scrn_all_customers
        customers = self.get_customer()
        customertable = DataTable(table=customers)
        screen_all_customers.add_widget(customertable)

        # Manage User Display Screen
        Screen_user = self.ids.scrn_manage_users
        users = self.get_saleRep()
        usertable = DataTable(table=users)
        Screen_user.add_widget(usertable)

        #Manage All Expenses Display
        expenses_screen = self.ids.scrn_expense_output
        expenses = self.get_expenses()
        expenstable = DataTable(table=expenses)
        expenses_screen.add_widget(expenstable)




        # Manage Products Display Screen
        Screen_products_manage = self.ids.scrn_manage_products
        products_manage = self.get_products()
        productstable_manage = DataTable(table=products_manage)
        Screen_products_manage.add_widget(productstable_manage)

        # ALL Sold Products  Display Screen
        screen_all_solds = self.ids.scrn_all_sales
        sold_products = self.get_sold_products()
        sold_products_table = DataTable(table=sold_products)
        screen_all_solds.add_widget(sold_products_table)

    def saveShop_init_data(self):
        self.shop_name = self.ids.shop_name.text
        self.Owner_name = self.ids.Owner_name.text
        self.shop_address = self.ids.shop_address.text
        self.shop_init_capital = self.ids.shop_init_capital.text
        self.email = self.ids.email.text
        self.owner_phone = self.ids.owner_phone.text
        footer = self.ids.foot_section
        footer.text = self.shop_address

        handle = self.conn.cursor()
        previous_config = handle.execute('SELECT * FROM shopconfig')
        pprevious = previous_config.fetchall()
        if len(pprevious) <= 0:
            exp_sql = handle.execute(
                '''INSERT INTO shopconfig(shop_name, Owner_name, owner_phone, email, shop_init_capital, shop_address)VALUES(?,?,?,?,?,?)''',
                (self.shop_name, self.Owner_name, self.owner_phone, self.email, self.shop_init_capital,
                 self.shop_address))
            self.conn.commit()
        else:
            previous_config = handle.execute('SELECT * FROM shopconfig')
            pprevious = previous_config.fetchall()
            for previous in pprevious:
                self.shop_name = previous[1]
                self.Owner_name = previous[2]
                self.owner_phone = previous[3]
                self.email = previous[4]
                self.shop_init_capital = previous[5]
                self.shop_address = previous[6]

    def add_users_fields(self):
        target = self.ids.Operations_fields
        target.clear_widgets()
        crud_surname = TextInput(hint_text="Surname")
        crud_first_name = TextInput(hint_text="First_Name")
        crud_mobile = TextInput(hint_text="mobile")
        crud_address = TextInput(hint_text="address")
        crud_next_kin = TextInput(hint_text="next_kin")
        crud_username = TextInput(hint_text="username")
        crud_password = TextInput(hint_text="password")
        crud_submit = Button(text='Add User',size_hint_x=None, width=100, on_release=lambda x:self.add_users(crud_surname.text, crud_first_name.text, crud_mobile.text, crud_address.text, crud_next_kin.text, crud_username.text, crud_password.text))

        target.add_widget(crud_surname)
        target.add_widget(crud_first_name)
        target.add_widget(crud_mobile)
        target.add_widget(crud_address)
        target.add_widget(crud_next_kin)
        target.add_widget(crud_username)
        target.add_widget(crud_password)
        target.add_widget(crud_submit)


    def add_products_fields(self):
        target = self.ids.Operations_fields_products
        target.clear_widgets()
        crud_product_name = TextInput(hint_text="Products Name")
        crud_product_quantity = TextInput(hint_text="Quantity")
        crud_unit_cost = TextInput(hint_text="Unity Cost")
        crud_selling_cost = TextInput(hint_text="Selling Price")
        crud_stock_low_alert = TextInput(hint_text="Low Stock alert")
        crud_submit = Button(text='Add Product',size_hint_x=None, width=100, on_release=lambda x:self.add_products(crud_product_name.text, crud_product_quantity.text, crud_unit_cost.text, crud_selling_cost.text, crud_stock_low_alert.text))

        target.add_widget(crud_product_name)
        target.add_widget(crud_product_quantity)
        target.add_widget(crud_unit_cost)
        target.add_widget(crud_selling_cost)
        target.add_widget(crud_stock_low_alert)
        target.add_widget(crud_submit)



    def update_users_fields(self):
        target = self.ids.Operations_fields
        target.clear_widgets()
        crud_surname = TextInput(hint_text="Surname")
        crud_first_name = TextInput(hint_text="First_Name")
        crud_mobile = TextInput(hint_text="mobile")
        crud_address = TextInput(hint_text="address")
        crud_next_kin = TextInput(hint_text="next_kin")
        crud_username = TextInput(hint_text="username")
        crud_password = TextInput(hint_text="password")
        crud_submit = Button(text='Update Profile',size_hint_x=None, width=100, on_release=lambda x:self.update_rep(crud_surname.text, crud_first_name.text, crud_mobile.text, crud_address.text, crud_next_kin.text, crud_username.text, crud_password.text))

        target.add_widget(crud_surname)
        target.add_widget(crud_first_name)
        target.add_widget(crud_mobile)
        target.add_widget(crud_address)
        target.add_widget(crud_next_kin)
        target.add_widget(crud_username)
        target.add_widget(crud_password)
        target.add_widget(crud_submit)


    def update_products_fields(self):
        target = self.ids.Operations_fields_products
        target.clear_widgets()
        crud_product_name = TextInput(hint_text="Products Name")
        crud_product_quantity = TextInput(hint_text="Quantity")
        crud_unit_cost = TextInput(hint_text="Unity Cost")
        crud_selling_cost = TextInput(hint_text="Selling Price")
        crud_stock_low_alert = TextInput(hint_text="Low Stock alert")
        crud_submit = Button(text='Modify Product', size_hint_x=None, width=100,
                             on_release=lambda x: self.update_products(crud_product_name.text, crud_product_quantity.text,
                                                                    crud_unit_cost.text, crud_selling_cost.text,
                                                                    crud_stock_low_alert.text))

        target.add_widget(crud_product_name)
        target.add_widget(crud_product_quantity)
        target.add_widget(crud_unit_cost)
        target.add_widget(crud_selling_cost)
        target.add_widget(crud_stock_low_alert)
        target.add_widget(crud_submit)

    def add_users(self, surname, first_name, mobile, address, next_kin, username, password):
        Screen_user = self.ids.scrn_manage_users
        Screen_user.clear_widgets()
        handle = self.conn.cursor()


        if username == '' or password == '':
            self.info.text = '[color=#FF0000]Either Username, Password Question Field is incorrect[/color]'  # This print to the GUI

        elif mobile.isdigit() == False:
            self.info.text = '[color=#FF0000]"Mobile Number should be should be Integer[/color]'
        else:
            # Obsfucation of Password for Security using sha256
            password = hashlib.sha256(password.encode()).hexdigest()

            # Save Users Details into DB
            handle.execute('''INSERT INTO Rep_login(username, pin)VALUES(?,?)''',
                           (username, password))
            lastAccountID =handle.lastrowid
            handle.execute(
                '''INSERT INTO Rep_Details(repID, surname, first_name, mobile, address, next_of_kin_name)VALUES(?,?,?,?,?,?)''',
                (lastAccountID, surname, first_name, mobile, address, next_kin))

            self.conn.commit()


        users = self.get_saleRep()
        usertable = DataTable(table=users)
        Screen_user.add_widget(usertable)


    def add_products(self, product_name, product_quantity, unit_cost, selling_cost, stock_low_alert):
        Screen_product = self.ids.scrn_manage_products
        Screen_product.clear_widgets()


        if product_name == '' or product_quantity=='' or unit_cost=='' or selling_cost=='' or stock_low_alert=='':
            self.info.text = '[color=#FF0000] Either Product Name, Quantity, Unit Cost, Selling Cost or Low Stock Alert field is empty, kindly fill all field appropriately[/color]'
        elif unit_cost.isdigit() == False or selling_cost.isdigit==False or product_quantity.isdigit()== False or stock_low_alert.isdigit()==False:
            self.info.text = '[color=#FF0000]"Unit cost", "Selling Cost", "Product Quantity" and "Low Stock Alert" should be Integer[/color]'
        elif int(unit_cost) >= int(selling_cost):
            self.info.text = '[color=#FF0000] You can not sell at Lost, Your Selling Cost must be higher to make profit[/color]'
        else:
            handle = self.conn.cursor()
            previous_product = handle.execute('SELECT * FROM Products')
            pprevious = previous_product.fetchall()
            if len(pprevious) <=0:
                handle.execute('''INSERT INTO Products(p_name, p_quantity, p_cost, 
            p_selling_price, stock_lowAt)VALUES(?,?,?,?,?)''', (product_name, product_quantity, unit_cost, selling_cost, stock_low_alert))
                self.conn.commit()

                self.info.text = '[color=#0000FF] Product Save Successfully[/color]'
            else:
                previous_product = handle.execute('SELECT p_name FROM Products ')
                pprevious = previous_product.fetchall()
                previous_db_product = set()
                for product in pprevious:
                    previous_db_product.add(product[0])
                if product_name not in previous_db_product:
                    handle.execute('''INSERT INTO Products(p_name, p_quantity, p_cost,
                            p_selling_price, stock_lowAt)VALUES(?,?,?,?,?)''', (
                product_name, product_quantity, unit_cost, selling_cost, stock_low_alert))
                    self.conn.commit()
                else:
                    self.info.text = '[color=#FF0000]Duplicate Product, Use update Buttom to modify this Product[/color]'


        products = self.get_products()
        producttable = DataTable(table=products)
        Screen_product.add_widget(producttable)


    def saveExp(self):
        exp_date = date.today()

        exp_name = self.ids.exp_name.text
        exp_descript = self.ids.exp_descript.text
        exp_cost = self.ids.exp_cost.text

        handle = self.conn.cursor()
        exp_sql = handle.execute('''INSERT INTO Owners_Expenses(expenses, cost, description, exp_date)VALUES(?,?,?,?)''',(exp_name,exp_cost, exp_descript,exp_date))

        self.conn.commit()




    def get_saleRep(self):
        _salesrep = OrderedDict()
        _salesrep['surname'] = {}
        _salesrep['first_name'] = {}
        _salesrep['mobile'] = {}
        _salesrep['address'] = {}
        _salesrep['next_of_kin_name'] = {}
        _salesrep['username'] = {}


        handle = self.conn.cursor()
        surname = []
        first_name = []
        mobile = []
        address = []
        next_of_kin_name = []
        username = []

        salerep = handle.execute('SELECt * FROM Rep_Details LEFT JOIN  Rep_login on Rep_Details.repID = Rep_login.ID')

        salereps = salerep.fetchall()
        for salerep in salereps:
            surname.append(salerep[2])
            first_name.append(salerep[3])
            mobile.append(salerep[4])
            address.append(salerep[5])
            next_of_kin_name.append(salerep[6])
            username.append(salerep[8])


        surname_lenght = len(surname)
        idx = 0
        while idx < surname_lenght:
            _salesrep['surname'][idx] = surname[idx]
            _salesrep['first_name'][idx] = first_name[idx]
            _salesrep['mobile'][idx] = mobile[idx]
            _salesrep['address'][idx] = address[idx]
            _salesrep['next_of_kin_name'][idx] = next_of_kin_name[idx]
            _salesrep['username'][idx] = username[idx]
            idx += 1
        return _salesrep

    def update_rep(self, surname, first_name, mobile, address, next_kin, username, password):
        Screen_user = self.ids.scrn_manage_users
        Screen_user.clear_widgets()
        handle = self.conn.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()

        update_query = handle.execute('''UPDATE Rep_Details SET surname=?, first_name=?, mobile=?, address=?, next_of_kin_name=? WHERE surname=?''' , (surname, first_name, mobile, address, next_kin, surname ))
        update_login_field = handle.execute('''UPDATE Rep_login SET username=?, pin=? WHERE username=?''',(username, password, username))

        self.conn.commit()

        users = self.get_saleRep()
        usertable = DataTable(table=users)
        Screen_user.add_widget(usertable)


    def update_products(self,product_name, product_quantity, unit_cost,selling_cost, stock_low_alert):
        Screen_product = self.ids.scrn_manage_products
        Screen_product.clear_widgets()
        handle = self.conn.cursor()
        update_query = handle.execute('''UPDATE Products SET p_quantity=?, p_cost=?, p_selling_price=?, stock_lowAt=? WHERE p_name=?''' , (product_quantity, unit_cost, selling_cost, stock_low_alert, product_name))

        self.conn.commit()

        products = self.get_products()
        producttable = DataTable(table=products)
        Screen_product.add_widget(producttable)


    def get_products(self):
        _products = OrderedDict()
        _products['product_name'] = {}
        _products['product_quantity'] = {}
        _products['product_unit_cost']= {}
        _products['product_selling_cost'] = {}
        _products['stock_low_alert'] ={}

        handle = self.conn.cursor()
        product_name = []
        product_quantity =[]
        product_unit_cost = []
        product_selling_cost =[]
        stock_low_alert = []
        products = handle.execute('SELECt * FROM Products')
        products = products.fetchall()
        for product in products:
            product_name.append(product[1])
            product_quantity.append(product[2])
            product_unit_cost.append(product[3])
            product_selling_cost.append(product[4])
            stock_low_alert.append(product[5])



        product_lenght = len(product_name)
        idx = 0
        while idx < product_lenght:
            _products['product_name'][idx] = product_name[idx]
            _products['product_quantity'][idx] = product_quantity[idx]
            _products['product_unit_cost'][idx] = product_unit_cost[idx]
            _products['product_selling_cost'][idx] = product_selling_cost[idx]
            _products['stock_low_alert'][idx] = stock_low_alert[idx]
            idx += 1
        return _products


    def get_customer(self):
        _customers = OrderedDict()
        _customers['surname'] = {}
        _customers['first_name'] = {}
        _customers['mobile_phone']= {}
        _customers['email'] = {}
        _customers['address'] ={}

        handle = self.conn.cursor()
        surname = []
        first_name =[]
        mobile_phone = []
        email =[]
        address = []
        customers = handle.execute('SELECt * FROM customer')
        customers = customers.fetchall()
        for customer in customers:
            surname.append(customer[1])
            first_name.append(customer[2])
            mobile_phone.append(customer[3])
            email.append(customer[4])
            address.append(customer[4])

        customer_lenght = len(surname)
        idx = 0
        while idx < customer_lenght:
            _customers['surname'][idx] = surname[idx]
            _customers['first_name'][idx] = first_name[idx]
            _customers['mobile_phone'][idx] = mobile_phone[idx]
            _customers['email'][idx] = email[idx]
            _customers['address'][idx] = address[idx]
            idx += 1
        return _customers

    def get_expenses(self):
        _expenses = OrderedDict()
        _expenses['exp_name'] = {}
        _expenses['exp_description'] = {}
        _expenses['exp_cost'] = {}
        _expenses['exp_date'] = {}

        handle = self.conn.cursor()
        exp_name = []
        exp_description = []
        exp_cost = []
        exp_date = []
        expenses = handle.execute('SELECt * FROM Owners_Expenses')
        expenses = expenses.fetchall()
        for expense in expenses:
            exp_name.append(expense[1])
            exp_cost.append(expense[2])
            exp_description.append(expense[3])
            exp_date.append(expense[4])

        expense_lenght = len(exp_name)
        idx = 0
        while idx < expense_lenght:
            _expenses['exp_name'][idx] = exp_name[idx]
            _expenses['exp_cost'][idx] = exp_cost[idx]
            _expenses['exp_description'][idx] = exp_description[idx]
            _expenses['exp_date'][idx] = exp_date[idx]
            idx += 1
        return _expenses

    def get_sold_products(self):
        _sales = OrderedDict()
        _sales['product_name'] = {}
        _sales['order_quantity'] = {}
        _sales['order_cost'] = {}
        _sales['customerid'] = {}
        _sales['order_date'] ={}

        handle = self.conn.cursor()
        product_name = []
        order_quantity =[]
        order_cost = []
        customerid =[]
        order_date = []
        all_orders = handle.execute('''SELECt * FROM sales_order LEFT JOIN Products ON sales_order.productID=Products.ID ''')

        all_orders = all_orders.fetchall()

        for order in all_orders:
            product_name.append(order[8])
            order_quantity.append(order[3])
            order_cost.append(order[4])
            customerid.append(order[2])
            order_date.append(order[6])



        product_lenght = len(product_name)
        idx = 0
        while idx < product_lenght:
            _sales['product_name'][idx] = product_name[idx]
            _sales['order_quantity'][idx] = order_quantity[idx]
            _sales['order_cost'][idx] = order_cost[idx]
            _sales['customerid'][idx] = customerid[idx]
            _sales['order_date'][idx] = order_date[idx]
            idx += 1
        return _sales

    # Doing Shop Calculate
    def get_capital_sales_expenses(self):
        handle = self.conn.cursor()
        capital = handle.execute('''SELECT shop_init_capital FROM shopconfig''')
        if capital.fetchone() == None:
            self.capital = str(0)
        else:
            self.capital = str(capital.fetchone()[0])

        total_expenses_sql = handle.execute('''SELECT cost FROM Owners_Expenses''')
        self.total_expenses = 0
        total_expense = total_expenses_sql.fetchall()
        for expenses in total_expense:
            self.total_expenses += int(expenses[0])

        selling_cost_sql = handle.execute('''SELECt * FROM sales_order LEFT JOIN Products ON sales_order.productID=Products.ID ''')
        self.total_sellings_cost = 0
        self.total_unit_cost = 0
        total_selling = selling_cost_sql.fetchall()
        for selling_cost in total_selling:
            self.total_sellings_cost += selling_cost[4]
            self.total_unit_cost += (selling_cost[10] * selling_cost[3])

            self.current_income = self.total_sellings_cost - self.total_unit_cost


        #profit calculation, without initial capital
            self.current_profit = self.current_income - self.total_expenses


        # Screen Income/ capital
        total_selling = str(self.total_sellings_cost)
        total_unit_cost = str(self.total_unit_cost)
        current_income = str(self.current_income)
        current_profit = str(self.current_profit)
        total_expenses = str(self.total_expenses)

        screen_capital = self.ids.scrn_capitals
        detail = Label(text=self.capital, markup=True)
        screen_capital.add_widget(detail)

        screen_unit_cost = self.ids.scrn_total_cost_units
        detail = Label(text=total_unit_cost)
        screen_unit_cost.add_widget(detail)

        screen_sales = self.ids.scrn_total_sales
        detail = Label(text=total_selling)
        screen_sales.add_widget(detail)

        screen_income = self.ids.scrn_current_incomes
        detail = Label(text=current_income)
        screen_income.add_widget(detail)

        screen_profit = self.ids.scrn_current_profits
        detail = Label(text=current_profit)
        screen_profit.add_widget(detail)

        screen_expenses = self.ids.scrn_total_expenses
        detail = Label(text=total_expenses)
        screen_expenses.add_widget(detail)

    def change_screen(self, instance):
        # Page Title change with below line
        self.page_title.text =instance.text

        if instance.text == 'Manage User':
            self.ids.scrn_mnger.current = 'scrn_manage_user'
        elif instance.text == 'Manage Products':
            self.ids.scrn_mnger.current = 'scrn_manage_product'
        elif instance.text =='View Sales':
            self.ids.scrn_mnger.current = 'scrn_all_sales'

        elif instance.text == 'View Stock':
            self.ids.scrn_mnger.current = 'scrn_all_stock'
        elif instance.text == 'Shop Config Setting':
            self.ids.scrn_mnger.current = 'scrn_shop_config'
        elif instance.text  == 'View Customers':
            self.ids.scrn_mnger.current = 'scrn_all_customers'
        elif instance.text == 'Manage Expenditure':
            self.ids.scrn_mnger.current = 'scrn_all_expenses'


class admindashboardApp(App):
    def build(self):
        return admindashboardwindow()

if __name__ == '__main__':
    admindashboardApp().run()
