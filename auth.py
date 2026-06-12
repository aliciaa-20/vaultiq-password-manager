import sqlite3
import bcrypt


def register_user(username, password):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (
                username,
                hashed_password.decode()
            )
        )

        conn.commit()
        print("User registered successfully!")

    except sqlite3.IntegrityError:
        print("Username already exists!")

    conn.close()


def login_user(username, password):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        print("Invalid username or password!")
        return None

    user_id = result[0]
    stored_hash = result[1]

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        print("Login successful!")
        return user_id

    print("Invalid username or password!")
    return None