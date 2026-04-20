import tkinter as tk
from tkinter import messagebox
from auth import register, login
import patient
import doctor
from ui import *
from db import cursor

def open_register():
    win = tk.Toplevel(root)
    setup_window(win, "Register", 740, 560)
    frame = create_card(win, 600, 430)
    
    title_label(frame, "Create Account").grid(row=0, column=0, columnspan=2, pady=(25, 10))
    subtitle_label(frame, "Please fill in all information completely").grid(row=1, column=0, columnspan=2, pady=(0, 20))

    normal_label(frame, "Full Name:").grid(row=2, column=0, sticky="w", padx=(30, 15), pady=10)
    name_entry = styled_entry(frame, width=28)
    name_entry.grid(row=2, column=1, padx=(0, 30), pady=10, ipady=6)

    normal_label(frame, "TCKN (ID):").grid(row=3, column=0, sticky="w", padx=(30, 15), pady=10)
    tckn_entry = styled_entry(frame, width=28)
    tckn_entry.grid(row=3, column=1, padx=(0, 30), pady=10, ipady=6)

    normal_label(frame, "Password:").grid(row=4, column=0, sticky="w", padx=(30, 15), pady=10)
    password_entry = styled_entry(frame, width=28, show="*")
    password_entry.grid(row=4, column=1, padx=(0, 30), pady=10, ipady=6)

    normal_label(frame, "Role:").grid(row=5, column=0, sticky="w", padx=(30, 15), pady=10)
    role_var = tk.StringVar(value="PATIENT")
    role_menu = tk.OptionMenu(frame, role_var, "PATIENT", "DOCTOR", "HOSPITAL")
    role_menu.config(font=("Segoe UI", 11), width=26, bg="white")
    role_menu.grid(row=5, column=1, sticky="w", padx=(0, 30), pady=10)

    def do_register():
        name = name_entry.get().strip()
        tckn = tckn_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get().strip()
        
        if not name or not tckn or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        try:
            register(name, tckn, password, role)
            messagebox.showinfo("Success", "Account created successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Registration error: {e}")

    primary_button(frame, "Register", do_register, 18).grid(row=6, column=0, columnspan=2, pady=(25, 10))

def open_login():
    win = tk.Toplevel(root)
    setup_window(win, "Login", 680, 430)
    frame = create_card(win, 540, 300)
    
    title_label(frame, "System Login").grid(row=0, column=0, columnspan=2, pady=(20, 8))
    subtitle_label(frame, "Login with your TCKN and password").grid(row=1, column=0, columnspan=2, pady=(0, 18))

    normal_label(frame, "TCKN (ID):").grid(row=2, column=0, sticky="w", padx=(30, 15), pady=10)
    tckn_entry = styled_entry(frame, width=26)
    tckn_entry.grid(row=2, column=1, padx=(0, 30), pady=10, ipady=6)

    normal_label(frame, "Password:").grid(row=3, column=0, sticky="w", padx=(30, 15), pady=10)
    password_entry = styled_entry(frame, width=26, show="*")
    password_entry.grid(row=3, column=1, padx=(0, 30), pady=10, ipady=6)

    def do_login():
        tckn = tckn_entry.get().strip()
        password = password_entry.get().strip()
        
        if not tckn or not password:
            messagebox.showerror("Error", "Please do not leave fields empty.")
            return
            
        try:
            user = login(tckn, password)
            if user:
                messagebox.showinfo("Success", "Login successful.")
                win.destroy()
                if user[4] == "PATIENT":
                    patient.menu(root, user)
                else:
                    doctor.menu(root, user)
            else:
                messagebox.showerror("Error", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    primary_button(frame, "Login", do_login, 16).grid(row=4, column=0, columnspan=2, pady=(22, 10))

def open_ratings_lookup():
    win = tk.Toplevel(root)
    setup_window(win, "Rating Inquiry", 450, 350)
    frame = create_card(win, 380, 260)
    
    title_label(frame, "Search Rating").pack(pady=(20, 10))
    subtitle_label(frame, "Enter Doctor or Hospital name").pack(pady=(0, 15))
    
    name_entry = styled_entry(frame, width=32)
    name_entry.pack(pady=10, ipady=5)
    
    def show_rating():
        target_name = name_entry.get().strip()
        if not target_name:
            messagebox.showerror("Error", "Please enter a name.")
            return
            
        cursor.execute(
            "SELECT rating FROM users WHERE LOWER(name) LIKE LOWER(%s) AND role IN ('DOCTOR', 'HOSPITAL')",
            (f"%{target_name}%",)
        )
        res = cursor.fetchone()
        
        if res:
            messagebox.showinfo("Result", f"{target_name} Average Rating: {res[0]}")
        else:
            messagebox.showwarning("Not Found", "Registered doctor or hospital not found.")

    primary_button(frame, "Submit", show_rating, 15).pack(pady=15)

root = tk.Tk()
setup_window(root, "Health Companion", 700, 560)

main_frame = create_card(root, 540, 440)

title_label(main_frame, "Health Companion").pack(pady=(35, 10))
subtitle_label(main_frame, "Please choose the action you want to perform").pack(pady=(0, 25))

primary_button(main_frame, "Register", open_register, 20).pack(pady=8)
primary_button(main_frame, "Login", open_login, 20).pack(pady=8)
primary_button(main_frame, "See Ratings", open_ratings_lookup, 20).pack(pady=8)

root.mainloop()