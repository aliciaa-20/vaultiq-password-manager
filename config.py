DEFAULT_LOCK_TIMEOUT = 900
DEFAULT_PASSWORD_LENGTH = 16
MIN_PASSWORD_AGE_WARNING = 90
EXPORT_FORMATS = ["JSON", "CSV"]

DARK_THEME_STYLESHEET = """
    QMainWindow {
        background-color: #1e1e1e;
    }

    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }

    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1084d7;
    }

    QPushButton:pressed {
        background-color: #005a9e;
    }

    QLineEdit, QTextEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        padding: 8px;
    }

    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #0078d4;
    }

    QLabel {
        color: #ffffff;
    }

    QProgressBar {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #0078d4;
    }

    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 12px;
    }

    QScrollBar::handle:vertical {
        background-color: #3d3d3d;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #4d4d4d;
    }

    QListWidget {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
    }

    QListWidget::item:selected {
        background-color: #0078d4;
    }

    QDialog {
        background-color: #1e1e1e;
    }

    QTabWidget::pane {
        border: 1px solid #3d3d3d;
    }

    QTabBar::tab {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 8px 20px;
    }

    QTabBar::tab:selected {
        background-color: #0078d4;
    }
"""
