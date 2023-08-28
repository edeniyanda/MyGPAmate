from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import qdarkstyle
import sys
import sqlite3
from functools import partial
from appresources import encrypt_password



APP_NAME = "MyGPAmate"
ui,_ = loadUiType("MyGPAmate.ui")

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dark_stylesheet)
        self.Handle_Ui_Changes()
        self.Handle_Button()
        self.lineEdit_username.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_password.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_user_name_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_first_name_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_last_name_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_email_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_password_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        self.lineEdit_confirm_password_2.returnPressed.connect(self.move_focus_to_next_line_edit)
        
        

            
        
    def Handle_Ui_Changes(self):
        try:
            self.load_current_user_info()
            self.tabWidget_main.setCurrentIndex(3)
            self.tabWidget_main_app.setCurrentIndex(0)
            self.label_welcome.setText(f"Welcome Back, {self.current_user_info[1]}")
        except:  
            self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_main_app.tabBar().setVisible(False)
        for i in range(2):
            if i == 0:
                self.tableWidget_course_info.setColumnWidth(i, 500)
                ...
            elif i == 1:
                self.tableWidget_course_info.setColumnWidth(i, 100)
            elif i == 2:
                self.tableWidget_course_info.setColumnWidth(i, 50)
        self.tableWidget_course_info.insertRow(0)
        self.load_course_info()
        # self.comboBox_faculty.currentTextChanged.connect(self.faculty_changed)
            
    # def faculty_changed(self, faculty):
    #     self.comboBox_department.clear()

    #     if faculty == "Faculty of Natural and Applied Science":
    #         self.department_combo.addItems(["Applied Physics", "Computer Science", "Chemistry"])
    #         self.course_combo.addItems(["Physics 101", "Intro to Programming", "Chemistry Basics"])
    #     elif faculty == "Faculty of Social Sciences":
    #         self.department_combo.addItems(["Psychology", "Economics", "Sociology"])
    #         self.course_combo.addItems(["Psych 101", "Microeconomics", "Introduction to Sociology"])
      
            
        
    def Handle_Button(self):
        self.pushButton_get_started.clicked.connect(partial(self.change_welcome_widget_index, 1))        
        self.pushButton_dash_board.clicked.connect(partial(self.change_main_app_widget, 0))
        self.pushButton_courses.clicked.connect(partial(self.change_main_app_widget, 1))
        self.pushButton_grade.clicked.connect(partial(self.change_main_app_widget, 2))
        self.pushButton_profile.clicked.connect(partial(self.change_main_app_widget, 3))
        self.pushButton_settings.clicked.connect(partial(self.change_main_app_widget, 4))
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_create_account_2.clicked.connect(self.create_account)
        self.commandLinkButton_already_have_an_account.clicked.connect(partial(self.change_welcome_widget_index, 1))
        self.commandLinkButton_create_account.clicked.connect(partial(self.change_welcome_widget_index, 2))
        self.pushButton_add_new_courses.clicked.connect(self.add_courses)
        self.pushButton_save_changes.clicked.connect(self.save_courses)
        self.pushButton_log_out.clicked.connect(self.log_out)
        ...    
    # Log out function
    def log_out(self):
        mg = QMessageBox()
        mg.setWindowTitle(f"{APP_NAME} - Log Out?")
        mg.setText("Are you sure you want to Log out?")
        mg.setIcon(QMessageBox.Question)
        mg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = mg.exec_()

        if result == QMessageBox.Yes:
            # Go back to welcome Screen
            self.tabWidget_main.setCurrentIndex(0)
        elif result == QMessageBox.No:
            # Do nothing
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
            fine_tuned_userdata = list(userdata)
            print(fine_tuned_userdata)
            first_name = fine_tuned_userdata[1]
            self.id = fine_tuned_userdata[0]
            last_name = fine_tuned_userdata[2]
            email = fine_tuned_userdata[5]
            self.show_message_box("Login Status", "Login Succesful",QMessageBox.information, QMessageBox.Ok)
            self.tabWidget_main.setCurrentIndex(3)
            self.tabWidget_main_app.setCurrentIndex(0)
            self.create_current_user(fine_tuned_userdata)
            self.load_current_user_info()
            self.label_welcome.setText(f"Welcome Back, {self.current_user_info[1]}")   
        else: 
            QMessageBox.warning(self, 'Password Empty', 'Invalid Password or Username')
            self.lineEdit_username.setText("")   
            self.lineEdit_password.setText("")   
            
    # Create a current User
    def create_current_user(self, data):
        data = tuple(data[1:])
        print(data)
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        query = '''CREATE TABLE IF NOT EXISTS "currentuser" (
                        "user_id"	INTEGER NOT NULL,
                        "first_name"	TEXT NOT NULL,
                        "last_name"	TEXT NOT NULL,
                        "username"	INTEGER NOT NULL,
                        "password"	TEXT NOT NULL,
                        "email"	TEXT NOT NULL,
                        "college_name"	TEXT NOT NULL,
                        PRIMARY KEY("user_id" AUTOINCREMENT)
                    );'''
        
        self.cur.execute(query)
        self.conn.commit()
        
        self.cur.execute("INSERT INTO currentuser (first_name, last_name, username, password, email, college_name) VALUES (?,?,?,?,?,?)", data)
        
        self.conn.commit()
        
        self.conn.close()
        
    # Load Current User Information
    def load_current_user_info(self):
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        query = "SELECT * FROM currentuser"
        
        self.cur.execute(query)
        
        self.current_user_info = self.cur.fetchone()
        
        self.conn.commit()
        self.conn.close()
        
        
        
        
        
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
            if not(len(i)):
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
        
        
    def move_focus_to_next_line_edit(self):
        current_line_edit = self.focusWidget()

        # Find the next line edit using tab order
        next_tab_order = self.focusNextChild()

        if next_tab_order:
            next_tab_order.setFocus(Qt.TabFocusReason)
        else:
            self.lineEdit_username.setFocus(Qt.TabFocusReason)  # Wrap around to the first line edit
    # Add new courses
    def add_courses(self):
        course_title = self.lineEdit_course_title.text()
        course_code = self.lineEdit_course_code.text()
        course_unit = self.spinBox_course_unit.value()  # Used value() to get the integer value from spinBox
        
        course_info = {
            course_code : [course_title, course_code, str(course_unit)]
        }

        row = self.tableWidget_course_info.rowCount()
        
        dec = [self.lineEdit_course_title, self.lineEdit_course_code, self.spinBox_course_unit]
        
        main_info = course_info[course_code]
        
        for i in main_info:
            try:
                int(i)
                QMessageBox.critical(self, "Invalid Input", f"{dec[main_info.index(i)].placeholderText()} Cannot be an Integer")
                return 
            except:
                ...
            if not i:
                QMessageBox.critical(self, "Invalid Details", f"{dec[main_info.index(i)].placeholderText()} Cannot be Empty")
                return
            elif i == "0" and i == str(course_unit):
                QMessageBox.critical(self, "Invalid Details", f"Course Unit Cannot be 0")
                return
            
        
        # if not (all([error for error in course_info[course_code]])):
        #     QMessageBox.critical(self, "Invalid Details", f"Field(s) Cannot be Empty")
        #     return
        
            
            
        
        if row > 15:
            QMessageBox.critical(self, "Eror 404", "Courses Cannot Exceed !5")
            return
        else:
            self.tableWidget_course_info.insertRow(row - 1)
            
        
        for i in range(3):
            self.tableWidget_course_info.setItem(row -1 , i, QTableWidgetItem(course_info[course_code][i]))

        
    
    def load_course_info(self):
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        query = "SELECT * FROM course_info"
        
        self.cur.execute(query)
        
        data = self.cur.fetchall()
        
        if data:
            for i in range(len(data)):
                fine_data = data[i]
                new_fine_data = list(fine_data[1:])
                for j in range(len(new_fine_data)):
                    item = QTableWidgetItem(str(new_fine_data[j]))
                    self.tableWidget_course_info.setItem(i, j, item)
                row_position = self.tableWidget_course_info.rowCount()
                self.tableWidget_course_info.insertRow(row_position)
    
    def save_courses(self):
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        num_row = self.tableWidget_course_info.rowCount()
        num_col = self.tableWidget_course_info.columnCount()
        
        all_data = []
        for row in range(num_row):
            if row == num_row - 1:
                break
            course_data = []
            for col in range(num_col):
                item = self.tableWidget_course_info.item(row, col)
                course_data.append(item.text())
            all_data.append(tuple(course_data))
        if len(all_data) == 0:
            QMessageBox.critical(self, "Error", "Courses Cannot Be Empty")
            return
            
        
        self.cur.execute("DELETE FROM 'course_info'")
        self.conn.commit()  
           
        for data in all_data:
            query = "INSERT INTO 'course_info' (course_title, course_code, course_unit) VALUES (?,?,?)"
            self.cur.execute(query, data)
            self.conn.commit()
                     
        self.conn.close()
        
        self.show_message_box("MyGPAmate - Status", "Courses Added Succesfully", QMessageBox.information, QMessageBox.Ok)
        
        
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
       