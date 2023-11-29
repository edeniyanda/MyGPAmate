import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class GPAPlotter:
    def __init__(self, semesters, gpas):
        self.semesters = semesters
        self.gpas = gpas

    def plot_gpa_progression(self, ax):
        # Plot the data with a line and markers
        ax.plot(self.semesters, self.gpas, marker='o', linestyle='-', color='b', label='GPA Progression')

        # Customize the plot
        ax.set_title('GPA Progression Over Semesters')
        ax.set_xlabel('Semester')
        ax.set_ylabel('GPA')
        ax.set_ylim(3.5, 5.0)  # Set y-axis limits for better visualization
        ax.grid(True, linestyle='--', alpha=0.7)

        # Add data labels
        for i, txt in enumerate(self.gpas):
            ax.annotate(f"{txt:.2f}", (self.semesters[i], self.gpas[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        # Highlight important points, e.g., lowest and highest GPAs
        min_gpa_index = np.argmin(self.gpas)
        max_gpa_index = np.argmax(self.gpas)

        # Highlight the lowest and highest GPAs
        ax.scatter(self.semesters[min_gpa_index], self.gpas[min_gpa_index], color='red', marker='o', s=150, label=f'Lowest GPA ({self.gpas[min_gpa_index]:.2f})')
        ax.scatter(self.semesters[max_gpa_index], self.gpas[max_gpa_index], color='green', marker='o', s=150, label=f'Highest GPA ({self.gpas[max_gpa_index]:.2f})')

        # Add a legend
        ax.legend()

# Example usage:
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Your data
        semesters = ["100L 1st", "100L 2nd", "200L 1st", "200L 2nd", "300L 1st", "300L 2nd", "400L 1st", "400L 2nd"]
        gpas = [4.81, 4.74, 4.78, 4.58, 4.57, 4.26, 3.79, 4.23]

        # Create a QWidget for the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout to hold the QFrame and Matplotlib FigureCanvas
        layout = QVBoxLayout(central_widget)

        # Create a QFrame to hold the Matplotlib plot
        frame = QFrame(self)
        layout.addWidget(frame)

        # Create a Matplotlib Figure and attach it to the QFrame
        fig, ax = plt.subplots(figsize=(8, 5))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Instantiate the GPAPlotter and plot on the Matplotlib axes
        gpa_plotter = GPAPlotter(semesters, gpas)
        gpa_plotter.plot_gpa_progression(ax)

        # Show the Matplotlib plot
        canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
