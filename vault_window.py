from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QProgressBar,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from vault_controller import VaultController
from security_controller import SecurityController
from encryption import decrypt_password
from dialogs import AddCredentialDialog, EditCredentialDialog, ExportDialog, ImportDialog
from utils import copy_to_clipboard
from config import DEFAULT_LOCK_TIMEOUT


class VaultWindow(QMainWindow):
    def __init__(self, user_id, key):
        super().__init__()
        self.user_id = user_id
        self.key = key
        self.vault_controller = VaultController()
        self.security_controller = SecurityController()
        self.selected_credential = None
        self.last_interaction = None

        self.setWindowTitle("VaultIQ - Vault")
        self.setGeometry(100, 100, 1200, 700)

        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.auto_lock)
        self.auto_lock_timer.start(1000)

        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self.check_inactivity)
        self.activity_timer.start(5000)

        self.init_ui()
        self.load_credentials()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        central_widget.setLayout(main_layout)

    def create_left_panel(self):
        frame = QFrame()
        layout = QVBoxLayout()

        title = QLabel("📊 DASHBOARD")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addWidget(QLabel("Total Credentials:"))
        self.total_label = QLabel("0")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #0078d4;")
        layout.addWidget(self.total_label)

        layout.addWidget(QLabel("Weak Passwords:"))
        self.weak_label = QLabel("0")
        self.weak_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff6b6b;")
        layout.addWidget(self.weak_label)

        layout.addWidget(QLabel("Overdue (90+ days):"))
        self.overdue_label = QLabel("0")
        self.overdue_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffa940;")
        layout.addWidget(self.overdue_label)

        layout.addSpacing(20)

        export_btn = QPushButton("📤 Export Vault")
        export_btn.clicked.connect(self.export_vault)
        layout.addWidget(export_btn)

        import_btn = QPushButton("📥 Import Vault")
        import_btn.clicked.connect(self.import_vault)
        layout.addWidget(import_btn)

        layout.addSpacing(20)

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        layout.addStretch()

        frame.setLayout(layout)
        frame.setMaximumWidth(250)
        return frame

    def create_right_panel(self):
        frame = QFrame()
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search credentials...")
        self.search_input.textChanged.connect(self.search_credentials)
        top_layout.addWidget(self.search_input)

        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_credential)
        top_layout.addWidget(add_btn)

        layout.addLayout(top_layout)

        middle_layout = QHBoxLayout()

        self.credentials_list = QListWidget()
        self.credentials_list.itemClicked.connect(self.on_credential_selected)
        middle_layout.addWidget(self.credentials_list, 1)

        self.detail_panel = self.create_detail_panel()
        middle_layout.addWidget(self.detail_panel, 1)

        layout.addLayout(middle_layout)

        frame.setLayout(layout)
        return frame

    def create_detail_panel(self):
        frame = QFrame()
        frame.setStyleSheet("border: 1px solid #3d3d3d; border-radius: 4px;")
        layout = QVBoxLayout()

        title = QLabel("Select a credential to view details")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout()

        content_layout.addWidget(QLabel("Website:"))
        self.detail_website = QLabel()
        content_layout.addWidget(self.detail_website)

        content_layout.addWidget(QLabel("Email:"))
        email_layout = QHBoxLayout()
        self.detail_email = QLabel()
        copy_email_btn = QPushButton("Copy")
        copy_email_btn.setMaximumWidth(60)
        copy_email_btn.clicked.connect(lambda: copy_to_clipboard(self.detail_email.text()))
        email_layout.addWidget(self.detail_email)
        email_layout.addWidget(copy_email_btn)
        content_layout.addLayout(email_layout)

        content_layout.addWidget(QLabel("Password:"))
        pwd_layout = QHBoxLayout()
        self.detail_password = QLabel("••••••••")
        self.show_pwd_btn = QPushButton("Show")
        self.show_pwd_btn.setMaximumWidth(60)
        self.show_pwd_btn.clicked.connect(self.toggle_password)
        copy_pwd_btn = QPushButton("Copy")
        copy_pwd_btn.setMaximumWidth(60)
        copy_pwd_btn.clicked.connect(lambda: copy_to_clipboard(self.actual_password))
        pwd_layout.addWidget(self.detail_password)
        pwd_layout.addWidget(self.show_pwd_btn)
        pwd_layout.addWidget(copy_pwd_btn)
        content_layout.addLayout(pwd_layout)

        content_layout.addWidget(QLabel("Strength:"))
        strength_layout = QHBoxLayout()
        self.detail_strength = QLabel()
        strength_layout.addWidget(self.detail_strength)
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximumHeight(20)
        strength_layout.addWidget(self.strength_bar)
        content_layout.addLayout(strength_layout)

        content_layout.addWidget(QLabel("Age:"))
        self.detail_age = QLabel()
        content_layout.addWidget(self.detail_age)

        content_layout.addWidget(QLabel("Notes:"))
        self.detail_notes = QLabel()
        self.detail_notes.setWordWrap(True)
        content_layout.addWidget(self.detail_notes)

        content_layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.clicked.connect(self.edit_credential)
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_credential)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        content_layout.addLayout(btn_layout)

        content_layout.addStretch()

        content.setLayout(content_layout)
        scroll.setWidget(content)

        layout.addWidget(scroll)
        frame.setLayout(layout)

        return frame

    def load_credentials(self):
        try:
            credentials = self.vault_controller.view_all(self.user_id, self.key)
            self.credentials_list.clear()

            for cred in credentials:
                item = QListWidgetItem(cred.get('website', ''))
                self.credentials_list.addItem(item)

            self.update_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load credentials: {e}")

    def search_credentials(self):
        search_text = self.search_input.text().strip().lower()

        if not search_text:
            self.load_credentials()
            return

        try:
            credentials = self.vault_controller.view_all(self.user_id, self.key)
            self.credentials_list.clear()

            for cred in credentials:
                if search_text in cred.get('website', '').lower() or \
                   search_text in cred.get('email', '').lower():
                    item = QListWidgetItem(cred.get('website', ''))
                    self.credentials_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Search failed: {e}")

    def on_credential_selected(self, item):
        website = item.text()

        try:
            credential = self.vault_controller.get(self.user_id, website)

            if credential:
                self.selected_credential = credential
                self.display_credential(credential)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load credential: {e}")

    def display_credential(self, credential):
        self.detail_website.setText(credential.get('website', 'N/A'))
        self.detail_email.setText(credential.get('email', 'N/A'))

        try:
            self.actual_password = decrypt_password(credential.get('password', ''), self.key)
        except Exception:
            self.actual_password = 'N/A'

        self.detail_password.setText('••••••••')
        self.show_pwd_btn.setText("Show")

        score, label = self.security_controller.check_strength(self.actual_password)
        self.detail_strength.setText(f"{label} ({score}%)")
        self.strength_bar.setValue(score)

        age = self.security_controller.get_credential_age(credential.get('created_at', ''))
        self.detail_age.setText(f"⏱️ {age} days")

        self.detail_notes.setText(credential.get('notes', 'N/A'))

    def toggle_password(self):
        if self.show_pwd_btn.text() == "Show":
            self.detail_password.setText(self.actual_password)
            self.show_pwd_btn.setText("Hide")
        else:
            self.detail_password.setText('••••••••')
            self.show_pwd_btn.setText("Show")

    def update_dashboard(self):
        try:
            stats = self.security_controller.get_dashboard_stats(self.user_id, self.key)
            self.total_label.setText(str(stats['total_credentials']))
            self.weak_label.setText(str(stats['weak_passwords']))
            self.overdue_label.setText(str(stats['overdue_passwords']))
        except Exception:
            pass

    def add_credential(self):
        dialog = AddCredentialDialog(self.user_id, self.key)
        if dialog.exec_():
            self.load_credentials()

    def edit_credential(self):
        if not self.selected_credential:
            QMessageBox.warning(self, "Error", "Please select a credential to edit")
            return

        dialog = EditCredentialDialog(self.user_id, self.key, self.selected_credential)
        if dialog.exec_():
            self.load_credentials()

    def delete_credential(self):
        if not self.selected_credential:
            QMessageBox.warning(self, "Error", "Please select a credential to delete")
            return

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Delete {self.selected_credential.get('website')}?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.vault_controller.delete(self.user_id,
                                            self.selected_credential.get('website'))
                QMessageBox.information(self, "Success", "Credential deleted")
                self.load_credentials()
                self.selected_credential = None
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Delete failed: {e}")

    def export_vault(self):
        dialog = ExportDialog(self.user_id, self.key)
        dialog.exec_()

    def import_vault(self):
        dialog = ImportDialog(self.user_id, self.key)
        if dialog.exec_():
            self.load_credentials()

    def check_inactivity(self):
        pass

    def auto_lock(self):
        pass

    def logout(self):
        reply = QMessageBox.question(self, "Logout",
                                    "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()

    def mouseMoveEvent(self, event):
        self.last_interaction = None
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        self.last_interaction = None
        super().keyPressEvent(event)
