import sqlite3
from encryption import encrypt_password
from encryption import decrypt_password
from logger import log_activity

def add_credential(user_id, website, email, password, notes):

    encrypted_password = encrypt_password(password)
    log_activity(user_id, "Added credential for {}".format(website))

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vault
        (user_id, website, email, password, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            website,
            email,
            encrypted_password,
            notes
        )
    )

    conn.commit()
    log_activity(user_id, "Added new credential")
    conn.close()

    print("Credential added successfully!")


def view_credentials(user_id):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT website, email, password, notes
        FROM vault
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No credentials found.")
        return

    print("\nStored Credentials:\n")

    for row in rows:

        decrypted_password = decrypt_password(row[2])

        print(f"Website : {row[0]}")
        print(f"Email   : {row[1]}")
        print(f"Password: {decrypted_password}")
        print(f"Notes   : {row[3]}")
        print("-" * 30)

def update_credential(user_id, credential_id, website, email, password, notes):
    encrypted_password = encrypt_password(password)

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE vault
        SET website = ?, email = ?, password = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        website,
        email,
        encrypted_password,
        notes,
        credential_id
    ))

    conn.commit()
    log_activity(user_id, "Updated credential")
    conn.close()

    print("Credential updated successfully!")

def delete_credential(credential_id):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vault WHERE id = ?",
        (credential_id,)
    )

    conn.commit()
    conn.close()

    print("Credential deleted successfully!")


def search_credentials(user_id, keyword):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, website, email, password, notes
        FROM vault
        WHERE user_id = ?
        AND (
            website LIKE ?
            OR email LIKE ?
        )
    """, (
        user_id,
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_dashboard_stats(user_id):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM vault
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "favorites": 0,
        "weak": 0,
        "health": 100 if total == 0 else 95
    }
def get_all_credentials(user_id):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, website, email, password, notes
        FROM vault
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    credentials = []

    for row in rows:

        credentials.append(
            (
                row[0],                      # ID
                row[1],                      # Website
                row[2],                      # Email
                decrypt_password(row[3]),   # Decrypted Password
                row[4]                       # Notes
            )
        )

    return credentials