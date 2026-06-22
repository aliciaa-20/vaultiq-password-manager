from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QMessageBox, QProgressBar, QFileDialog, QSpinBox
)
from PyQt6.QtCore import Qt
from vault_controller import VaultController
from security_controller import SecurityController
from generator import generate_password
from models import PasswordStrength
from utils import export_to_csv, export_to_json, import_from_csv


class AddCredentialDialog(QDialog):
    def __init__(self, user_id, key):
        super().__init__()
        self.user_id = user_id
        self.key = key
        self.vault_controller = VaultController()
        self.security_controller = SecurityController()

        self.setWindowTitle("Add Credential")
        self.setGeometry(200, 200, 400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Website:"))
        self.website_input = QLineEdit()
        layout.addWidget(self.website_input)

        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Password:"))
        pwd_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.textChanged.connect(self.update_strength)
        pwd_layout.addWidget(self.password_input)
        gen_btn = QPushButton("Generate")
        gen_btn.setMaximumWidth(100)
        gen_btn.clicked.connect(self.generate_password)
        pwd_layout.addWidget(gen_btn)
        layout.addLayout(pwd_layout)

        layout.addWidget(QLabel("Strength:"))
        self.strength_label = QLabel("Very Weak")
        layout.addWidget(self.strength_label)

        self.strength_bar = QProgressBar()
        self.strength_bar.setValue(0)
        layout.addWidget(self.strength_bar)

        self.duplicate_warning = QLabel()
        self.duplicate_warning.setStyleSheet("color: #ff6b6b;")
        layout.addWidget(self.duplicate_warning)

        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_credential)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_strength(self):
        password = self.password_input.text()
        score, label = PasswordStrength.calculate(password)

        self.strength_bar.setValue(score)
        self.strength_label.setText(label)

        if score < 60:
            color = "#ff6b6b"
        elif score < 80:
            color = "#ffa940"
        else:
            color = "#52c41a"

        self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        duplicates = self.security_controller.find_duplicates(
            self.user_id, password, self.key
        )

        if duplicates:
            self.duplicate_warning.setText(f"⚠️ Same password used for: {', '.join(duplicates)}")
        else:
            self.duplicate_warning.setText("")

    def generate_password(self):
        pwd = generate_password(16)
        self.password_input.setText(pwd)

    def save_credential(self):
        website = self.website_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        notes = self.notes_input.toPlainText()

        if not website or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all required fields")
            return

        try:
            self.vault_controller.add_credential(
                self.user_id, website, email, password, notes, self.key
            )
            QMessageBox.information(self, "Success", "Credential added successfully!")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add credential: {e}")


class EditCredentialDialog(QDialog):
    def __init__(self, user_id, key, credential):
        super().__init__()
        self.user_id = user_id
        self.key = key
        self.credential = credential
        self.vault_controller = VaultController()

        self.setWindowTitle("Edit Credential")
        self.setGeometry(200, 200, 400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Website: {self.credential.get('website')}"))

        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setText(self.credential.get('email', ''))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QTextEdit()
        self.notes_input.setText(self.credential.get('notes', ''))
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save_changes(self):
        email = self.email_input.text().strip()
        notes = self.notes_input.toPlainText()

        if not email:
            QMessageBox.warning(self, "Error", "Email cannot be empty")
            return

        try:
            website = self.credential.get('website')
            self.vault_controller.update_email(self.user_id, website, email)
            self.vault_controller.update_notes(self.user_id, website, notes)
            QMessageBox.information(self, "Success", "Credential updated!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Update failed: {e}")


class ExportDialog(QDialog):
    def __init__(self, user_id, key):
        super().__init__()
        self.user_id = user_id
        self.key = key
        self.vault_controller = VaultController()

        self.setWindowTitle("Export Vault")
        self.setGeometry(200, 200, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Choose export format:"))

        csv_btn = QPushButton("Export as CSV (Safe)")
        csv_btn.clicked.connect(self.export_csv)
        layout.addWidget(csv_btn)

        json_btn = QPushButton("Export as JSON (All data)")
        json_btn.clicked.connect(self.export_json)
        layout.addWidget(json_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)

    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export as CSV", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            credentials = self.vault_controller.view_all(self.user_id, self.key)
            export_to_csv(credentials, file_path)
            QMessageBox.information(self, "Success", f"Exported to {file_path}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def export_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export as JSON", "", "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            credentials = self.vault_controller.view_all(self.user_id, self.key)
            export_to_json(credentials, file_path)
            QMessageBox.information(self, "Success", f"Exported to {file_path}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {e}")


class ImportDialog(QDialog):
    def __init__(self, user_id, key):
        super().__init__()
        self.user_id = user_id
        self.key = key
        self.vault_controller = VaultController()

        self.setWindowTitle("Import Vault")
        self.setGeometry(200, 200, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select CSV file to import:"))

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self.import_file)
        layout.addWidget(import_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)
        self.selected_file = None

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split('/')[-1])

    def import_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file")
            return

        try:
            credentials = import_from_csv(self.selected_file)

            if not credentials:
                QMessageBox.warning(self, "Error", "No valid credentials in file")
                return

            for cred in credentials:
                self.vault_controller.add_credential(
                    self.user_id,
                    cred.get('website', 'Unknown'),
                    cred.get('email', ''),
                    cred.get('password', ''),
                    cred.get('notes', ''),
                    self.key
                )

            QMessageBox.information(self, "Success", f"Imported {len(credentials)} credentials!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Import failed: {e}")
