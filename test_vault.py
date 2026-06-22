import unittest
import os
from database import create_database, DB_PATH
from auth import register_user, login_user
from vault_controller import VaultController
from models import CredentialValidator
from encryption import generate_salt, derive_key


class TestVault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_vault.db"
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        from database import DB_PATH as original_db
        create_database(self.test_db)

        self.username = "testuser"
        self.password = "TestPassword123"
        salt = generate_salt()
        self.key = derive_key(self.password, salt)

        register_user(self.username, self.password)
        self.user_id, self.key = login_user(self.username, self.password)

        self.controller = VaultController()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_credential(self):
        result = self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "Main email account",
            self.key
        )
        self.assertEqual(result['success'], True)

    def test_add_credential_empty_website(self):
        with self.assertRaises(ValueError):
            self.controller.add_credential(
                self.user_id,
                "",
                "test@gmail.com",
                "MyPassword123",
                "",
                self.key
            )

    def test_add_credential_short_website(self):
        with self.assertRaises(ValueError):
            self.controller.add_credential(
                self.user_id,
                "a",
                "test@gmail.com",
                "MyPassword123",
                "",
                self.key
            )

    def test_view_all_credentials(self):
        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "Main email",
            self.key
        )

        credentials = self.controller.view_all(self.user_id, self.key)
        self.assertEqual(len(credentials), 1)
        self.assertEqual(credentials[0]['website'], "gmail.com")

    def test_search_credentials(self):
        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "",
            self.key
        )

        self.controller.add_credential(
            self.user_id,
            "github.com",
            "test@github.com",
            "AnotherPass123",
            "",
            self.key
        )

        results = self.controller.search(self.user_id, "github")
        self.assertEqual(len(results), 1)

    def test_get_credential(self):
        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "Main account",
            self.key
        )

        cred = self.controller.get(self.user_id, "gmail.com")
        self.assertIsNotNone(cred)
        self.assertEqual(cred['website'], "gmail.com")

    def test_update_email(self):
        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "",
            self.key
        )

        self.controller.update_email(self.user_id, "gmail.com", "newemail@gmail.com")
        cred = self.controller.get(self.user_id, "gmail.com")
        self.assertEqual(cred['email'], "newemail@gmail.com")

    def test_delete_credential(self):
        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            "MyPassword123",
            "",
            self.key
        )

        self.controller.delete(self.user_id, "gmail.com")
        cred = self.controller.get(self.user_id, "gmail.com")
        self.assertIsNone(cred)

    def test_duplicate_password_detection(self):
        password = "SamePassword123"

        self.controller.add_credential(
            self.user_id,
            "gmail.com",
            "test@gmail.com",
            password,
            "",
            self.key
        )

        result = self.controller.add_credential(
            self.user_id,
            "github.com",
            "test@github.com",
            password,
            "",
            self.key
        )

        self.assertEqual(len(result['duplicates']), 1)
        self.assertIn("gmail.com", result['duplicates'])


if __name__ == "__main__":
    unittest.main()
