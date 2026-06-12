import sqlite3


def add_credential(user_id, website, email, password, notes):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vault
        (user_id, website, email, password, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, website, email, password, notes)
    )

    conn.commit()
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
        print(f"Website : {row[0]}")
        print(f"Email   : {row[1]}")
        print(f"Password: {row[2]}")
        print(f"Notes   : {row[3]}")
        print("-" * 30)