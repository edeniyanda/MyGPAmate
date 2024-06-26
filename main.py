from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.uic import loadUiType
import qdarkstyle
import sys
import sqlite3
from functools import partial
from appresources import encrypt_password, update_table, settings, load_data_from_db, edittable, convert_score_to_grade, GPAPlotter



APP_NAME = "MyGPAmate"
ui,_ = loadUiType("MyGPAmate.ui")

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(1327, 694)
        self.setupUi(self)
        self.default_values()
        self.settings_data = self.load_settings()
        self.initial_current_theme = self.settings_data["theme"]
        self.Handle_Ui_Changes()
        self.exectue_settings(self.settings_data)
        self.Handle_Button()
        self.load_profile()
        self.set_graph()
        if self.tabWidget_main.currentIndex() == 3:
            self.statusofall()
        
        # Use QVBoxLayout to add the Matplotlib canvas to the QFrame
        layout = QVBoxLayout(self.graph_frame)
        layout.addWidget(self.canvas)
        try:
            self.update_matplotlib_plot()
        except:
            ...
    def set_graph(self):
        # Create a Matplotlib figure and canvas
            self.fig, self.ax = plt.subplots(figsize=(8, 5))
            self.canvas = FigureCanvas(self.fig)

    def statusofall(self):
        rowCount = self.tableWidget_grade.rowCount()
        if rowCount <=1:
            self.statusBar().showMessage("📌Go to My Course to add Courses📌 ")
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
            
    def Handle_Ui_Changes(self):
        self.load_grade_grader()
        try:
            self.load_current_user_info()
            self.tabWidget_main.setCurrentIndex(3)
            self.tabWidget_main_app.setCurrentIndex(0)
        except:  
            self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_main_app.tabBar().setVisible(False)
        for i in range(2):
            if i == 0:
                self.tableWidget_course_info.setColumnWidth(i, 500)
            elif i == 1:
                self.tableWidget_course_info.setColumnWidth(i, 100)
            elif i == 2:
                self.tableWidget_course_info.setColumnWidth(i, 50)
                
        self.tableWidget_grade.setColumnWidth(0, 380)
        self.tableWidget_course_info.insertRow(0)
        self.load_timeline_info()
        self.load_course_info()
        self.current_grade_table = self.current_course_table
        self.load_grade_info()
        self.handle_combox_changes()
        self.getgpas()


        
    def calculategpa(self):
        num_row = self.tableWidget_grade.rowCount()
        try: 
            for i in range(num_row):
                quality_point = str(int(self.tableWidget_grade.item(i, 2).text()) * int(self.tableWidget_grade.item(i, 5).text()))
                self.tableWidget_grade.setItem(i, 6, QTableWidgetItem(quality_point))
            sum_qp = 0    
            for i in range(num_row):
                sum_qp += int(self.tableWidget_grade.item(i, 6).text())
                self.label_eqp.setText(str(sum_qp))
            sum_cu = 0  
            for i in range(num_row):
                sum_cu += int(self.tableWidget_grade.item(i, 2).text())
                self.label_ecu.setText(str(sum_cu))
                
            gpa = round(sum_qp / sum_cu, 2)
            
            self.label_gpa.setText(str(gpa))
        except:
            self.label_gpa.setText("0")
            
        # Update the Matplotlib plot with the GPA data
        # self.update_matplotlib_plot()
        
    def load_grade_grader(self):
        gradeinst = load_data_from_db("assets/mygpamatedata.db", "GradeGrader")
        data = gradeinst.load_data_for_grade()

        self.tableWidget_grader.setRowCount(1)
        
        for i in range(len(data)):
            row_data = data[i][1:]
            for j in range(len(row_data)):
                item_to_add = QTableWidgetItem(row_data[j]) 
                self.tableWidget_grader.setItem(i, j , item_to_add)
            row_pos = self.tableWidget_grader.rowCount()
            if row_pos != len(data):
                self.tableWidget_grader.insertRow(row_pos)
            
        # Set all columns as uneditable initially
        self.tableWidget_grader.setEditTriggers(QTableWidget.NoEditTriggers)
                  
    def default_values(self):
        self.semesters = ["100L 1st", "100L 2nd", "200L 1st", "200L 2nd", "300L 1st", "300L 2nd", "400L 1st", "400L 2nd"]
        self.current_level = "100 Level"
        self.current_semester = "First Semester"
        
        n = self.current_level.split()[0]
        m = self.current_semester.split()[0]
        self.current_course_table =  f"{n}{m}Semester"
            
        self.current_grade_level = "100 Level"
        self.current_grade_semester = "First Semester"
    
        n = self.current_grade_level.split()[0]
        m = self.current_grade_semester.split()[0]
        self.current_grade_table =  f"{n}{m}Semester"
        
    def getgpas(self):
        gpas_getter =  {"100 Level" : ["First Semester", "Second Semester"],
                             "200 Level" : ["First Semester", "Second Semester"],
                             "300 Level" : ["First Semester", "Second Semester"],
                             "400 Level" : ["First Semester", "Second Semester"]
                        }
        self.gpas = []
        
        
        prev_semester = self.comboBox_semester.currentText()
        prev_level = self.comboBox_level.currentText()
        
        for i in gpas_getter.keys():
            self.comboBox_level.setCurrentText(i)
            for j in range(2):
                self.comboBox_semester.setCurrentText(gpas_getter[i][j])
                gpa = float(self.label_gpa.text())
                self.gpas.append(gpa)
                
        
        sum_all_cu = 0
        sum_all_qp = 0
        for i in gpas_getter.keys():
            self.comboBox_level.setCurrentText(i)
            for j in range(2):
                self.comboBox_semester.setCurrentText(gpas_getter[i][j])
                sum_all_cu  += int(self.label_ecu.text())
                sum_all_qp += int(self.label_eqp.text())
        try:
            self.cgpa = round(sum_all_qp/ sum_all_cu, 2)
            self.label_CGPA.setText(str(self.cgpa))
                
            self.comboBox_level.setCurrentText(prev_level)
            self.comboBox_semester.setCurrentText(prev_semester)
        except:
            ...
        
    
        

    def save_changes(self):
        data = (1, self.initial_current_theme, "12", "test", self.comboBox_level.currentText(), self.comboBox_semester.currentText())
        save_data = settings("assets/mygpamatedata.db")
        save_data.save_settings(data)
    
    def load_profile(self):
        profile = load_data_from_db("assets/mygpamatedata.db", "users")
        
        profile_data = profile.load_data()
        if profile_data is None:
            return
        self.label_welcome.setText(f"{profile_data[1]}")
        self.lineEdit_set_username.setText(profile_data[3])
        self.lineEdit_set_firstname.setText(profile_data[1])
        self.lineEdit_set_lastname.setText(profile_data[2])
        self.lineEdit_set_email.setText(profile_data[5])
        

        # self.tableWidget_course_info.itemSelectionChanged.connect(self.update_button_state)
        
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
        self.pushButton_delete_course.clicked.connect(self.delete_course)
        self.pushButton_edit_grade.clicked.connect(self.edit_grade)
        self.pushButton_save_grade_changes.clicked.connect(self.save_grade_changes)
        self.pushButton_estimate_grade.clicked.connect(self.estimate_grade)
        self.pushButton_edit_unit.clicked.connect(self.edit_grader)
        self.pushButton_save_unit_change.clicked.connect(self.save_grader)   
        self.pushButton_set_to_default.clicked.connect(self.set_grader_to_default)
        self.pushButton_clacuategpa.clicked.connect(self.calculategpa)
        self.pushButton_plot.clicked.connect(self.update_matplotlib_plot)
        self.pushButton_h1.clicked.connect(partial(self.hideAndShowPressed, self.pushButton_h1, self.lineEdit_password_2))
        self.pushButton_h2.clicked.connect(partial(self.hideAndShowPressed, self.pushButton_h2, self.lineEdit_confirm_password_2))
        self.pushButton_h3.clicked.connect(partial(self.hideAndShowPressed, self.pushButton_h3, self.lineEdit_password))

        
        
    def set_grader_to_default(self):
        default_data = [['A', '5'], ['B', '4'], ['C', '3'], ['D', '2'], ['E', '1'], ['F', '0']]
        
        num_row = self.tableWidget_grader.rowCount()
        num_col = self.tableWidget_grader.columnCount()
        
        for i in range(num_row):
            for j in range(2):
              self.tableWidget_grader.setItem(i, j, QTableWidgetItem(default_data[i][j])) 
              
        num_row = self.tableWidget_grader.rowCount()
        num_col = self.tableWidget_grader.columnCount()
        

        grade_data = []
        for i in range(num_row):
            row_data = []
            for j in range(num_col):
                grade_item = self.tableWidget_grader.item(i, j)
                row_data.append(grade_item.text())
            grade_data.append(row_data)
        grade_data = tuple(grade_data)
        data = load_data_from_db("assets/mygpamatedata.db", "GradeGrader",  grade_data)
        data.save_data_to_grader()
        try:
            self.estimate_grade()
            self.calculategpa()    
            self.refresh_gpa_com()
        except:
            ...
        QMessageBox.information(self,
                    "MyGPAmate Grader",
                    "Grader Table restored back \nto default Sucesfully",
                    QMessageBox.Ok)
              
               
            
    def save_grader(self):
        num_row = self.tableWidget_grader.rowCount()
        num_col = self.tableWidget_grader.columnCount()
        

        grade_data = []
        for i in range(num_row) :
            row_data = []
            for j in range(num_col):
                grade_item = self.tableWidget_grader.item(i, j)
                if j == 3:
                    try:   
                        int(grade_item)
                    except:
                        QMessageBox.critical(self,
                                    "MyGPAmate Grader",
                                    "Grade Cannot be empty",
                                    QMessageBox.Ok)
                row_data.append(grade_item.text())
            grade_data.append(row_data)
        grade_data = tuple(grade_data)
        data = load_data_from_db("assets/mygpamatedata.db", "GradeGrader",  grade_data)
        data.save_data_to_grader()
        QMessageBox.information(self,
                    "MyGPAmate Grader",
                    "Grader Table Updated Sucesfully",
                    QMessageBox.Ok)
        try:
            self.estimate_grade()
            self.calculategpa()    
            self.refresh_gpa_com()
        except:
            ...
        
    def edit_grader(self):
        get_response = QMessageBox.critical(self, 
                                            "Warning", 
                                            "Are you sure you want to edit the Grade Unit?",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
    
        if get_response == QMessageBox.Yes:
            delegate = edittable.MyDelegate2()
            self.tableWidget_grader.setItemDelegate(delegate)
            # Allow editing for specific columns (e.g., column 3)
            self.tableWidget_grader.setEditTriggers(QTableWidget.DoubleClicked)  # or any other desired trigger
            self.statusBar().showMessage("🔥You can now edit Grader")
        else:
            ...
    
    def estimate_grade(self):
        num_row = self.tableWidget_grade.rowCount()
        scores = []
        if num_row ==  0:
            ...
        else:
            for i in range(num_row):
                try:
                    score = int(self.tableWidget_grade.item(i, 3).text())
                    if score > 100 or score < 0:
                        QMessageBox.critical(self,
                                        "MyGPAmate",
                                        "Score should be in the range 0 -100")
                        return
                    scores.append(score)
                except:
                    QMessageBox.critical(self,
                                    "MyGPAmate",
                                    "Score cannot Empty")
                    return 
            grade_list_object = convert_score_to_grade(scores)
            grade_list = grade_list_object.convert()
            
            try:
                for i in range(num_row):
                    grade_to_add = QTableWidgetItem(str(grade_list[i]))
                    self.tableWidget_grade.setItem(i, 4, grade_to_add)
                    
  
                gradeinst = load_data_from_db("assets/mygpamatedata.db", "GradeGrader")
                data = gradeinst.load_data_for_grade()
                grader_dict = {}
                for i in data:
                    grade, value = i[1], i[2]
                    grader_dict[grade] = value
                    
                for i in range(num_row):
                    grade_val = self.tableWidget_grade.item(i, 4).text()
                    grade_point = QTableWidgetItem(grader_dict[grade_val])
                    self.tableWidget_grade.setItem(i, 5, grade_point)
                    ...
            except:
                ...
            # QMessageBox.information(self,
            #             "MyGPAmate",
            #      `       "Graded Successfully")
    def refresh_gpa_com(self):
        self.estimate_grade()
        self.calculategpa()
        self.getgpas()
        self.update_matplotlib_plot()
        
        
    def save_grade_changes(self):
        num_row = self.tableWidget_grade.rowCount()
        if num_row <= 0:
            QMessageBox.information(
                self,
                "Invalid",
                "Add a Course to Save"
            )
            return 
        all_data = []
        for i in range(num_row):
            grade_data = []
            for j in range(4):
                itemtoadd = self.tableWidget_grade.item(i, j)
                if j == 3:
                    try:
                        itemtoadd = itemtoadd.text()
                        if len(itemtoadd) == 0:
                            QMessageBox.critical(self,
                                    "Error",
                                    "Invalid Score input")
                            return
                    except:
                        QMessageBox.critical(self,
                                    "Error",
                                    "Invalid Score input")
                        return
                    try:
                        int(itemtoadd)
                        grade_data.append(itemtoadd)
                    except:
                        QMessageBox.critical(self,
                                    "Error",
                                    "Score cannot be a String")
                        return
                else:
                    itemtoadd = itemtoadd.text()
                    grade_data.append(itemtoadd)
                     
            all_data.append(tuple(grade_data))  
            
        data_handle = update_table("assets/mygpamatedata.db", self.current_grade_table, self.current_grade_level, self.current_grade_semester) 
        data_handle.save_grade_to_database(all_data)
        self.refresh_gpa_com()
        QMessageBox.information(self,
                                "MyGPAmate - Grade",
                                "Grade Saved Succesfully",
                                )
        self.statusBar().showMessage("")
        
    def edit_grade(self):
        if self.pushButton_edit_grade.text() == "Edit Mode":
            message = QMessageBox.information(
                self,
                "MyGPPAmate - Grade",
                "You are now in Edit Mode, \nYou can edit your Score"
            )
            self.statusBar().showMessage("🔥You are in Edit Mode")
            self.pushButton_edit_grade.setText("Read Only Mode")
            # Set the item delegate for the table
            delegate = edittable.MyDelegate()
            self.tableWidget_grade.setItemDelegate(delegate)
            # Allow editing for specific columns (e.g., column 3)
            self.tableWidget_grade.setEditTriggers(QTableWidget.DoubleClicked)  # or any other desired trigger
        else:
            # Set all columns as uneditable initially
            self.tableWidget_grade.setEditTriggers(QTableWidget.NoEditTriggers)
            message = QMessageBox.information(
                self,
                "MyGPPAmate - Grade",
                "You are now back in Read\n Only Mode"
            )
            self.statusBar().showMessage("🔥You are in Read Only Mode")
            self.pushButton_edit_grade.setText("Edit Mode")


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
        
        self.conn = sqlite3.connect("assets/mygpamatedata.db")
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
            # Delete current user table
            self.conn = sqlite3.connect("assets/mygpamatedata.db")
            self.cur = self.conn.cursor()
            
            query = "DELETE FROM currentuser"
            self.cur.execute(query)
            self.conn.commit()
            self.conn.close()
            
            # Go back to welcome Screen
            self.tabWidget_main.setCurrentIndex(0)
            
        elif result == QMessageBox.No:
            # Do nothing
            ...
            
    # Load settings from database
    def load_settings(self):
        info = settings("assets/mygpamatedata.db")
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
        self.refresh_table("Courses")

    # Execute settings
    def exectue_settings(self, data):
        # Get the current font size before changing the theme
        current_font = self.font()

        if data["theme"] == "dark":
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dark_stylesheet)   
            plt.style.use("dark_background")
            self.set_graph()
            self.update_matplotlib_plot()
        else:
            # If the theme is not "dark," set an empty stylesheet to reset the theme.
            self.setStyleSheet("")
            plt.style.use("default")
            self.set_graph()
            self.update_matplotlib_plot()

        # Set the font size back to the original value
        self.setFont(current_font)
        n = self.current_level.split()[0]
        m = self.current_semester.split()[0]
        
        
        self.current_course_table =  f"{n}{m}Semester"
    # Change theme function 
    def change_theme(self, theme:str):
        self.initial_current_theme = theme
        self.conn = sqlite3.connect('assets/mygpamatedata.db')
        self.cursor = self.conn.cursor()

        # Retrieve settings from the database
        select_query = "UPDATE app_settings SET theme=? WHERE id = ?"
        row_id = 1  # The ID of the row 
        self.cursor.execute(select_query, (theme, row_id))
        self.conn.commit()  # Fetch a single row
        
        self.conn.close()
    
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
         
        self.conn = sqlite3.connect("assets/mygpamatedata.db")
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
            
        self.load_profile()
        self.statusofall()
            
    # Create a current User
    def create_current_user(self, data):
        data = tuple(data[1:])
        self.conn = sqlite3.connect("assets/mygpamatedata.db")
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
        self.conn = sqlite3.connect("assets/mygpamatedata.db")
        self.cur = self.conn.cursor()
        
        query = "SELECT * FROM currentuser"
        
        self.cur.execute(query)
        
        self.current_user_info = self.cur.fetchone()
        
        self.conn.commit()
        self.conn.close()
        
        if self.current_user_info == None:
            raise Exception

        
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
        #  Check Email Compactness
        if not("@" in email) or (not("." in email)):
            QMessageBox.warning(self, 'Details Error', 'Invalid Email Address')
            return
        self.conn = sqlite3.connect("assets/mygpamatedata.db")
        self.cursor = self.conn.cursor()
        

        # Insert user data into the database
        try:
            self.cursor.execute('''INSERT INTO users (first_name, last_name, username, password, email, college_name)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (first_name, last_name, username, password, email, college_name))
            self.conn.commit()
            QMessageBox.information(self, 'Account Created', 'Your account has been created successfully.')
            self.tabWidget_main.setCurrentIndex(1)
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

        self.conn.close()
        
        self.lineEdit_user_name_2.setText("")
        self.lineEdit_first_name_2.setText("")
        self.lineEdit_last_name_2.setText("")
        self.lineEdit_email_2.setText("")
        self.lineEdit_password_2.setText("")
        self.lineEdit_confirm_password_2.setText("")

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
            self.tableWidget_course_info.insertRow(row)
            
        for i in range(3):
            self.tableWidget_course_info.setItem(row , i, QTableWidgetItem(course_info[course_code][i]))
            
        self.lineEdit_course_title.setText("")
        self.lineEdit_course_code.setText("")
        self.spinBox_course_unit.setValue(0)
        
    def load_grade_info(self):
        grade_data_handle = update_table("assets/mygpamatedata.db", self.current_grade_table, self.current_grade_level, self.current_grade_semester)
        grade_data =  grade_data_handle.load_course_from_database() 
        
        
        if grade_data:
            self.tableWidget_grade.setRowCount(1)
            for i in range(len(grade_data)):
                fine_grade_data= grade_data[i]
                new_fine_grade_data= list(fine_grade_data[1:])
                for j in range(len(new_fine_grade_data)):
                    grade_item = QTableWidgetItem(str(new_fine_grade_data[j]))
                    self.tableWidget_grade.setItem(i, j, grade_item)
                row_position = self.tableWidget_grade.rowCount()
                if row_position != len(grade_data):
                    self.tableWidget_grade.insertRow(row_position) 
        else:
            self.tableWidget_grade.setRowCount(0)
            
            return
                    
        self.estimate_grade()
        self.calculategpa()
                    

        # Set all columns as uneditable initially
        self.tableWidget_grade.setEditTriggers(QTableWidget.NoEditTriggers)

        # # Allow editing for specific columns (e.g., column 3)
        # self.tableWidget_grade.setEditTriggers(QTableWidget.DoubleClicked)  # or any other desired trigger

    def load_course_info(self):
        data_handle = update_table("assets/mygpamatedata.db", self.current_course_table, self.current_level, self.current_semester)
        data =  data_handle.load_course_from_database() 
        if data:
            self.tableWidget_course_info.setRowCount(1)
            for i in range(len(data)):
                fine_data = data[i]
                new_fine_data = list(fine_data[1:])
                for j in range(len(new_fine_data)):
                    item = QTableWidgetItem(str(new_fine_data[j]))
                    self.tableWidget_course_info.setItem(i, j, item)
                row_position = self.tableWidget_course_info.rowCount()
                if row_position != len(data):
                    self.tableWidget_course_info.insertRow(row_position)
        else:
            self.tableWidget_course_info.setRowCount(0)
        try:            
            self.estimate_grade()
            self.calculategpa()
        except:
            ...
    def delete_course(self):
        selectedRow = self.tableWidget_course_info.currentRow()
        
        if selectedRow >= 1:
            self.tableWidget_course_info.removeRow(selectedRow)
        
        try:
            self.save_courses()
        except:
            pass
            
    def save_courses(self):
        num_row = self.tableWidget_course_info.rowCount()
        num_col = self.tableWidget_course_info.columnCount()
        
        all_data = []
        final_data = []
        for row in range(num_row):
            course_data = []
            for col in range(num_col):
                item = self.tableWidget_course_info.item(row, col)
                course_data.append(item.text())
            all_data.append(tuple(course_data))
        if len(all_data) == 0:
            QMessageBox.critical(self, "Error", "Courses Cannot Be Empty")
            return
        grade_num_row = self.tableWidget_grade.rowCount()
        grade_num_col = 4
        grade_data = []
        if grade_num_row == 0:
            for data in all_data:
                row_data = data + ("0",)
                final_data.append(row_data)
            ...
        else:
            for i in range(grade_num_row):
                row_data = ()
                for j in range(grade_num_col):
                    item = self.tableWidget_grade.item(i, j).text()
                    row_data = row_data + (item,)
                grade_data.append(row_data)
               
            if len(all_data) == len(grade_data):
                for i in range(len(all_data)):
                    if all_data[i] == grade_data[i][:-1]:
                        final_data.append(grade_data[i])
                    else:
                        final_data.append(all_data[i] + ("0",))           
            elif len(all_data) > len(grade_data):
                for i in range(len(grade_data)):
                    if all_data[i] == grade_data[i][:-1]:
                        final_data.append(grade_data[i])
                    else:
                        final_data.append(all_data[i] + ("0",))
                data_dif = len(all_data) - len(grade_data)
                for k in range(1,data_dif+1):
                    data_to_add = all_data[i+k] + ("0",)
                    final_data.append(data_to_add)
            elif len(all_data) < len(grade_data):
                for i in range(len(all_data)):
                    if all_data[i] == grade_data[i][:-1]:
                        final_data.append(grade_data[i])
                    else:
                        final_data.append(all_data[i] + ("0",))
            
        
        
        data_handle = update_table("assets/mygpamatedata.db", self.current_course_table, self.current_level, self.current_semester) 
        data_handle.save_courses_to_database(final_data)
        
        # Show Success message 
        self.show_message_box("MyGPAmate - Status", "Courses Added Succesfully", QMessageBox.information, QMessageBox.Ok)
        
        # Update Staus Bar
        self.statusBar().showMessage("📌Go to My Grade to Add corresponding Grade to your courses📌")
        # Refresh Grade Table
        self.refresh_table("Grade")
        self.refresh_gpa_com()
    
    
    def handle_combox_changes(self):
        self.comboBox_level.currentTextChanged.connect(partial(self.refresh_table, "Courses"))
        self.comboBox_semester.currentTextChanged.connect(partial(self.refresh_table, "Courses"))
        self.comboBox_level_3.currentTextChanged.connect(partial(self.refresh_table, "Grade"))
        self.comboBox_semester_3.currentTextChanged.connect(partial(self.refresh_table, "Grade"))
        
    def refresh_table(self, table_type):
        self.label_eqp.setText("0")
        self.label_ecu.setText("0")
        self.label_gpa.setText("0.0")
        if table_type == "Courses":
            self.current_level = self.comboBox_level.currentText()
            self.current_semester = self.comboBox_semester.currentText()
        
            n = self.current_level.split()[0]
            m = self.current_semester.split()[0]

            self.current_course_table =  f"{n}{m}Semester"
            
            self.comboBox_level_3.setCurrentText(str(self.comboBox_level.currentText()))
            self.comboBox_semester_3.setCurrentText(str(self.comboBox_semester.currentText()))          
            self.load_course_info()
            
            try:
                self.estimate_grade()
                self.calculategpa()
            except:
                ...

        elif table_type == "Grade":
            self.label_eqp.setText("0")
            self.label_ecu.setText("0")
            self.label_gpa.setText("0.0")
            self.pushButton_edit_grade.setText("Edit Mode")
            self.statusBar().showMessage("")
            self.tableWidget_grade.setItem(0, 4, QTableWidgetItem(" "))
            self.current_grade_level = self.comboBox_level_3.currentText()
            self.current_grade_semester = self.comboBox_semester_3.currentText()
        
            n = self.current_grade_level.split()[0]
            m = self.current_grade_semester.split()[0]

            self.current_grade_table =  f"{n}{m}Semester"
            
            self.comboBox_level.setCurrentText(str(self.comboBox_level_3.currentText()))
            self.comboBox_semester.setCurrentText(str(self.comboBox_semester_3.currentText()))
            
            self.load_grade_info()
            
            try:
                self.estimate_grade()
                self.calculategpa()
                # self.refresh_gpa_com()
            except:
                ...
    
    def update_matplotlib_plot(self):
        # Clear the existing plot
        self.ax.clear()

        # Plot the data
        self.ax.plot(self.semesters, self.gpas, marker='o', linestyle='-', color='b', label='GPA Progression')
        
        # Add data labels
        for i, txt in enumerate(self.gpas):
            self.ax.annotate(f"{txt:.2f}", (self.semesters[i], self.gpas[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        # Highlight important points, e.g., lowest and highest GPAs
        min_gpa_index = np.argmin(self.gpas)
        max_gpa_index = np.argmax(self.gpas)

        # Highlight the lowest and highest GPAs
        self.ax.scatter(self.semesters[min_gpa_index], self.gpas[min_gpa_index], color='red', marker='o', s=150, label=f'Lowest GPA ({self.gpas[min_gpa_index]:.2f})')
        self.ax.scatter(self.semesters[max_gpa_index], self.gpas[max_gpa_index], color='green', marker='o', s=150, label=f'Highest GPA ({self.gpas[max_gpa_index]:.2f})')

        # Customize the plot as needed
        self.ax.set_title('GPA Progression Over Semesters')
        self.ax.set_xlabel('Semester')
        self.ax.set_ylabel('GPA')
        
        upper_lim = max(self.gpas)
        lower_lim = min(self.gpas) - 0.4
        self.ax.set_ylim(lower_lim, 5.0)  # Set y-axis limits for better visualization
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Add legend and show the plot
        self.ax.legend()
        self.canvas.draw()
    
    def hideAndShowPressed(self, currentButton, currentLineEdit):
        current_icon = currentButton.icon()
        current_pixmap = current_icon.pixmap(current_icon.actualSize(QSize(64, 64)))

        # Check if the current icon is the default icon
        if current_pixmap.toImage() == QIcon(":/assets/images/view.png").pixmap(QSize(64, 64)).toImage():
            currentLineEdit.setEchoMode(QLineEdit.Normal)
            currentButton.setIcon(QIcon.fromTheme(":/assets/images/hide.png"))
        else:
            currentLineEdit.setEchoMode(QLineEdit.Password)
            currentButton.setIcon(QIcon.fromTheme(":/assets/images/view.png"))
    
    def show_message_box(self, title, text, icon, buttons=QMessageBox.Ok | QMessageBox.Cancel):
        mg = QMessageBox()
        mg.setWindowTitle(title)
        mg.setText(text)
        mg.setIcon=(icon)   
        mg.setStandardButtons(buttons) 
        mg.exec_()
        


pBui,_ = loadUiType("ProgressbarUI.ui")
counter = 0

class ProgressbarUI(QMainWindow, pBui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)        


        # ProgresBar timer 
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        
        self.timer.start(35)
        
    def progress(self):
        global counter
        
        self.progressBar.setValue(counter)
        
        if counter > 100:
            self.timer.stop()
            ...
            
            self.mainapp = MainApp()
            self.mainapp.show()
            
            self.close()
            
        counter += 1
            


def main():
    app = QApplication([])
    window = ProgressbarUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()      