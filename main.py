from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import qdarkstyle
import sys
import sqlite3
from functools import partial
from appresources import encrypt_password, update_table, settings, load_data_from_db



APP_NAME = "MyGPAmate"
ui,_ = loadUiType("MyGPAmate.ui")

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.current_semester = "First Semester"
        # self.current_level = "!00 Level"
        self.settings_data = self.load_settings()
        self.Handle_Ui_Changes()
        self.exectue_settings(self.settings_data)
        self.Handle_Button()
        self.load_profile()

    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()  # Close the application
            self.save_changes()
        else:
            event.ignore()  # Ignore the close event
    
    def save_changes(self):
        data = (1, "dark", "12", "test", self.comboBox_level.currentText(), self.comboBox_semester.currentText())
        save_data = settings("mygpamatedata.db")
        save_data.save_settings(data)
    
    def load_profile(self):
        profile = load_data_from_db("mygpamatedata.db", "users")
        profile_data = profile.load_data()
        
        self.lineEdit_set_username.setText(profile_data[3])
        self.lineEdit_set_firstname.setText(profile_data[1])
        self.lineEdit_set_lastname.setText(profile_data[2])
        self.lineEdit_set_email.setText(profile_data[5])
    
    
    
    def Handle_Ui_Changes(self):
        try:
            self.load_current_user_info()
            self.tabWidget_main.setCurrentIndex(3)
            self.tabWidget_main_app.setCurrentIndex(0)
            self.label_welcome.setText(f"{self.current_user_info[1]}")
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
        self.load_timeline_info()
        self.load_course_info()
        self.handle_combox_changes()
            
  
        
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
        self.pushButton_dark_theme.clicked.connect(partial(self.change_theme, "dark"))
        self.pushButton_light_theme.clicked.connect(partial(self.change_theme, "light"))
        self.pushButton_editprofile.clicked.connect(self.edit_profile)
        self.pushButton_savechanges.clicked.connect(self.save_profile_settings)
        
    def edit_profile(self):
        # Enable Save Changes Button
        self.pushButton_savechanges.setEnabled(True)
        
        
        # Enable LineEdit Changes
        self.lineEdit_set_username.setEnabled(True)
        self.lineEdit_set_firstname.setEnabled(True)
        self.lineEdit_set_lastname.setEnabled(True)
        self.lineEdit_set_email.setEnabled(True)
        
        # Disable Edit Profile Changes Button
        self.pushButton_editprofile.setEnabled(False)
        
    def save_profile_settings(self):
        # Enable Edit Profile Button
        self.pushButton_editprofile.setEnabled(True)
        
        
        new_username = self.lineEdit_set_username.text()
        new_firstname = self.lineEdit_set_firstname.text()
        new_lastname= self.lineEdit_set_lastname.text()
        new_email = self.lineEdit_set_email.text()
        
        self.conn = sqlite3.connect("mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        query = 'UPDATE users SET first_name=?, last_name=?, username=?, email=? WHERE user_id = 1'
        new = (new_firstname, new_lastname, new_username, new_email,)
        
        self.cur.execute(query, new)
        
        self.conn.commit()
        self.conn.close()
        
        
        # Disable LineEdit
        self.lineEdit_set_username.setEnabled(False)
        self.lineEdit_set_firstname.setEnabled(False)
        self.lineEdit_set_lastname.setEnabled(False)
        self.lineEdit_set_email.setEnabled(False)
        
        # Chane Name in Dashboard
        self.label_welcome.setText(f"{new_firstname}") 
        
        mg = QMessageBox.information(self, "Status", "Changes Saved Succesfully")
        
        # Disable Save Changes Button
        self.pushButton_savechanges.setEnabled(False)
        
        
    
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
            
            # Delete current user table
            self.conn = sqlite3.connect("mygpamatedata.db")
            self.cur = self.conn.cursor()
            
            query = "DELETE FROM currentuser"
            
            self.cur.execute(query)
            self.conn.commit()
            self.conn.close()
        elif result == QMessageBox.No:
            # Do nothing
            ...
            
    # Load settings from database
    def load_settings(self):
        info = settings("mygpamatedata.db")
        self.settings_row = info.load_data()

        if self.settings_row:
            id, theme, font_size, font_type, current_level, current_semester = self.settings_row
            return {
                'theme': theme,
                'font_size': font_size,
                'font_type': font_type, 
                "current_level": current_level,
                "current_semester": current_semester
            }
            
        else:
            return None  # Return None if the row is not found
    def load_timeline_info(self):
        self.comboBox_level.setCurrentText(self.settings_data["current_level"])
        self.comboBox_semester.setCurrentText(self.settings_data["current_semester"])
        self.refresh_table()
        



    # Execute settings
    def exectue_settings(self, data):
        # Get the current font size before changing the theme
        current_font = self.font()

        if data["theme"] == "dark":
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dark_stylesheet)
        else:
            # If the theme is not "dark," set an empty stylesheet to reset the theme.
            self.setStyleSheet("")

        # Set the font size back to the original value
        self.setFont(current_font)
        n = self.current_level.split()[0]
        m = self.current_semester.split()[0]
        
        
        self.current_course_table =  f"{n}{m}Semester"
    # Change theme function 
    def change_theme(self, theme:str):
        self.conn = sqlite3.connect('mygpamatedata.db')
        self.cursor = self.conn.cursor()

        # Retrieve settings from the database
        select_query = "UPDATE app_settings SET theme=? WHERE id = ?"
        row_id = 1  # The ID of the row 
        self.cursor.execute(select_query, (theme, row_id))
        self.conn.commit()  # Fetch a single row
        
        self.conn.close()
        
        # self.load_course_info()
        self.settings_data = self.load_settings()
        self.exectue_settings(self.settings_data)
            
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
            first_name = fine_tuned_userdata[1]
            self.id = fine_tuned_userdata[0]
            last_name = fine_tuned_userdata[2]
            email = fine_tuned_userdata[5]
            self.show_message_box("Login Status", "Login Succesful",QMessageBox.information, QMessageBox.Ok)
            self.tabWidget_main.setCurrentIndex(3)
            self.tabWidget_main_app.setCurrentIndex(0)
            self.create_current_user(fine_tuned_userdata)
            self.load_current_user_info()
            self.label_welcome.setText(f"{self.current_user_info[1]}") 
            self.lineEdit_username.setText("")
            self.lineEdit_password.setText("")  
        else: 
            QMessageBox.warning(self, 'Password Empty', 'Invalid Password or Username')
            self.lineEdit_username.setText("")   
            self.lineEdit_password.setText("")   
            
    # Create a current User
    def create_current_user(self, data):
        data = tuple(data[1:])
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
        data_handle = update_table("mygpamatedata.db", self.current_course_table, self.current_level, self.current_semester)
        data =  data_handle.load_course_from_database() 
        
        self.tableWidget_course_info.setRowCount(1)
        
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
        
        data_handle = update_table("mygpamatedata.db", self.current_course_table, "100", self.current_semester) 
        data_handle.save_courses_to_database(all_data)
        
        # Show Success message 
        self.show_message_box("MyGPAmate - Status", "Courses Added Succesfully", QMessageBox.information, QMessageBox.Ok)
    
    
    def handle_combox_changes(self):
        self.comboBox_level.currentTextChanged.connect(self.refresh_table)
        self.comboBox_semester.currentTextChanged.connect(self.refresh_table)
        
    def refresh_table(self):
        self.current_level = self.comboBox_level.currentText()
        self.current_semester = self.comboBox_semester.currentText()
        
        n = self.current_level.split()[0]
        m = self.current_semester.split()[0]
        
        
        self.current_course_table =  f"{n}{m}Semester"
        
        self.load_course_info()
       
        
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