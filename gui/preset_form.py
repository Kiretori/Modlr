import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QHBoxLayout, QFileDialog, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import app_profile
import ml_utils
import os


class ProfileForm(QWidget):
    def __init__(self):
        super().__init__()

        # Hashmap for registered models in the form
        self.registered_models = {}

        # Layout for the form
        layout = QVBoxLayout()

        # Profile name input
        layout.addWidget(QLabel('Profile Name:'))
        self.profile_name_input = QLineEdit()
        layout.addWidget(self.profile_name_input)

        # Model files list
        layout.addWidget(QLabel('Model Files:'))
        self.model_files_list = QListWidget()
        layout.addWidget(self.model_files_list)

        # Buttons to upload and delete model files
        model_files_buttons_layout = QHBoxLayout()
        self.upload_button = QPushButton('Upload Model Files')
        self.upload_button.clicked.connect(self.upload_models)
        model_files_buttons_layout.addWidget(self.upload_button)

        self.delete_model_file_button = QPushButton('Delete Model File')
        self.delete_model_file_button.clicked.connect(self.delete_model_file)
        model_files_buttons_layout.addWidget(self.delete_model_file_button)
        layout.addLayout(model_files_buttons_layout)

        # Input features list
        layout.addWidget(QLabel('Input Features:'))
        self.input_features_list = QListWidget()
        self.input_features_list.itemSelectionChanged.connect(
            self.update_buttons)
        layout.addWidget(self.input_features_list)

        # Buttons to add and delete input features
        input_feature_buttons_layout = QHBoxLayout()
        self.add_input_feature_button = QPushButton('Add Input Feature')
        self.add_input_feature_button.clicked.connect(self.add_input_feature)
        input_feature_buttons_layout.addWidget(self.add_input_feature_button)

        self.delete_input_feature_button = QPushButton('Delete Input Feature')
        self.delete_input_feature_button.clicked.connect(
            self.delete_input_feature)
        input_feature_buttons_layout.addWidget(
            self.delete_input_feature_button)
        layout.addLayout(input_feature_buttons_layout)

        # Target variable name
        layout.addWidget(QLabel('Target variable label:'))
        self.target_variable_input = QLineEdit()
        layout.addWidget(self.target_variable_input)

        # Save profile button
        self.save_button = QPushButton('Save Profile')
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

    def upload_models(self):
        # Function to upload model files
        file, _ = QFileDialog.getOpenFileName(
            self, 'Select Model File', '', 'All Files (*)')
        if file:

            input_features = ml_utils.get_input_features_from_file(file)

            if len(self.registered_models) >= 1:

                for other_model in self.registered_models.values():
                    features_for_validation = ml_utils.get_input_features_from_file(
                        other_model)

                    # Gets input features from first element
                    if len(input_features) != len(features_for_validation):
                        self.warning_box("Warning", "Input features mismatch",
                                         "Models don't have the same number of input features!")
                        return

                    if sorted(input_features) != sorted(features_for_validation):
                        self.warning_box("Warning", "Input features mismatch",
                                         "Models have different input feature labels this might cause errors later!")

            file_name = os.path.basename(file)

            self.registered_models[file_name] = file

            print(self.registered_models)

            for feature in input_features:
                if (not self.item_exists(self.input_features_list, feature)):
                    self.input_features_list.addItem(feature)

            self.model_files_list.addItem(file_name)
            self.update_buttons()

    def delete_model_file(self):
        # Function to delete the selected model file
        selected_item = self.model_files_list.currentItem()
        if selected_item:
            self.model_files_list.takeItem(
                self.model_files_list.row(selected_item))
            del self.registered_models[selected_item.text()]
            self.update_buttons()

    def add_input_feature(self):
        # Function to add an input feature
        feature, ok = QInputDialog.getText(
            self, 'Add Input Feature', 'Feature:')
        if ok and feature:
            self.input_features_list.addItem(feature)
            self.update_buttons()

    def delete_input_feature(self):
        # Function to delete the selected input feature
        selected_item = self.input_features_list.currentItem()
        if selected_item:
            self.input_features_list.takeItem(
                self.input_features_list.row(selected_item))
            self.update_buttons()

    def add_target_variable(self):
        # Function to add a target variable
        variable, ok = QInputDialog.getText(
            self, 'Add Target Variable', 'Variable:')
        if ok and variable:
            self.target_variables_list.addItem(variable)
            self.update_buttons()

    def delete_target_variable(self):
        # Function to delete the selected target variable
        selected_item = self.target_variables_list.currentItem()
        if selected_item:
            self.target_variables_list.takeItem(
                self.target_variables_list.row(selected_item))
            self.update_buttons()

    def update_buttons(self):
        # Enable/disable the delete buttons based on list content
        self.delete_input_feature_button.setEnabled(
            self.input_features_list.count() > 0)
        self.delete_model_file_button.setEnabled(
            self.model_files_list.count() > 0)

    # Check if item is in a QListWidget
    def item_exists(self, list_widget: QListWidget, item_text: str):
        # Iterate through items in the list widget
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            if item.text() == item_text:
                return True
        return False

    # Function that saves the profile

    def save_profile(self):
        features = []
        for index in range(self.input_features_list.count()):
            features.append(self.input_features_list.item(index).text())

        metadata = app_profile.load_dict_from_json()
        blueprint = app_profile.create_blueprint(
            features, self.target_variable_input.text())
        new_profile = app_profile.create_profile(
            self.profile_name_input.text(), blueprint, list(self.registered_models.values()), metadata)

        if new_profile is not None:
            ok = app_profile.save_profiles_to_json([new_profile], metadata)

            if ok:  # TODO: Show text box for error
                print("Data saved successfully.")
            else:
                print("Failed to save data.")


def main():
    app = QApplication(sys.argv)
    window = ProfileForm()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()