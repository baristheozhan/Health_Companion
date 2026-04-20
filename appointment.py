from db import cursor, conn

ALL_SLOTS = ["10:00", "11:00", "12:00", "13:00"]

def get_slots_with_status(doctor_id):
    cursor.execute(
        "SELECT date FROM appointments WHERE doctor_id=%s",
        (doctor_id,)
    )
    taken = [row[0] for row in cursor.fetchall()]

    result = []
    for slot in ALL_SLOTS:
        if slot in taken:
            result.append((slot, False))
        else:
            result.append((slot, True))

    return result

def create_appointment(patient_id, doctor_id, slot):
    cursor.execute(
        "SELECT * FROM appointments WHERE doctor_id=%s AND date=%s",
        (doctor_id, slot)
    )
    if cursor.fetchone():
        return False

    cursor.execute(
        "INSERT INTO appointments (doctor_id, patient_id, institution_id, date) VALUES (%s,%s,1,%s)",
        (doctor_id, patient_id, slot)
    )
    conn.commit()
    return True