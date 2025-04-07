import tkinter as tk
from tkinter import messagebox
from add_que import open_add_que

def open_admin_login(root, cursor, db):
    close_all_windows(root)
    login_window(root, cursor, "Admin Login", "admin", db)

def login_window(root, cursor, title, role, db):
    close_all_windows(root)
    login_win = tk.Toplevel(root)
    login_win.title(title)
    login_win.geometry("300x200")

    username_label = tk.Label(login_win, text="Username")
    username_label.pack(pady=7)
    username_entry = tk.Entry(login_win)
    username_entry.pack(pady=7)

    password_label = tk.Label(login_win, text="Password")
    password_label.pack(pady=7)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack(pady=7)

    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        if role == "admin":
            if username == "admin" and password == "password":
                messagebox.showinfo("Login Success", f"Welcome, {role.capitalize()}!")
                open_add_que(root, cursor, db)
            else:
                messagebox.showerror("Login Failed", "Invalid admin credentials")

    login_button = tk.Button(login_win, text="Login", command=validate_login)
    login_button.pack(pady=15)

def close_all_windows(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
