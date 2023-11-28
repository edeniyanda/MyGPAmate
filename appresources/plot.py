import matplotlib.pyplot as plt
import numpy as np

class GPAPlotter:
    def __init__(self, semesters, gpas):
        self.semesters = semesters
        self.gpas = gpas

    def plot_gpa_progression(self):
        # Create a figure and axis with a larger size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the data with a line and markers
        plt.plot(self.semesters, self.gpas, marker='o', linestyle='-', color='b', label='GPA Progression')

        # Customize the plot
        plt.title('GPA Progression Over Semesters')
        plt.xlabel('Semester')
        plt.ylabel('GPA')
        plt.ylim(3.5, 5.0)  # Set y-axis limits for better visualization
        plt.grid(True, linestyle='--', alpha=0.7)

        # Add data labels
        for i, txt in enumerate(self.gpas):
            ax.annotate(f"{txt:.2f}", (self.semesters[i], self.gpas[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        # Highlight important points, e.g., lowest and highest GPAs
        min_gpa_index = np.argmin(self.gpas)
        max_gpa_index = np.argmax(self.gpas)

        # Highlight the lowest and highest GPAs
        plt.scatter(self.semesters[min_gpa_index], self.gpas[min_gpa_index], color='red', marker='o', s=150, label=f'Lowest GPA ({self.gpas[min_gpa_index]:.2f})')
        plt.scatter(self.semesters[max_gpa_index], self.gpas[max_gpa_index], color='green', marker='o', s=150, label=f'Highest GPA ({self.gpas[max_gpa_index]:.2f})')

        # Add a legend
        plt.legend()

        # Display the plot
        plt.tight_layout()  # Ensure all elements are properly placed
        plt.xticks(rotation=25)  # Rotate x-axis labels for better readability
        plt.show()

