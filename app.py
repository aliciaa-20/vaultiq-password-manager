import sys
from PyQt6.QtWidgets import QApplication
from main_window import VaultIQApp


def main():
    app = QApplication(sys.argv)
    window = VaultIQApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
