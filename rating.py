from db import cursor, conn

def add_rating(target_id, score):
    cursor.execute(
        "INSERT INTO ratings (user_id, score) VALUES (%s, %s)",
        (target_id, score)
    )
    conn.commit()
    update_average(target_id)

def update_average(user_id):
    cursor.execute(
        "SELECT AVG(score) FROM ratings WHERE user_id = %s",
        (user_id,)
    )
    result = cursor.fetchone()
    
    if result and result[0] is not None:
        avg = result[0]
        cursor.execute(
            "UPDATE users SET rating = %s WHERE id = %s",
            (avg, user_id)
        )
        conn.commit()