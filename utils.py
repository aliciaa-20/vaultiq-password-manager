import json
import csv
from pathlib import Path


def copy_to_clipboard(text: str) -> bool:
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QClipboard

        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        return True
    except Exception:
        return False


def export_to_json(credentials: list, file_path: str) -> bool:
    try:
        with open(file_path, 'w') as f:
            json.dump(credentials, f, indent=2, default=str)
        return True
    except Exception:
        return False


def export_to_csv(credentials: list, file_path: str) -> bool:
    try:
        if not credentials:
            return False

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Website', 'Email', 'Password', 'Notes', 'Created'])

            for cred in credentials:
                writer.writerow([
                    cred.get('website', ''),
                    cred.get('email', ''),
                    cred.get('password', ''),
                    cred.get('notes', ''),
                    cred.get('created_at', '')
                ])

        return True
    except Exception:
        return False


def import_from_csv(file_path: str) -> list:
    try:
        credentials = []

        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                credentials.append({
                    'website': row.get('Website', ''),
                    'email': row.get('Email', ''),
                    'password': row.get('Password', ''),
                    'notes': row.get('Notes', '')
                })

        return credentials
    except Exception:
        return []
