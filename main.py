from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PySide6
import qdarkstyle
import sys
import sqlite3



from PyQt5.uic import loadUiType
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
        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.tabBar().setVisible(False)
        ...
    def Handle_Button(self):
        self.pushButton_get_started.clicked.connect(self.change_main_widget_index)
        ...    
        
    def change_main_widget_index(self):
        self.tabWidget_main.setCurrentIndex(1)
        

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    
    
if __name__ == "__main__":
    main()
       