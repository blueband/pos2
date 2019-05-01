from  kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from DbUtils import dbconn
from collections import OrderedDict
conn = dbconn.con()


Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None, 250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            
<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos

''')

class DataTable(BoxLayout):
    def __init__(self, table = '', **kwargs):
        super().__init__(**kwargs)


        products = table
        # products = self.get_products()

        col_titles = [k for k in products.keys()]
        rows_lenght = len(products[col_titles[0]])

        self.columns = len(col_titles)
        table_data = []
        for title in col_titles:
            table_data.append({'text':str(title),'size_hint_y':None, 'height':50, 'bcolor':(.769,.604,.286, 1)})

        for row in range(rows_lenght):
            for title in col_titles:
                table_data.append({'text':str(products[title][row]), 'size_hint_y':None, 'height':30, 'bcolor':(.769,.604,.286, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data

'''
    def get_products(self):
        _products = OrderedDict()
        _products['product_name'] = {}
        _products['product_quantity'] = {}
        _products['product_unit_cost'] = {}
        _products['product_selling_cost'] = {}
        _products['stock_low_alert'] = {}

        handle = conn.cursor()
        product_name = []
        product_quantity = []
        product_unit_cost = []
        product_selling_cost = []
        stock_low_alert = []
        products = handle.execute('SELECt * FROM Products')
        products = products.fetchall()
        for product in products:
            product_name.append(product[1])
            product_quantity.append(product[2])
            product_unit_cost.append(product[3])
            product_selling_cost.append(product[4])
            stock_low_alert.append(product[4])

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
'''
'''
class DataTableApp(App):
    def build(self):
        return DataTable()

if __name__ == '__main__':
    table = DataTableApp()
    table.run()

'''