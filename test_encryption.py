import unittest
from encryption import generate_salt, derive_key, encrypt_password, decrypt_password


class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.test_password = "TestPassword123"
        self.salt = generate_salt()

    def test_key_derivation(self):
        key1 = derive_key(self.test_password, self.salt)
        key2 = derive_key(self.test_password, self.salt)
        self.assertEqual(key1, key2, "Same password + salt should produce same key")

    def test_different_salt_different_key(self):
        salt1 = generate_salt()
        salt2 = generate_salt()
        key1 = derive_key(self.test_password, salt1)
        key2 = derive_key(self.test_password, salt2)
        self.assertNotEqual(key1, key2, "Different salts should produce different keys")

    def test_encrypt_decrypt_roundtrip(self):
        key = derive_key(self.test_password, self.salt)
        original_password = "MySecure@Pass123"

        encrypted = encrypt_password(original_password, key)
        decrypted = decrypt_password(encrypted, key)

        self.assertEqual(original_password, decrypted,
                        "Encrypt → Decrypt should return original password")

    def test_encrypt_different_outputs(self):
        key = derive_key(self.test_password, self.salt)
        password = "TestPassword123"

        encrypted1 = encrypt_password(password, key)
        encrypted2 = encrypt_password(password, key)

        self.assertNotEqual(encrypted1, encrypted2,
                           "Encrypting same password twice should produce different ciphertexts")

    def test_decrypt_with_wrong_key_fails(self):
        key1 = derive_key(self.test_password, self.salt)
        key2 = derive_key("DifferentPassword", self.salt)

        password = "TestPassword123"
        encrypted = encrypt_password(password, key1)

        with self.assertRaises(Exception):
            decrypt_password(encrypted, key2)

    def test_empty_password(self):
        key = derive_key(self.test_password, self.salt)
        encrypted = encrypt_password("", key)
        decrypted = decrypt_password(encrypted, key)
        self.assertEqual("", decrypted)

    def test_special_characters(self):
        key = derive_key(self.test_password, self.salt)
        password = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"

        encrypted = encrypt_password(password, key)
        decrypted = decrypt_password(encrypted, key)

        self.assertEqual(password, decrypted)


if __name__ == "__main__":
    unittest.main()
