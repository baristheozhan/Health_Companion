import tkinter as tk
from tkinter import messagebox
from db import cursor
from ui import *


# =========================
# DOCTOR / HOSPITAL MENU
# =========================
def menu(root, user):
    win = tk.Toplevel(root)
    setup_window(win, "Doctor Panel", 720, 520)

    frame = create_card(win, 480, 320)

    role_text = "Doctor Panel"
    if user[4] == "HOSPITAL":
        role_text = "Hospital Panel"

    title_label(frame, f"Welcome, {user[1]}").pack(pady=(30, 10))
    subtitle_label(frame, role_text).pack(pady=(0, 25))

    primary_button(frame, "Appointments", lambda: appt(user), 22).pack(pady=10)
    primary_button(frame, "Patient Tracking", track, 22).pack(pady=10)


# =========================
# APPOINTMENTS
# =========================
def appt(user):
    w = tk.Toplevel()
    setup_window(w, "Appointments", 820, 560)

    frame = create_card(w, 660, 430)

    title_label(frame, "Appointments").pack(pady=(25, 10))
    subtitle_label(frame, "Today's and upcoming appointments").pack(pady=(0, 15))

    listbox = tk.Listbox(
        frame,
        width=65,
        height=14,
        font=("Segoe UI", 11),
        selectbackground="#4a90e2",
        selectforeground="white"
    )
    listbox.pack(pady=15)

    if user[4] == "DOCTOR":
        cursor.execute("""
            SELECT a.date, u.name
            FROM appointments a
            JOIN users u ON a.patient_id = u.id
            WHERE a.doctor_id = %s
            ORDER BY a.date
        """, (user[0],))
    else:
        cursor.execute("""
            SELECT a.date, p.name, d.name
            FROM appointments a
            JOIN users p ON a.patient_id = p.id
            JOIN users d ON a.doctor_id = d.id
            ORDER BY a.date
        """)

    rows = cursor.fetchall()

    if not rows:
        listbox.insert(tk.END, "No appointments found.")
    else:
        if user[4] == "DOCTOR":
            for row in rows:
                listbox.insert(tk.END, f"Patient: {row[1]}  |  Date: {row[0]}")
        else:
            for row in rows:
                listbox.insert(tk.END, f"Patient: {row[1]}  |  Doctor: {row[2]}  |  Date: {row[0]}")


# =========================
# PATIENT TRACKING
# =========================
def track():
    w = tk.Toplevel()
    setup_window(w, "Patient Tracking", 900, 650)

    frame = create_card(w, 760, 520)

    title_label(frame, "Patient Tracking").pack(pady=(25, 10))
    subtitle_label(frame, "Search by patient name and surname").pack(pady=(0, 18))

    normal_label(frame, "Patient Name Surname").pack()

    top_row = tk.Frame(frame, bg=CARD)
    top_row.pack(pady=10)

    entry = styled_entry(top_row, width=30)
    entry.grid(row=0, column=0, padx=(0, 10), ipady=6)

    listbox = tk.Listbox(
        frame,
        width=70,
        height=16,
        font=("Segoe UI", 11),
        selectbackground="#4a90e2",
        selectforeground="white"
    )
    listbox.pack(pady=20)

    def search():
        listbox.delete(0, tk.END)

        patient_name = entry.get().strip()

        if patient_name == "":
            messagebox.showerror("Error", "Please enter patient name and surname.")
            return

        cursor.execute(
            """
            SELECT id, name
            FROM users
            WHERE LOWER(name) LIKE LOWER(%s)
            AND role = 'PATIENT'
            """,
            ("%" + patient_name + "%",)
        )
        patient = cursor.fetchone()

        if not patient:
            listbox.insert(tk.END, "Patient not found.")
            return

        patient_id = patient[0]
        patient_full_name = patient[1]

        cursor.execute(
            """
            SELECT med_name, status
            FROM medication_logs
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (patient_id,)
        )
        rows = cursor.fetchall()

        listbox.insert(tk.END, f"Patient: {patient_full_name}")
        listbox.insert(tk.END, "-" * 60)

        if not rows:
            listbox.insert(tk.END, "No medicine records found.")
            return

        for row in rows:
            listbox.insert(tk.END, f"Medicine: {row[0]}   |   Status: {row[1]}")

    primary_button(top_row, "Submit", search, 12).grid(row=0, column=1, padx=5)