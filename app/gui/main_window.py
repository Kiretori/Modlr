import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListView,
    QComboBox,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from database import DB_PATH
import sqlite3
import pandas as pd
import csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the main window
        main_layout = QHBoxLayout()

        # Left section: Profile selection and creation
        left_layout = QVBoxLayout()

        left_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Profile selection
        left_layout.addWidget(QLabel("Select Profile:"))
        self.profile_combo = QComboBox()

        # Fetch all profiles
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM profiles")
            profile_names = map(lambda row: row[0], cur.fetchall())

        self.profile_combo.addItems(profile_names)  # Example profiles
        left_layout.addWidget(self.profile_combo)

        # Create new profile button
        self.create_profile_button = QPushButton("Create New Profile")
        left_layout.addWidget(self.create_profile_button)
        left_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Right section: Dataset upload and actions
        right_layout = QVBoxLayout()

        # Dataset upload
        right_layout.addWidget(QLabel("Upload Dataset:"))
        self.upload_button = QPushButton("Upload Dataset")
        self.upload_button.clicked.connect(self.upload_dataset)
        right_layout.addWidget(self.upload_button)

        # Dataset preview (optional)
        self.dataset_preview = QTableWidget(0, 0)  # Example preview with 5x5 grid
        right_layout.addWidget(self.dataset_preview)

        # Action buttons
        self.continue_button = QPushButton("Continue")
        right_layout.addWidget(self.continue_button)

        # Add layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def upload_dataset(self):
        # Function to upload dataset
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if file:
            try:
                if file.endswith(".csv"):
                    delimiter = detect_csv_delimiter(file)
                    dataset = pd.read_csv(file, delimiter=delimiter)
                    if len(dataset.columns) == 1:
                        print("Only one column detected. If that's not intended make sure the Separator in the CSV file is a comma ','")
                elif file.endswith(".xlsx"):
                    dataset = pd.read_excel(file)
                else:
                    print("File format not suppored.")
                    return
                
                dataset = clean_index_column(dataset)
                rows, cols = dataset.shape
                
                self.dataset_preview.setRowCount(rows)
                self.dataset_preview.setColumnCount(cols)
                self.dataset_preview.setHorizontalHeaderLabels(dataset.columns.astype(str).tolist())

                for i in range(rows):
                    for j in range(cols):
                        value = str(dataset.iat[i, j])
                        self.dataset_preview.setItem(i, j, QTableWidgetItem(value))
            except Exception as e:
                # TODO: error windo
                print(f"Failed to load dataset: {e}")

            
def clean_index_column(df):
    """
    Detect if the first column is just a duplicate of the index and remove it.
    Returns a cleaned DataFrame.
    """
    first_col_name = df.columns[0]
    first_col = df.iloc[:, 0]

    # Heuristics to detect index column
    if (
        first_col_name.lower().startswith('unnamed') or
        first_col_name.lower() in ['index', 'id'] and
        pd.api.types.is_integer_dtype(first_col) and
        (first_col.reset_index(drop=True) == range(len(df))).all()
    ):
        return df.iloc[:, 1:]  # Drop the first column
    return df


def detect_csv_delimiter(file_path, sample_size=2048):
    with open(file_path, 'r', encoding='utf-8') as f:
        sample = f.read(sample_size)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
        except csv.Error:
            return ','
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
