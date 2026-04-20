import tkinter as tk
from tkinter import messagebox
from db import cursor, conn
from ui import *

AVAILABLE_TIMES = [
    "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00"
]

def menu(root, user):
    win = tk.Toplevel(root)
    setup_window(win, "Patient Menu", 700, 500)
    frame = create_card(win, 460, 320)
    title_label(frame, f"Welcome, {user[1]}").pack(pady=(30, 10))
    subtitle_label(frame, "Patient Dashboard").pack(pady=(0, 25))
    primary_button(frame, "Medicine Tracking", lambda: med(win, user), 22).pack(pady=10)
    primary_button(frame, "Make Appointment", lambda: appt(win, user), 22).pack(pady=10)
    primary_button(frame, "Rating", lambda: rate(win), 22).pack(pady=10)

def med(parent, user):
    w = tk.Toplevel(parent)
    setup_window(w, "Medicine Tracking", 900, 720)
    frame = create_card(w, 760, 600)
    title_label(frame, "Medicine Tracking").pack(pady=(25, 10))
    subtitle_label(frame, "Add, edit, save, delete or update medicine status").pack(pady=(0, 15))
    listbox = tk.Listbox(frame, width=60, height=10, font=("Segoe UI", 11), selectbackground="#4a90e2", selectforeground="white")
    listbox.pack(pady=10)
    normal_label(frame, "Medicine Name").pack()
    entry = styled_entry(frame, width=36)
    entry.pack(pady=8, ipady=6)
    selected_id = {"value": None}

    def load():
        listbox.delete(0, tk.END)
        cursor.execute("SELECT id, med_name, status FROM medication_logs WHERE user_id=%s ORDER BY id DESC", (user[0],))
        rows = cursor.fetchall()
        for row in rows:
            listbox.insert(tk.END, f"{row[0]} | {row[1]} - {row[2]}")
        selected_id["value"] = None
        entry.delete(0, tk.END)

    def get_selected_row():
        if not listbox.curselection(): return None
        selected_text = listbox.get(listbox.curselection()[0])
        parts = selected_text.split(" | ", 1)
        if len(parts) != 2: return None
        row_id = int(parts[0])
        rest = parts[1]
        med_name = rest.rsplit(" - ", 1)[0] if " - " in rest else rest
        return row_id, med_name

    def on_select(event=None):
        selected = get_selected_row()
        if selected:
            selected_id["value"], med_name = selected
            entry.delete(0, tk.END)
            entry.insert(0, med_name)

    def add():
        med_name = entry.get().strip()
        if not med_name: return messagebox.showerror("Error", "Enter medicine name.")
        cursor.execute("INSERT INTO medication_logs(user_id, med_name) VALUES(%s, %s)", (user[0], med_name))
        conn.commit()
        load()

    def save():
        if selected_id["value"] is None: return messagebox.showerror("Error", "Select a medicine.")
        new_name = entry.get().strip()
        cursor.execute("UPDATE medication_logs SET med_name=%s WHERE id=%s AND user_id=%s", (new_name, selected_id["value"], user[0]))
        conn.commit()
        load()

    def delete():
        selected = get_selected_row()
        if not selected: return messagebox.showerror("Error", "Select a medicine.")
        if messagebox.askyesno("Confirm", f"Delete '{selected[1]}'?"):
            cursor.execute("DELETE FROM medication_logs WHERE id=%s AND user_id=%s", (selected[0], user[0]))
            conn.commit()
            load()

    def update_status(new_status):
        selected = get_selected_row()
        if not selected: return messagebox.showerror("Error", "Select a medicine.")
        cursor.execute("UPDATE medication_logs SET status=%s WHERE id=%s AND user_id=%s", (new_status, selected[0], user[0]))
        conn.commit()
        load()

    listbox.bind("<<ListboxSelect>>", on_select)
    row1 = tk.Frame(frame, bg=CARD)
    row1.pack(pady=10)
    primary_button(row1, "Add", add, 9).grid(row=0, column=0, padx=5)
    primary_button(row1, "Save", save, 9).grid(row=0, column=1, padx=5)
    danger_button(row1, "Delete", delete, 9).grid(row=0, column=2, padx=5)
    row2 = tk.Frame(frame, bg=CARD)
    row2.pack(pady=8)
    success_button(row2, "Taken", lambda: update_status("TAKEN"), 12).grid(row=0, column=0, padx=6)
    danger_button(row2, "Missed", lambda: update_status("MISSED"), 12).grid(row=0, column=1, padx=6)
    load()

