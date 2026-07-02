from cryptography.fernet import Fernet


def generate_key():

    key = Fernet.generate_key()

    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():

    with open("secret.key", "rb") as key_file:
        return key_file.read()


def encrypt_password(password):

    key = load_key()

    cipher = Fernet(key)

    encrypted_password = cipher.encrypt(
        password.encode()
    )

    return encrypted_password.decode()


def decrypt_password(encrypted_password):

    key = load_key()

    cipher = Fernet(key)

    decrypted_password = cipher.decrypt(
        encrypted_password.encode()
    )

    return decrypted_password.decode()