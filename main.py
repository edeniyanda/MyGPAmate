from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import qdarkstyle
import sys
import sqlite3
from functools import partial
from appresources import encrypt_password

ui,_ = loadUiType("MyGPAmate.ui")

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dark_stylesheet)
        self.Handle_Ui_Changes()
        self.Handle_Button()
        
        
        
        
    def Handle_Ui_Changes(self):
        self.tabWidget_main.setCurrentIndex(3)
        self.tabWidget_main_app.setCurrentIndex(0)
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_main_app.tabBar().setVisible(False)
        
    def Handle_Button(self):
        self.pushButton_get_started.clicked.connect(partial(self.change_welcome_widget_index, 2))        
        self.pushButton_dash_board.clicked.connect(partial(self.change_main_app_widget, 0))
        self.pushButton_courses.clicked.connect(partial(self.change_main_app_widget, 1))
        self.pushButton_grade.clicked.connect(partial(self.change_main_app_widget, 2))
        self.pushButton_profile.clicked.connect(partial(self.change_main_app_widget, 3))
        self.pushButton_settings.clicked.connect(partial(self.change_main_app_widget, 4))
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_create_account_2.clicked.connect(self.create_account)
        ...    
    
    # Change Main Widget 
    def change_welcome_widget_index(self, index_position:int):
        self.tabWidget_main.setCurrentIndex(index_position)
        
    # Change Main Application Widget
    def change_main_app_widget(self, index_position:int):
        self.tabWidget_main_app.setCurrentIndex(index_position)
        
    # Login    
    def login(self):
        entered_user_name = self.lineEdit_username.text()
        entered_password = self.lineEdit_password.text()
        entered_password = encrypt_password(entered_password)
         
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
            
        query = "SELECT * FROM users WHERE username= ? AND password = ?"
            
        self.cur.execute(query, (entered_user_name, entered_password,))
            
        userdata = self.cur.fetchone()
        if userdata:
            print(userdata)
            fine_tuned_userdate = list(userdata)
            first_name = fine_tuned_userdate[1]
            last_name = fine_tuned_userdate[2]
            email = fine_tuned_userdate[5]
            self.show_message_box("Login Status", "Login Succesful",QMessageBox.information, QMessageBox.Ok)
            self.tabWidget_main.setCurrentIndex(1)
            self.label_welcome.setText(f"Welcome Back, {first_name}")
            
        else: 
            self.show_message_box("Login Status", "Invalid Username or Password",QMessageBox.information, QMessageBox.Ok)
            self.lineEdit_username.setText("")   
            self.lineEdit_password.setText("")   
            
        
    def create_account(self):
        username = self.lineEdit_user_name_2.text()
        first_name = self.lineEdit_first_name_2.text()
        last_name = self.lineEdit_last_name_2.text()
        email = self.lineEdit_email_2.text()
        password = self.lineEdit_password_2.text()
        confirm_password = self.lineEdit_confirm_password_2.text()
        college_name = self.comboBox_college_name_2.currentText()

        data = (first_name, last_name, username, password, email, college_name)
        
        for i in data:
            if len(i) == 0:
                QMessageBox.warning(self, 'Details Error', 'Details incomplete.')
                return
        
        if not(len(password)):
            QMessageBox.warning(self, 'Password Empty', 'Password should be 8 characters.')
            return
            
        # Check if passwords match
        if (password != confirm_password):
            QMessageBox.warning(self, 'Password Mismatch', 'Passwords do not match.')
            return
        else:
            password = encrypt_password(password)

        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cursor = self.conn.cursor()
        

        # Insert user data into the database
        try:
            self.cursor.execute('''INSERT INTO users (first_name, last_name, username, password, email, college_name)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (first_name, last_name, username, password, email, college_name))
            self.conn.commit()
            QMessageBox.information(self, 'Account Created', 'Your account has been created successfully.')
            self.tabWidget_main.setCurrentIndex(2)
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

        self.conn.close()
    def show_message_box(self, title, text, icon, buttons=QMessageBox.Ok | QMessageBox.Cancel):
        mg = QMessageBox()
        mg.setWindowTitle(title)
        mg.setText(text)
        mg.setIcon=(icon)   
        mg.setStandardButtons(buttons) 
        mg.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    
    
if __name__ == "__main__":
    main()
       