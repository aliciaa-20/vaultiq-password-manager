from encryption import encrypt_password
from encryption import decrypt_password

password = "gmail123"

encrypted = encrypt_password(password)

print("Encrypted:")
print(encrypted)

print("\nDecrypted:")
print(decrypt_password(encrypted))