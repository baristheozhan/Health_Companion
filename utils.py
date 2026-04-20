from db import cursor

def search_patient(name):
    cursor.execute(
        "SELECT id, name, rating FROM users WHERE role='PATIENT' AND name LIKE %s",
        ("%" + name + "%",)
    )
    return cursor.fetchall()

def search_doctor(name):
    cursor.execute(
        "SELECT id, name, rating FROM users WHERE role='DOCTOR' AND name LIKE %s",
        ("%" + name + "%",)
    )
    return cursor.fetchall()

def get_patient_stats(user_id):
    cursor.execute(
        "SELECT med_name, status FROM medication_logs WHERE user_id=%s",
        (user_id,)
    )
    data = cursor.fetchall()

    result = {}
    for name, status in data:
        if name not in result:
            result[name] = {"TAKEN": 0, "MISSED": 0}

        if status == "TAKEN":
            result[name]["TAKEN"] += 1
        elif status == "MISSED":
            result[name]["MISSED"] += 1

    return result