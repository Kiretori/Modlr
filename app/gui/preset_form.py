import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QFileDialog,
    QInputDialog,
    QComboBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import os
from app.utils import get_input_features_from_file
import database
from database.scripts.db_queries import (
    ProfileData,
    ModelBlueprint,
    insert_complete_preset,
)


class ProfileForm(QWidget):
    def __init__(self):
        super().__init__()

        # Hashmap for registered models in the form
        self.registered_models = {}

        # Layout for the form
        layout = QVBoxLayout()

        # Profile name input
        layout.addWidget(QLabel("Profile Name:"))
        self.profile_name_input = QLineEdit()
        layout.addWidget(self.profile_name_input)

        # Model files list
        layout.addWidget(QLabel("Model Files:"))
        self.model_files_list = QListWidget()
        layout.addWidget(self.model_files_list)

        # Buttons to upload and delete model files
        model_files_buttons_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload Model Files")
        self.upload_button.clicked.connect(self.upload_models)
        model_files_buttons_layout.addWidget(self.upload_button)

        self.delete_model_file_button = QPushButton("Delete Model File")
        self.delete_model_file_button.clicked.connect(print)
        layout.addLayout(model_files_buttons_layout)

        # Input features list
        layout.addWidget(QLabel("Input Features:"))
        self.input_features_list = QListWidget()
        self.input_features_list.itemSelectionChanged.connect(self.update_buttons)
        layout.addWidget(self.input_features_list)

        # Buttons to add and delete input features
        input_feature_buttons_layout = QHBoxLayout()
        self.add_input_feature_button = QPushButton("Add Input Feature")
        self.add_input_feature_button.clicked.connect(print)
        input_feature_buttons_layout.addWidget(self.add_input_feature_button)

        self.delete_input_feature_button = QPushButton("Delete Input Feature")
        self.delete_input_feature_button.clicked.connect(print)
        input_feature_buttons_layout.addWidget(self.delete_input_feature_button)
        layout.addLayout(input_feature_buttons_layout)

        # Target variable name
        layout.addWidget(QLabel("Target variable label:"))
        self.target_variable_input = QLineEdit()
        layout.addWidget(self.target_variable_input)

        # Model type selection
        layout.addWidget(QLabel("Model Type:"))
        self.model_type_dropdown = QComboBox()
        self.model_type_dropdown.addItem("Regressor")
        self.model_type_dropdown.addItem("Classifier")
        layout.addWidget(self.model_type_dropdown)

        # Save profile button
        self.save_button = QPushButton("Save Profile")
        self.save_button.clicked.connect(self.save_profile)
        layout.addWidget(self.save_button)

        # Set layout to the main window
        self.setLayout(layout)

        # Initialize the button states
        self.update_buttons()

    def warning_box(self, window_title, text, additional_text):
        warning_box = QMessageBox(self)
        warning_box.setIcon(QMessageBox.Icon.Warning)
        warning_box.setWindowTitle(window_title)
        warning_box.setText(text)
        warning_box.setInformativeText(additional_text)
        warning_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning_box.exec()

    def item_exists(self, list_widget: QListWidget, item_text: str):
        # Iterate through items in the list widget
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            if item.text() == item_text:
                return True
        return False

    def upload_models(self):
        # Function to upload model files
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Model File", "", "All Files (*)"
        )
        if file:
            try:
                input_features = get_input_features_from_file(file)
            except Exception as e:
                self.warning_box(
                    "Error",
                    str(e),
                    "The file you tried to upload is not a .pkl or .joblib file",
                )
                return

            if len(self.registered_models) >= 1:
                for other_model in self.registered_models.values():
                    features_for_validation = get_input_features_from_file(other_model)

                    # Gets input features from first element
                    if len(input_features) != len(features_for_validation):
                        self.warning_box(
                            "Warning",
                            "Input features mismatch",
                            "Models don't have the same number of input features!",
                        )
                        return

                    if sorted(input_features) != sorted(features_for_validation):
                        self.warning_box(
                            "Warning",
                            "Input features mismatch",
                            "Models have different input feature labels, this might cause errors later!",
                        )

            file_name = os.path.basename(file)

            self.registered_models[file_name] = file

            print(self.registered_models)

            for feature in input_features:
                if not self.item_exists(self.input_features_list, feature):
                    self.input_features_list.addItem(feature)

            self.model_files_list.addItem(file_name)
            self.update_buttons()

    def update_buttons(self):
        # Enable/disable the delete buttons based on list content
        self.delete_input_feature_button.setEnabled(
            self.input_features_list.count() > 0
        )
        self.delete_model_file_button.setEnabled(self.model_files_list.count() > 0)

    def save_profile(self):
        features = []
        for index in range(self.input_features_list.count()):
            features.append(self.input_features_list.item(index).text())

        conn = sqlite3.connect(database.DB_PATH)
        cur = conn.cursor()
        model_type_name = self.model_type_dropdown.currentText()

        profile_name = self.profile_name_input.text()
        profile_description = ""

        profile_data = ProfileData(profile_name, profile_description)

        # Fetch model type id from database
        cur.execute(
            "SELECT model_type_id FROM model_types where name == ?", (model_type_name,)
        )
        res = cur.fetchone()
        if res:
            model_type_id = res[0]
        else:
            print("Error assigning a model type")
            raise Exception

        models_data = []
        feature_dict_list: list[dict[str, str]] = []
        for feature in features:
            feature_dict = dict()
            feature_dict["feature_name"] = feature
            feature_dict["feature_type"] = ""
            feature_dict["configuration"] = ""
            feature_dict_list.append(feature_dict)

        for model, path in self.registered_models.items():
            models_data.append(
                ModelBlueprint(
                    model_type_id=model_type_id,
                    model_name=model,
                    model_path=path,
                    features=feature_dict_list,
                )
            )

        try:
            insert_complete_preset(profile_data, models_data)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Failed to save data. Error: {e}")


def main():
    app = QApplication(sys.argv)
    window = ProfileForm()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
