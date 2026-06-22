from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from login_window import LoginWindow
from vault_window import VaultWindow
from config import DARK_THEME_STYLESHEET
from database import create_database


class VaultIQApp(QMainWindow):
    def __init__(self):
        super().__init__()

        create_database()

        self.login_window = LoginWindow()
        self.vault_window = None
        self.current_user_id = None
        self.current_key = None

        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.show()

        self.setStyleSheet(DARK_THEME_STYLESHEET)
        self.setWindowTitle("VaultIQ - Password Manager")

    def on_login_success(self, user_id, key):
        self.current_user_id = user_id
        self.current_key = key

        self.login_window.close()

        self.vault_window = VaultWindow(user_id, key)
        self.vault_window.setStyleSheet(DARK_THEME_STYLESHEET)
        self.vault_window.show()
