import tkinter as tk

BG = "#eef3f9"
CARD = "#ffffff"
PRIMARY = "#4a90e2"
PRIMARY_DARK = "#3578c8"
SUCCESS = "#28a745"
DANGER = "#dc3545"
TEXT = "#1f2937"
MUTED = "#6b7280"
BORDER = "#d9e2ec"


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


def setup_window(window, title, width, height):
    window.title(title)
    window.configure(bg=BG)
    window.resizable(False, False)
    center_window(window, width, height)


def create_card(parent, width, height):
    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1,
        bd=0
    )
    frame.place(relx=0.5, rely=0.5, anchor="center", width=width, height=height)
    return frame


def title_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 20, "bold"),
        bg=CARD,
        fg=TEXT
    )


def subtitle_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 10),
        bg=CARD,
        fg=MUTED
    )


def normal_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 11),
        bg=CARD,
        fg=TEXT
    )


def styled_entry(parent, width=28, show=None):
    entry = tk.Entry(
        parent,
        font=("Segoe UI", 11),
        width=width,
        show=show,
        relief="solid",
        bd=1
    )
    return entry


def primary_button(parent, text, command, width=18):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        width=width,
        height=2,
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_DARK,
        activeforeground="white",
        bd=0,
        cursor="hand2"
    )
    return btn


def success_button(parent, text, command, width=12):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        width=width,
        height=2,
        bg=SUCCESS,
        fg="white",
        activebackground="#218838",
        activeforeground="white",
        bd=0,
        cursor="hand2"
    )
    return btn


def danger_button(parent, text, command, width=12):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        width=width,
        height=2,
        bg=DANGER,
        fg="white",
        activebackground="#c82333",
        activeforeground="white",
        bd=0,
        cursor="hand2"
    )
    return btn