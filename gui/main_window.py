import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListView, QComboBox, QFileDialog, QTableWidget, QTableWidgetItem, QSplitter
)
from PyQt6.QtCore import Qt, QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the main window
        main_layout = QHBoxLayout()

        # Left section: Profile selection and creation
        left_layout = QVBoxLayout()
        
        # Profile selection
        left_layout.addWidget(QLabel('Select Profile:'))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Profile 1", "Profile 2", "Profile 3"])  # Example profiles
        left_layout.addWidget(self.profile_combo)

        # Create new profile button
        self.create_profile_button = QPushButton('Create New Profile')
        left_layout.addWidget(self.create_profile_button)

        # Right section: Dataset upload and actions
        right_layout = QVBoxLayout()

        # Dataset upload
        right_layout.addWidget(QLabel('Upload Dataset:'))
        self.upload_button = QPushButton('Upload Dataset')
        self.upload_button.clicked.connect(self.upload_dataset)
        right_layout.addWidget(self.upload_button)

        # Dataset preview (optional)
        self.dataset_preview = QTableWidget(5, 5)  # Example preview with 5x5 grid
        right_layout.addWidget(self.dataset_preview)

        # Action buttons
        self.continue_button = QPushButton('Continue')
        right_layout.addWidget(self.continue_button)

        # Add layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def upload_dataset(self):
        # Function to upload dataset
        file, _ = QFileDialog.getOpenFileName(self, 'Select Dataset', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file:
            # You can add logic here to read and preview the dataset
            # For now, we'll just simulate adding the file name to the preview
            self.dataset_preview.setItem(0, 0, QTableWidgetItem(file.split('/')[-1]))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()