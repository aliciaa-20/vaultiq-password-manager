import sqlite3


def log_activity(user_id, action):

    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity_logs(user_id, action)
        VALUES(?, ?)
    """, (user_id, action))

    conn.commit()
    conn.close()