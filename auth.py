from db import cursor, conn


def register(name, tckn, password, role):
    cursor.execute(
        "INSERT INTO users (name, tckn, password, role) VALUES (%s, %s, %s, %s)",
        (name, tckn, password, role)
    )
    conn.commit()


def login(tckn, password):
    cursor.execute(
        "SELECT * FROM users WHERE tckn=%s AND password=%s",
        (tckn, password)
    )
    return cursor.fetchone()