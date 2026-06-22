import sqlite3
from encryption import encrypt_password, decrypt_password
from database import get_db, DB_PATH


def add_credential(user_id, website, email, password, notes, key):
    if not website or len(website.strip()) < 2:
        raise ValueError("Website must be at least 2 characters")
    if not email or len(email.strip()) < 3:
        raise ValueError("Email must be at least 3 characters")

    encrypted_password = encrypt_password(password, key)

    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                INSERT INTO vault
                (user_id, website, email, password, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    website.strip(),
                    email.strip(),
                    encrypted_password,
                    notes
                )
            )
        return True
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Database error: {e}")
    except Exception as e:
        raise Exception(f"Failed to add credential: {e}")


def view_credentials(user_id, key):
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                SELECT website, email, password, notes, created_at
                FROM vault
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()

        if not rows:
            return []

        credentials = []
        for row in rows:
            try:
                decrypted_password = decrypt_password(row[2], key)
                credentials.append({
                    "website": row[0],
                    "email": row[1],
                    "password": decrypted_password,
                    "notes": row[3],
                    "created_at": row[4]
                })
            except Exception:
                pass

        return credentials
    except Exception as e:
        raise Exception(f"Failed to view credentials: {e}")


def view_all_credentials_raw(user_id):
    """Get all credentials as raw data (for models.py use)"""
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                SELECT credential_id, website, email, password, notes, created_at
                FROM vault
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()

        credentials = []
        for row in rows:
            credentials.append({
                "credential_id": row[0],
                "website": row[1],
                "email": row[2],
                "password": row[3],
                "notes": row[4],
                "created_at": row[5]
            })

        return credentials
    except Exception as e:
        raise Exception(f"Failed to fetch credentials: {e}")


def search_credentials(user_id, website):
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                SELECT website, email, password, notes, created_at
                FROM vault
                WHERE user_id = ?
                AND website LIKE ?
                """,
                (user_id, f"%{website}%")
            )
            rows = cursor.fetchall()

        return rows
    except Exception as e:
        raise Exception(f"Search failed: {e}")


def get_credential(user_id, website):
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                SELECT credential_id, website, email, password, notes, created_at
                FROM vault
                WHERE user_id = ?
                AND website = ?
                """,
                (user_id, website)
            )
            result = cursor.fetchone()

        return result if not result else dict(result)
    except Exception as e:
        raise Exception(f"Failed to get credential: {e}")


def update_email(user_id, website, new_email):
    if not new_email or len(new_email.strip()) < 3:
        raise ValueError("Email must be at least 3 characters")

    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                UPDATE vault
                SET email = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                AND website = ?
                """,
                (new_email.strip(), user_id, website)
            )
        return True
    except Exception as e:
        raise Exception(f"Failed to update email: {e}")


def update_password(user_id, website, new_password, key):
    if not new_password or len(new_password) < 1:
        raise ValueError("Password cannot be empty")

    encrypted_password = encrypt_password(new_password, key)

    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                UPDATE vault
                SET password = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                AND website = ?
                """,
                (encrypted_password, user_id, website)
            )
        return True
    except Exception as e:
        raise Exception(f"Failed to update password: {e}")


def update_notes(user_id, website, new_notes):
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                UPDATE vault
                SET notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                AND website = ?
                """,
                (new_notes, user_id, website)
            )
        return True
    except Exception as e:
        raise Exception(f"Failed to update notes: {e}")


def delete_credential(user_id, website):
    try:
        with get_db(DB_PATH) as cursor:
            cursor.execute(
                """
                DELETE FROM vault
                WHERE user_id = ?
                AND website = ?
                """,
                (user_id, website)
            )
        return True
    except Exception as e:
        raise Exception(f"Failed to delete credential: {e}")
