from models import PasswordStrength, CredentialValidator
from vault import view_all_credentials_raw


class SecurityController:
    @staticmethod
    def check_strength(password: str) -> tuple:
        score, label = PasswordStrength.calculate(password)
        return score, label

    @staticmethod
    def find_duplicates(user_id: int, password: str, key, exclude_website: str = None) -> list:
        try:
            duplicates = CredentialValidator.find_duplicates(
                user_id, password, key, exclude_website
            )
            return duplicates
        except Exception:
            return []

    @staticmethod
    def get_dashboard_stats(user_id: int, key) -> dict:
        try:
            credentials = view_all_credentials_raw(user_id)

            total = len(credentials)
            weak_count = 0
            overdue_count = 0

            for cred in credentials:
                age = CredentialValidator.get_credential_age(cred["created_at"])
                if age >= 90:
                    overdue_count += 1

            overdue = CredentialValidator.get_overdue_passwords(user_id, days_threshold=90)
            weak = CredentialValidator.get_weak_passwords(user_id, threshold=60)

            return {
                "total_credentials": total,
                "weak_passwords": len(weak),
                "overdue_passwords": overdue_count,
                "weak_list": weak,
                "overdue_list": overdue
            }
        except Exception:
            return {
                "total_credentials": 0,
                "weak_passwords": 0,
                "overdue_passwords": 0,
                "weak_list": [],
                "overdue_list": []
            }

    @staticmethod
    def get_credential_age(created_at_str: str) -> int:
        return CredentialValidator.get_credential_age(created_at_str)
