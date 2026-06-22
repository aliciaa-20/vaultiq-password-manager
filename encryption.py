import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Number of PBKDF2 iterations. Higher = slower to brute-force, slower to log in.
PBKDF2_ITERATIONS = 200_000


def generate_salt():
    """
    Generate a fresh random salt for a new user.
    Stored in the database (not secret) and reused to re-derive
    that user's key on every login.
    """
    return os.urandom(16)


def derive_key(master_password, salt):
    """
    Turn (master_password + salt) into a Fernet-compatible key.
    Same password + same salt -> same key, every time, with nothing
    about the key itself ever stored on disk.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    raw_key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(raw_key)


def encrypt_password(password, key):
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, key):
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
