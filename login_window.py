from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal
from auth_controller import AuthController
from models import PasswordStrength


class LoginWindow(QDialog):
    login_success = pyqtSignal(int, bytes)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultIQ - Login")
        self.setGeometry(100, 100, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        banner = QLabel("🔐 VaultIQ")
        banner.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078d4;")
        layout.addWidget(banner)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_login_tab(), "Login")
        self.tabs.addTab(self.create_register_tab(), "Register")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_login_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.login_username = QLineEdit()
        layout.addWidget(self.login_username)

        layout.addWidget(QLabel("Password:"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.login_password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.do_login)
        layout.addWidget(login_btn)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_register_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.reg_username = QLineEdit()
        layout.addWidget(self.reg_username)

        layout.addWidget(QLabel("Password:"))
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password.textChanged.connect(self.update_strength_meter)
        layout.addWidget(self.reg_password)

        layout.addWidget(QLabel("Password Strength:"))
        self.strength_label = QLabel("Very Weak")
        self.strength_label.setStyleSheet("color: #ff6b6b;")
        layout.addWidget(self.strength_label)

        self.strength_bar = QProgressBar()
        self.strength_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #ff6b6b;
            }
        """)
        self.strength_bar.setValue(0)
        layout.addWidget(self.strength_bar)

        layout.addWidget(QLabel("Confirm Password:"))
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.reg_confirm)

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.do_register)
        layout.addWidget(register_btn)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def update_strength_meter(self):
        password = self.reg_password.text()
        score, label = PasswordStrength.calculate(password)

        self.strength_bar.setValue(score)
        self.strength_label.setText(label)

        if score < 20:
            color = "#ff6b6b"
        elif score < 40:
            color = "#ffa940"
        elif score < 60:
            color = "#fadb14"
        elif score < 80:
            color = "#52c41a"
        else:
            color = "#13c2c2"

        self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)

    def do_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        try:
            controller = AuthController()
            user_id, key = controller.login(username, password)
            self.login_success.emit(user_id, key)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Login Failed", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def do_register(self):
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            controller = AuthController()
            controller.register(username, password)
            QMessageBox.information(self, "Success", "Account created! Please login.")
            self.tabs.setCurrentIndex(0)
            self.reg_username.clear()
            self.reg_password.clear()
            self.reg_confirm.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Registration Failed", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