def appt(parent, user):
    w = tk.Toplevel(parent)
    setup_window(w, "Make Appointment", 820, 650)
    frame = create_card(w, 680, 540)
    title_label(frame, "Make Appointment").pack(pady=(25, 10))
    subtitle_label(frame, "Choose doctor, date and available time").pack(pady=(0, 20))
    normal_label(frame, "Doctor Name Surname").pack()
    doctor_entry = styled_entry(frame, width=36)
    doctor_entry.pack(pady=8, ipady=6)
    normal_label(frame, "Appointment Date (YYYY-MM-DD)").pack()
    date_entry = styled_entry(frame, width=36)
    date_entry.pack(pady=8, ipady=6)
    time_var = tk.StringVar()
    time_frame = tk.Frame(frame, bg=CARD)
    time_frame.pack(pady=10)

    def load_times():
        for child in time_frame.winfo_children(): child.destroy()
        d_name, d_date = doctor_entry.get().strip(), date_entry.get().strip()
        if not d_name or not d_date: return messagebox.showerror("Error", "Fill doctor and date.")
        cursor.execute("SELECT id FROM users WHERE LOWER(name) = LOWER(%s) AND role='DOCTOR'", (d_name,))
        doc = cursor.fetchone()
        if not doc: return messagebox.showerror("Error", "Doctor not found.")
        cursor.execute("SELECT date FROM appointments WHERE doctor_id=%s AND date LIKE %s", (doc[0], f"{d_date}%"))
        taken = [r[0].split(" ")[1] for r in cursor.fetchall() if " " in r[0]]
        r, c = 0, 0
        for t in AVAILABLE_TIMES:
            state = "disabled" if t in taken else "normal"
            bg = "#cbd5e1" if t in taken else PRIMARY
            tk.Radiobutton(time_frame, text=t, variable=time_var, value=t, indicatoron=0, width=10, pady=8, font=("Segoe UI", 10, "bold"), bg=bg, fg="white", state=state).grid(row=r, column=c, padx=6, pady=6)
            c += 1
            if c == 4: c, r = 0, r + 1

    def book():
        d_name, d_date, s_time = doctor_entry.get().strip(), date_entry.get().strip(), time_var.get()
        if not s_time: return messagebox.showerror("Error", "Select a time.")
        cursor.execute("SELECT id FROM users WHERE LOWER(name) = LOWER(%s) AND role='DOCTOR'", (d_name,))
        doc = cursor.fetchone()
        full_dt = f"{d_date} {s_time}"
        cursor.execute("INSERT INTO appointments(doctor_id, patient_id, date) VALUES(%s, %s, %s)", (doc[0], user[0], full_dt))
        conn.commit()
        messagebox.showinfo("Success", "Appointment booked.")
        w.destroy()

    btns = tk.Frame(frame, bg=CARD)
    btns.pack(pady=15)
    primary_button(btns, "Check Times", load_times, 18).grid(row=0, column=0, padx=6)
    primary_button(btns, "Book Now", book, 18).grid(row=0, column=1, padx=6)

def rate(parent):
    w = tk.Toplevel(parent)
    setup_window(w, "Rating", 780, 560)
    frame = create_card(w, 640, 420)
    title_label(frame, "Rate Doctor / Hospital").pack(pady=(25, 10))
    normal_label(frame, "Type").pack()
    target_type = tk.StringVar(value="DOCTOR")
    tk.OptionMenu(frame, target_type, "DOCTOR", "HOSPITAL").pack(pady=8)
    normal_label(frame, "Name").pack()
    name_entry = styled_entry(frame, width=34)
    name_entry.pack(pady=8)
    normal_label(frame, "Score (1-5)").pack()
    score_entry = styled_entry(frame, width=34)
    score_entry.pack(pady=8)

    def send():
        name, score, t_type = name_entry.get().strip(), score_entry.get().strip(), target_type.get()
        if not name or not score: return messagebox.showerror("Error", "Fill all fields.")
        try:
            val = int(score)
            if val < 1 or val > 5: raise ValueError
        except: return messagebox.showerror("Error", "Invalid score (1-5).")
        cursor.execute("SELECT id FROM users WHERE LOWER(name) LIKE LOWER(%s) AND role=%s", (f"%{name}%", t_type))
        target = cursor.fetchone()
        if not target: return messagebox.showerror("Error", "Target not found.")
        tid = target[0]
        cursor.execute("INSERT INTO ratings(user_id, score) VALUES(%s, %s)", (tid, val))
        cursor.execute("SELECT AVG(score) FROM ratings WHERE user_id=%s", (tid,))
        avg = cursor.fetchone()[0]
        cursor.execute("UPDATE users SET rating=%s WHERE id=%s", (avg, tid))
        conn.commit()
        messagebox.showinfo("Success", f"Rating updated. New Average: {avg:.1f}")
        w.destroy()

    primary_button(frame, "Submit Rating", send, 20).pack(pady=20)