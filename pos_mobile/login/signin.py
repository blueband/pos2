from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from DbUtils import dbconn, create_db_table
import os
from kivy.lang.builder import Builder
import hashlib

KV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'signin.kv'))
Builder.load_file(KV_PATH)


class signinwidows(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.StartTable()
        self.conn = dbconn.con()


    def StartTable(self):
        pass

    def validate_user(self):
        handle = self.conn.cursor()
        user = self.ids.username_field
        pwd = self.ids.password_field
        info = self.ids.info

        username = user.text
        password = pwd.text
        usernameset = dict()
        adminset = dict()
        user_data = handle.execute('''SELECT * FROM Rep_login''')
        for user in user_data.fetchall():
            usernameset[user[1]] =user[2]
        user_data = handle.execute('''SELECT * FROM Admin_login''')
        for user in user_data.fetchall():
            adminset[user[1]] =user[2]


        if username == '' or password == '':
            info.text = '[color=#FF0000]Either Username or Password Field is incorrect[/color]'  # This print to the GUI
        else:
            print('this is username : ', username, 'this is adminset : ',adminset)
            password = hashlib.sha256(password.encode()).hexdigest()
            print('this is username : ', username, 'password :', password)

            #Load new GUI after succesfully login
            if username not in (adminset and usernameset):

                info.text = '[color=#FFAABB]first time of running this App[/color]'

            elif username in adminset:
                # check and load admin section
                for repuser, reppwd in adminset.items():
                    if repuser == username and  reppwd == password:
                        info.text = '[color=#FFAABB]Login successfully[/color]'
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        info.text = '[color=#FFAABB]Incorrect Login details supply[/color]'

            elif username in usernameset:

                # check and load client page
                for repuser, reppwd in usernameset.items():
                    if repuser == username and reppwd == password:
                        info.text = '[color=#FFAABB]Login successfully[/color]'
                        self.parent.parent.current = 'scrn_client'
                    else:
                        info.text = '[color=#FFAABB]Incorrect Login details supply for the user[/color]'


class signinApp(App):
    def build(self):
        return signinwidows()

if __name__ == '__main__':
    signinApp().run()
