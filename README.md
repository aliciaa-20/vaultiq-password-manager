# VaultIQ - Secure Password Manager

A professional desktop password manager built with Python, PyQt5, and military-grade encryption. Perfect for the Samsung Innovation Campus internship project.

## Features

- 🔐 **Military-Grade Encryption**: PBKDF2 + Fernet encryption
- 🎨 **Dark Theme UI**: Modern, corporate aesthetic
- 📊 **Dashboard**: Real-time statistics (total, weak, overdue passwords)
- 🔑 **Password Strength Meter**: Real-time visual feedback
- ⚠️ **Duplicate Detection**: Warns when same password is used multiple times
- ⏱️ **Password Age Tracking**: Days since last change
- 📤 **Export/Import**: CSV and JSON formats
- 📋 **Copy to Clipboard**: Quick access with one click
- 🔒 **Auto-Lock**: Configurable timeout for security
- 🎯 **MVC Architecture**: Clean, maintainable code

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone or download the project
cd vaultiq-password-manager

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py
```

### First Time
1. Click **Register** tab
2. Create username (3+ characters) and password (8+ characters)
3. Watch the strength meter update in real-time
4. Click **Register**
5. Login with your credentials

### In the Vault
- **Add**: Click ➕ to add new credentials
- **View**: Click any credential to see details
- **Copy**: Click [Copy] buttons for email/password
- **Edit**: Select a credential and click ✏️
- **Delete**: Select a credential and click 🗑️
- **Search**: Type in search bar to filter
- **Dashboard**: Left panel shows stats
- **Export**: Save vault as CSV (safe) or JSON (all data)
- **Import**: Load credentials from CSV file

## Architecture

```
vaultiq-password-manager/
├── auth.py                 # Authentication logic
├── vault.py               # Credential CRUD
├── encryption.py          # PBKDF2 + Fernet
├── generator.py           # Password generation
├── database.py            # SQLite + Database class
├── models.py              # Business logic (strength, duplicates, age)
├── config.py              # Constants & dark theme
├── auth_controller.py     # Auth orchestration
├── vault_controller.py    # Vault operations
├── security_controller.py # Dashboard & validation
├── login_window.py        # Login/Register UI
├── vault_window.py        # Main vault UI
├── dialogs.py            # Add/Edit/Import/Export dialogs
├── main_window.py        # App orchestrator
├── app.py                # Entry point
├── utils.py              # Clipboard, file I/O
├── test_encryption.py    # Encryption tests
├── test_strength.py      # Strength meter tests
├── test_vault.py         # CRUD tests
└── requirements.txt      # Dependencies
```

## Testing

```bash
# Run all tests
python -m pytest test_*.py -v

# Or individual tests
python -m unittest test_encryption.TestEncryption -v
python -m unittest test_strength.TestPasswordStrength -v
python -m unittest test_vault.TestVault -v
```

## Security Features

1. **Zero-Knowledge Design**: Master password never stored, encryption key derived on every login
2. **PBKDF2**: 200,000 iterations for key derivation (resistant to brute-force)
3. **Fernet Encryption**: AES-128 authenticated encryption
4. **Bcrypt Hashing**: Password hashing with salt
5. **Random Salts**: 16-byte random salt per user
6. **Clipboard Clearing**: [Future feature] Auto-clear clipboard after 30 seconds

## Portfolio Value

This project showcases:
- ✅ **Python Mastery**: OOP, design patterns, modules
- ✅ **Database Design**: Normalization, relationships, migrations
- ✅ **Cryptography**: Key derivation, symmetric encryption, hashing
- ✅ **GUI Development**: PyQt5, signals/slots, layout management
- ✅ **Architecture**: MVC pattern, separation of concerns, testability
- ✅ **Testing**: Unit tests, edge cases, error handling
- ✅ **Code Quality**: Type hints, error messages, clean code

## Future Enhancements

- [ ] Master password change
- [ ] Breach detection (Have I Been Pwned API)
- [ ] TOTP 2FA support
- [ ] Vault backup/restore
- [ ] Password change history
- [ ] Keyboard shortcuts
- [ ] Light theme toggle
- [ ] Multi-vault support
- [ ] Cloud sync (encrypted)

## License

MIT License - Feel free to use for your internship project!

## Author

Created for Samsung Innovation Campus Internship - Coding & Programming Track
