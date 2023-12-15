import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set the default icon
        self.default_icon_path = 'path_to_default_icon.png'
        self.alternate_icon_path = 'path_to_alternate_icon.png'

        self.button = QPushButton('Toggle Image', self)
        self.button.setIcon(QIcon(self.default_icon_path))

        # Connect the button's clicked signal to the toggle_image slot
        self.button.clicked.connect(self.toggle_image)

        self.label = QLabel('Current Image: Default', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Button Image Example')
        self.show()

    def toggle_image(self):
        current_icon_path = self.button.icon().actualSize(QSize(64, 64)).cacheKey()

        # Check if the current icon is the default icon
        if current_icon_path == self.default_icon_path:
            self.button.setIcon(QIcon(self.alternate_icon_path))
            self.label.setText('Current Image: Alternate')
        else:
            self.button.setIcon(QIcon(self.default_icon_path))
            self.label.setText('Current Image: Default')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())
