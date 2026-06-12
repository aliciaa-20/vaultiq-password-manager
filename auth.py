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