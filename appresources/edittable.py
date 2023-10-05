from PyQt5.QtWidgets import  QItemDelegate

class MyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        # Allow editing for specific columns (e.g., column 1)
        if index.column() == 3:
            return super(MyDelegate, self).createEditor(parent, option, index)
        else:
            return None  # Disable editing for other columns
        
class MyDelegate2(QItemDelegate):
    def createEditor(self, parent, option, index):
        # Allow editing for specific columns (e.g., column 1)
        if index.column() == 1:
            return super(MyDelegate2, self).createEditor(parent, option, index)
        else:
            return None  # Disable editing for other columns