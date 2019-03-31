from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from admin.admindashboard import admindashboardwindow
from login.signin import signinwidows
from clients.clientdashboard import clientdashboardwindow

class mainwindow(BoxLayout):

    admin_widget = admindashboardwindow()
    signin_widget = signinwidows()
    operator_widget = clientdashboardwindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_signin.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_client.add_widget(self.operator_widget)

class mainApp(App):
    def build(self):

        return mainwindow()

if __name__=='__main__':
    mainApp().run()