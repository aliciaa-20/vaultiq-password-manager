import re
from datetime import datetime
from encryption import decrypt_password


class PasswordStrength:
    SCORE_RANGES = [
        (0, 20, "Very Weak"),
        (20, 40, "Weak"),
        (40, 60, "Fair"),
        (60, 80, "Good"),
        (80, 101, "Very Strong"),
    ]

    @staticmethod
    def calculate(password: str) -> tuple[int, str]:
        score = 0

        if len(password) < 8:
            score += 0
        elif len(password) < 12:
            score += 20
        elif len(password) < 16:
            score += 40
        else:
            score += 50

        if re.search(r"[a-z]", password):
            score += 10
        if re.search(r"[A-Z]", password):
            score += 10
        if re.search(r"\d", password):
            score += 10
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            score += 20

        score = min(score, 100)

        label = next(
            label for min_s, max_s, label in PasswordStrength.SCORE_RANGES
            if min_s <= score < max_s
        )

        return score, label


class CredentialValidator:
    @staticmethod
    def find_duplicates(user_id: int, password: str, key, exclude_website: str = None) -> list:
        from database import get_db
        from vault import view_all_credentials_raw

        try:
            credentials = view_all_credentials_raw(user_id)
            duplicates = []

            for cred in credentials:
                if exclude_website and cred["website"] == exclude_website:
                    continue

                try:
                    decrypted = decrypt_password(cred["password"], key)
                    if decrypted == password:
                        duplicates.append(cred["website"])
                except Exception:
                    pass

            return duplicates
        except Exception:
            return []

    @staticmethod
    def get_credential_age(created_at_str: str) -> int:
        try:
            created = datetime.fromisoformat(created_at_str)
            now = datetime.now()
            age = (now - created).days
            return age
        except Exception:
            return 0

    @staticmethod
    def get_overdue_passwords(user_id: int, days_threshold: int = 90) -> list:
        from vault import view_all_credentials_raw

        try:
            credentials = view_all_credentials_raw(user_id)
            overdue = []

            for cred in credentials:
                age = CredentialValidator.get_credential_age(cred["created_at"])
                if age >= days_threshold:
                    overdue.append({
                        "website": cred["website"],
                        "age_days": age
                    })

            return overdue
        except Exception:
            return []

    @staticmethod
    def get_weak_passwords(user_id: int, threshold: int = 60) -> list:
        from vault import view_all_credentials_raw

        try:
            credentials = view_all_credentials_raw(user_id)
            weak = []

            for cred in credentials:
                try:
                    from encryption import decrypt_password
                    key = None
                    decrypted_pwd = decrypt_password(cred["password"], key)
                except Exception:
                    decrypted_pwd = ""

                score, label = PasswordStrength.calculate(decrypted_pwd)
                if score < threshold:
                    weak.append({
                        "website": cred["website"],
                        "score": score,
                        "label": label
                    })

            return weak
        except Exception:
            return []
