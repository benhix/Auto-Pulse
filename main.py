import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PySide6.QtGui import QIcon, QFont, QClipboard
from PySide6.QtCore import Qt

def resource_path(relative_path):
    """ Generate proper resource path for PyInstaller """ 
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:   
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(430, 270, 1200, 600)  # Adjusted the size to accommodate two text boxes side by side
        self.setWindowTitle('Auto Pulse')

        # Set window icon
        icon_path = resource_path('icon.ico')
        self.setWindowIcon(QIcon(icon_path))

        # Create QLabel to hold everything
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1200, 600)
        self.background.setStyleSheet("background-color: #282828;")

        # Create the main vertical layout
        main_layout = QVBoxLayout(self)

        # Add a spacer to push the text boxes down
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a horizontal layout for the text boxes
        textboxes_layout = QHBoxLayout()

        # Create and set the font
        font = QFont()
        font.setPointSize(12)  # Set the desired font size

        # Creating the input text box
        self.input_textbox = QTextEdit(self)
        self.input_textbox.setPlaceholderText("Enter schedule")
        self.input_textbox.setMinimumSize(500, 400)
        self.input_textbox.setFont(font)  # Set the font for the input text box

        # Creating the output text box
        self.output_textbox = QTextEdit(self)
        self.output_textbox.setPlaceholderText("Output")
        self.output_textbox.setMinimumSize(500, 400)
        self.output_textbox.setFont(font)  # Set the font for the output text box

        # Add the text boxes to the horizontal layout
        textboxes_layout.addWidget(self.input_textbox)
        textboxes_layout.addWidget(self.output_textbox)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(textboxes_layout)

        # Create a horizontal layout for the buttons
        buttons_layout = QHBoxLayout()

        # Add a button to process the input
        self.process_button = QPushButton("Generate Pulse")
        self.process_button.setMinimumSize(200, 50)  # Set the minimum size for the button

        # Set a larger font for the button text
        button_font = QFont()
        button_font.setPointSize(14)  # Set the desired font size for the button
        self.process_button.setFont(button_font)
        self.process_button.clicked.connect(self.process_input)

        # Add a button to copy the output text
        self.copy_button = QPushButton("Copy Output")
        self.copy_button.setMinimumSize(200, 50)  # Set the minimum size for the button
        self.copy_button.setFont(button_font)  # Set the same font for consistency
        self.copy_button.clicked.connect(self.copy_output)

        # Add buttons to the buttons layout
        buttons_layout.addWidget(self.process_button)
        buttons_layout.addWidget(self.copy_button)

        # Add the buttons layout to the main layout
        main_layout.addLayout(buttons_layout)

        # Add another spacer to push the text boxes up from the bottom
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the main window
        self.setLayout(main_layout)

    def process_input(self):
        # Get the input text
        input_text = self.input_textbox.toPlainText()

        # Split the input text into lines
        lines = input_text.splitlines()

        # Create a dictionary to count occurrences
        task_counts = {}
        for line in lines:
            if line.strip():  # Check if the line is not empty or whitespace
                if line in task_counts:
                    task_counts[line] += 0.25
                else:
                    task_counts[line] = 0.25

        # Generate the output text
        output_text = ""
        task_number = 1
        for task, count in task_counts.items():
            output_text += f"{task_number}. {task} ({count})\n"
            task_number += 1

        # Get the current day and date
        now = datetime.now()
        current_day = now.strftime("%A")  # Full weekday name
        current_date = now.strftime("%d/%m/%Y")  # Date in DD/MM/YYYY format

        # Create the header
        header = f"PULSE TEXT: Start Of Day\nBen\n{current_day} {current_date}\n\n"

        # Prepend the header to the output text
        output_text = header + output_text

        # Add total tasks scheduled
        total_tasks = len(task_counts)
        output_text += f"\nTotal Tasks Scheduled: {total_tasks}"

        # Set the output text
        self.output_textbox.setPlainText(output_text)

    def copy_output(self):
        # Get the text from the output text box
        output_text = self.output_textbox.toPlainText()

        # Copy the text to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setApplicationName("Auto Pulse")

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
