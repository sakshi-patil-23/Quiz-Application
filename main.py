import tkinter as tk
import mysql.connector
from admin_login import open_admin_login
from user_login import open_user_login

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root", 
        database="py_project"
    )

def create_main_window():
    root = tk.Tk()
    root.title("Welcome to Quiz Game")
    root.geometry("300x200")

    welcome_label = tk.Label(root, text="Welcome to Quiz Game", font=("Helvetica", 16))
    welcome_label.pack(pady=20)

    # Database connection setup
    db = get_database_connection()
    cursor = db.cursor()

    admin_button = tk.Button(root, text="Admin Login", width=20, height=2, command=lambda: open_admin_login(root, cursor, db))
    admin_button.pack(pady=10)  # Corrected to pack the admin button+-

    user_button = tk.Button(root, text="User Login", width=20, height=2, command=lambda: open_user_login(root, cursor, db))
    user_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: close_connection(db, root))
    return root, db, cursor

def close_connection(db, root):
    db.close()
    root.destroy()

if __name__ == "__main__":
    root, db, cursor = create_main_window()
    root.mainloop()
