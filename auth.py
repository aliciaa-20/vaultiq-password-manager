import sqlite3
import bcrypt

from encryption import generate_salt, derive_key


def register_user(username, password):
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters.")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    salt = generate_salt()

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt)
            VALUES (?, ?, ?)
            """,
            (
                username,
                hashed_password.decode(),
                salt
            )
        )

        conn.commit()

    except sqlite3.IntegrityError:
        raise ValueError("Username already exists!")

    finally:
        conn.close()


def login_user(username, password):
    """
    Returns (user_id, key) on success, (None, None) on failure.
    `key` is the per-user Fernet key, derived fresh from the master
    password and salt — never stored anywhere.
    """

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        raise ValueError("Invalid username or password!")

    user_id, stored_hash, salt = result

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        key = derive_key(password, salt)
        return user_id, key

    raise ValueError("Invalid username or password!")
