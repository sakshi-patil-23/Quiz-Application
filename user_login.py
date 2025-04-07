import tkinter as tk
from tkinter import messagebox
from quiz_options import open_welcome_screen


def open_user_login(root, cursor, db):
    close_all_windows(root)
    user_login_win = tk.Toplevel(root)
    user_login_win.title("User Options")
    user_login_win.geometry("300x200")

    login_button = tk.Button(user_login_win, text="Login", command=lambda: login_window(root, cursor, db, "User Login", "user"))
    login_button.pack(pady=10)

    register_button = tk.Button(user_login_win, text="Register", command=lambda: open_registration(root, cursor, db))
    register_button.pack(pady=10)

def login_window(root, cursor, db, title, role):
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

        if role == "user":
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Login Success", "Welcome, User!")
                open_welcome_screen(root, cursor, db, username)
            else:
                messagebox.showerror("Login Failed", "Invalid user credentials. Please register first.")

    login_button = tk.Button(login_win, text="Login", command=validate_login)
    login_button.pack(pady=15)

def open_registration(root, cursor, db):
    close_all_windows(root)
    register_win = tk.Toplevel(root)
    register_win.title("User Registration")
    register_win.geometry("300x250")

    username_label = tk.Label(register_win, text="Username")
    username_label.pack(pady=7)
    username_entry = tk.Entry(register_win)
    username_entry.pack(pady=7)

    password_label = tk.Label(register_win, text="Password")
    password_label.pack(pady=7)
    password_entry = tk.Entry(register_win, show="*")
    password_entry.pack(pady=7)

    confirm_password_label = tk.Label(register_win, text="Confirm Password")
    confirm_password_label.pack(pady=7)
    confirm_password_entry = tk.Entry(register_win, show="*")
    confirm_password_entry.pack(pady=7)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password == confirm_password:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Registration Failed", "Username already exists.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                messagebox.showinfo("Registration Success", "You have successfully registered!")
                register_win.destroy()
        else:
            messagebox.showerror("Registration Failed", "Passwords do not match.")

    register_button = tk.Button(register_win, text="Register", command=register_user)
    register_button.pack(pady=15)

def close_all_windows(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
