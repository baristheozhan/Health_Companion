import tkinter as tk
from tkinter import messagebox
from auth import register, login
import patient, doctor

import threading
from scheduler import run

threading.Thread(target=run,daemon=True).start()

root=tk.Tk()

def reg():
    w=tk.Toplevel()
    n=tk.Entry(w); n.pack()
    t=tk.Entry(w); t.pack()
    p=tk.Entry(w,show="*"); p.pack()

    role=tk.StringVar(value="PATIENT")
    tk.OptionMenu(w,role,"PATIENT","DOCTOR").pack()

    def go():
        register(n.get(),t.get(),p.get(),role.get())
        messagebox.showinfo("OK","Registered")

    tk.Button(w,text="Register",command=go).pack()

def log():
    w=tk.Toplevel()
    t=tk.Entry(w); t.pack()
    p=tk.Entry(w,show="*"); p.pack()

    def go():
        u=login(t.get(),p.get())
        if u:
            if u[4]=="PATIENT":
                patient.menu(root,u)
            else:
                doctor.menu(root,u)

    tk.Button(w,text="Login",command=go).pack()

tk.Button(root,text="Register",command=reg).pack()
tk.Button(root,text="Login",command=log).pack()

root.mainloop()