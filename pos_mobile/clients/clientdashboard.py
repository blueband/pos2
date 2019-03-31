from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from collections import OrderedDict
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
import re
from kivy.lang.builder import Builder
from RouteSMS.core import RouteSMS
import random
from datetime import date
import hashlib

from DbUtils import dbconn
from utils.datatable import DataTable


Builder.load_file('clients/clientdashboard.kv')

class clientdashboardwindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = dbconn.con()
        self.page_title = self.ids.page_title
        self.product_quantity = ''
        self.crud_product_name = ''
        self.crud_product_quantity = ''
        self.order_product_cost = ''
        self.old_stock = ''
        self.sms_username = 'assakiinahsms'
        self.sms_password = 'sms12345'
        # Save all Shopping Cart for Current User
        self.cart = []
        self.qty = []
        self.total = 0.00
        self.product_total_cost = []
        self.customerid = ''
        self.productid = []
        self.get_sold_products()


        # ALL Stock Display Screen
        screen_all_products = self.ids.scrn_all_stock
        products = self.get_products()
        productstable = DataTable(table=products)

        screen_all_products.add_widget(productstable)



        # # ALL Sold Products  Display Screen
        screen_all_solds = self.ids.scrn_all_sales
        sold_products = self.get_sold_products()
        sold_products_table = DataTable(table=sold_products)
        screen_all_solds.add_widget(sold_products_table)



        # Order Page
        products_screen = self.ids.view_available_products
        product =self.get_available_products()
        producttable = DataTable(table=product)
        self.ids.view_available_products.add_widget(producttable)




    def add_orders_fields(self):
        target = self.ids.Operations_fields_orders
        target.clear_widgets()

        crud_product_name = TextInput(hint_text="Products Name", multiline=False)
        crud_product_quantity = TextInput(hint_text="Quantity",multiline=False,id='crud_product_quantity', on_text_validate=lambda x:self.order_validate_cart(crud_product_name.text,crud_product_quantity.text))

        target.add_widget(crud_product_name)
        target.add_widget(crud_product_quantity)


    def order_validate_cart(self,p_name, quantity):
        # Updating Global Variable
        self.crud_product_quantity = quantity
        self.crud_product_name = p_name


        # #target_screen_cart = self.ids.screen_order_cart_heading
        #
        # details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top':1})
        # target_screen_cart.add_widget(details)
        # target_screen_cart.clear_widgets()
        #
        # order_product_name = Label(text='Product Name', size_hint_x=2)
        # order_product_quantity = Label(text='Quantity', size_hint_x=2)
        # order_product_cost = Label(text='Product Cost', size_hint_x=2)
        #
        # details.add_widget(order_product_name)
        # details.add_widget(order_product_quantity)
        # details.add_widget(order_product_cost)


        # Get All Data From DB
        handle = self.conn.cursor()

        try:
            product_details = handle.execute('''SELECT * FROM Products WHERE p_name=?''', (p_name,))

        except:
            print('Product Not Match')

        product_details = product_details.fetchall()

        for _product in product_details:
            productid = _product[0]
            order_product_name = _product[1]
            order_product_cost = int(_product[4]) * int(quantity)
            order_product_low_stock = _product[5]



        # Get Customer ID
        self.customerid = self.get_customerid()


        # Get add all Cart
        self.total += float(order_product_cost)

        purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t'+str(self.total)

        preview = self.ids.order_preview
        prev_text = preview.text
        _prev = prev_text.find('`')
        if _prev > 0:
            prev_text = prev_text[:_prev]

        ptarget = -1
        for i, c in enumerate(self.cart):
            if c == p_name:
                ptarget = i

        if ptarget >= 0:
            quantity = self.qty[ptarget] + 1
            self.qty[ptarget] = quantity
            expr = '%s\t\tx\d\t' % (p_name)
            rexpr = p_name + '\t\tx' + str(quantity) + '\t'
            nu_text = re.sub(expr, rexpr, prev_text)
            preview.text = nu_text + purchase_total
        else:
            self.cart.append(p_name)
            self.qty.append(quantity)
            self.product_total_cost.append(order_product_cost)
            self.productid.append(productid)

            nu_preview = '\n'.join([prev_text, p_name + '\t\tx' + quantity + '\t\t' + str(order_product_cost), purchase_total])
            preview.text = nu_preview


        # Update User Cart
        target_cart = self.ids.screen_order_cart

        self.order_product_cost = order_product_cost


    def save_sales(self):

        handle = self.conn.cursor()

        p = zip(self.cart,self.qty, self.product_total_cost, self.productid)
        #print(self.cart)
        for i in p:
            new_transact = handle.execute('''INSERT INTO transact_table(transact_code)VALUES(?)''', (self.customerid,))

            last_transactid = new_transact.lastrowid

            new_sales = handle.execute('''INSERT INTO sales_order(productID, customerID, order_quantity, price, transactID)VALUES(?,?,?,?,?)''', (i[3], self.customerid, i[1], i[2], last_transactid))

            # Updating The new Stock
            old_stock = handle.execute("SELECT p_quantity from Products WHERE ID=?", (i[3],))
            old_stock = old_stock.fetchone()

            # We are substracting Order quantity of product from the old stock here
            new_stock = int(old_stock[0]) - int(i[1])

            self.stock_update(i[3], new_stock )

            # Send SMS Notification to the Shop Owner
            self.sms_notify(self.customerid, i[0], i[2])

        self.conn.commit()



    def saveExp(self):
        exp_date = date.today()

        exp_name = self.ids.exp_name.text
        exp_descript = self.ids.exp_descript.text
        exp_cost = self.ids.exp_cost.text

        handle = self.conn.cursor()
        exp_sql = handle.execute('''INSERT INTO Owners_Expenses(expenses, cost, description, exp_date)VALUES(?,?,?,?)''',(exp_name,exp_cost, exp_descript,exp_date))

        self.conn.commit()

        details = self.ids.exp_name
        details.clear_widgets()




    def stock_update(self, productid, newstock):
        handle =self.conn.cursor()

        update_query = handle.execute(
            '''UPDATE Products SET p_quantity=? WHERE ID=?''',
            (newstock, productid))



    def sms_notify(self, customerid, product_name, price):
        message = "'New Sales Occured, The following product', + str(product_name), + '\t\t', + 'valued ' + 'N' +price, +' was purchase with transaction code ' +customerid"

        send_sms = RouteSMS(self.sms_username, self.sms_password)
        send_sms.send_message('KWASU', '2348055322087', message)


    def get_orders(self, name, quantity ):
        _products = OrderedDict()
        _products['product_name'] = {}
        _products['product_quantity'] = {}
        _products['Total_cost'] = {}

        handle = self.conn.cursor()
        product_name = []
        product_quantity = []
        Total_cost = []

        products = handle.execute("SELECt p_name, p_quantity, p_selling_price FROM Products WHERE p_name=?", (name,))
        products = products.fetchall()
        for product in products:
            product_name.append(product[0])
            product_quantity.append(product[1])
            Total_cost.append(product[2])

        product_lenght = len(product_name)
        idx = 0
        while idx < product_lenght:
            _products['product_name'][idx] = product_name[idx]
            _products['product_quantity'][idx] = product_quantity[idx]
            _products['Total_cost'][idx] = (Total_cost[idx]*int(quantity))
            idx += 1
            self.cart.append(_products)

        return self.cart



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


    def get_available_products(self):
        _products = OrderedDict()
        _products['product_name'] = {}
        _products['product_quantity'] = {}
        _products['product_selling_cost'] = {}

        handle = self.conn.cursor()
        product_name = []
        product_quantity =[]
        product_selling_cost =[]
        products = handle.execute('SELECt p_name, p_quantity, p_selling_price FROM Products')
        products = products.fetchall()
        for product in products:
            product_name.append(product[0])
            product_quantity.append(product[1])
            product_selling_cost.append(product[2])



        product_lenght = len(product_name)
        idx = 0
        while idx < product_lenght:
            _products['product_name'][idx] = product_name[idx]
            _products['product_quantity'][idx] = product_quantity[idx]
            _products['product_selling_cost'][idx] = product_selling_cost[idx]
            idx += 1
        return _products


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


    def get_customerid(self):
        id = random.randint(1000,10000)

        customerid = 'PHTG'+str(id)

        return customerid



    def change_screen(self, instance):
        # Page Title change with below line
        self.page_title.text =instance.text

        if instance.text == 'Create Sales':
            self.ids.scrn_mnger.current = 'scrn_manage_order'

        elif instance.text == 'View Order':
            self.ids.scrn_mnger.current = 'scrn_view_order'

        elif instance.text =='View Sales':
            self.ids.scrn_mnger.current = 'scrn_all_sales'

        elif instance.text == 'View Available Stock':
            self.ids.scrn_mnger.current = 'scrn_all_stock'

        elif instance.text  == 'View Customers':
            self.ids.scrn_mnger.current = 'scrn_all_customers'

        elif instance.text == 'Record expenses':
            self.ids.scrn_mnger.current = 'scrn_all_expenses'


class clientdashboardApp(App):
    def build(self):
        return clientdashboardwindow()

if __name__ == '__main__':
    clientdashboardApp().run()
    # board = clientdashboardApp()
    # board.run()