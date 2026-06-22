from vault import (
    add_credential as vault_add,
    view_credentials as vault_view,
    search_credentials as vault_search,
    get_credential as vault_get,
    update_email as vault_update_email,
    update_password as vault_update_password,
    update_notes as vault_update_notes,
    delete_credential as vault_delete
)
from models import CredentialValidator, PasswordStrength


class VaultController:
    @staticmethod
    def add_credential(user_id: int, website: str, email: str, password: str, notes: str, key) -> dict:
        try:
            duplicates = CredentialValidator.find_duplicates(user_id, password, key)

            vault_add(user_id, website, email, password, notes, key)

            return {
                "success": True,
                "message": "Credential added successfully!",
                "duplicates": duplicates
            }
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Failed to add credential: {e}")

    @staticmethod
    def view_all(user_id: int, key) -> list:
        try:
            credentials = vault_view(user_id, key)
            return credentials
        except Exception as e:
            raise Exception(f"Failed to view credentials: {e}")

    @staticmethod
    def search(user_id: int, website: str) -> list:
        try:
            results = vault_search(user_id, website)
            return results
        except Exception as e:
            raise Exception(f"Search failed: {e}")

    @staticmethod
    def get(user_id: int, website: str) -> dict:
        try:
            credential = vault_get(user_id, website)
            return credential
        except Exception as e:
            raise Exception(f"Failed to get credential: {e}")

    @staticmethod
    def update_email(user_id: int, website: str, new_email: str) -> bool:
        try:
            vault_update_email(user_id, website, new_email)
            return True
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Failed to update email: {e}")

    @staticmethod
    def update_password(user_id: int, website: str, new_password: str, key) -> bool:
        try:
            vault_update_password(user_id, website, new_password, key)
            return True
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Failed to update password: {e}")

    @staticmethod
    def update_notes(user_id: int, website: str, new_notes: str) -> bool:
        try:
            vault_update_notes(user_id, website, new_notes)
            return True
        except Exception as e:
            raise Exception(f"Failed to update notes: {e}")

    @staticmethod
    def delete(user_id: int, website: str) -> bool:
        try:
            vault_delete(user_id, website)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete credential: {e}")
