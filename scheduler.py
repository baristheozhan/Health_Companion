import time
from db import cursor, conn

def reset():
    cursor.execute("UPDATE medication_logs SET status='PENDING'")
    conn.commit()

def run():
    last = None
    while True:
        day = time.strftime("%Y-%m-%d")
        if day != last:
            reset()
            last = day
        time.sleep(60)