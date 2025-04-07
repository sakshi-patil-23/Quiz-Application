import tkinter as tk
from tkinter import messagebox, ttk
from textwrap import wrap
import mysql.connector

def open_admin_login(root, cursor, db):
    open_add_que(root, cursor, db)

def open_add_que(root, cursor, db):
    close_all_windows(root)
    dashboard_win = tk.Toplevel(root)
    dashboard_win.title("Admin Dashboard")
    dashboard_win.geometry("400x300")

    back_button = tk.Button(dashboard_win, text="Back", command=dashboard_win.destroy)
    back_button.pack(anchor="nw", padx=10, pady=10)

    add_question_button = tk.Button(dashboard_win, text="Add Question", command=lambda: add_question(root, cursor, db, dashboard_win))
    add_question_button.pack(pady=10)

    remove_question_button = tk.Button(dashboard_win, text="Remove Question", command=lambda: remove_question(root, cursor, db, dashboard_win))
    remove_question_button.pack(pady=10)

    show_questions_button = tk.Button(dashboard_win, text="Show Questions", command=lambda: show_questions(root, cursor, dashboard_win))
    show_questions_button.pack(pady=10)

    dashboard_win.protocol("WM_DELETE_WINDOW", lambda: close_connection(db, root))

def add_question(root, cursor, db, dashboard_win):
    add_win = tk.Toplevel(root)
    add_win.title("Add Question")
    add_win.geometry("600x600")

    back_button = tk.Button(add_win, text="Back", command=lambda: [add_win.destroy(), dashboard_win.deiconify()])
    back_button.pack(anchor="nw", padx=10, pady=10)

    question_label = tk.Label(add_win, text="Question")
    question_label.pack(pady=7)
    question_entry = tk.Entry(add_win, width=50)
    question_entry.pack(pady=7)

    option1_label = tk.Label(add_win, text="Option 1")
    option1_label.pack(pady=7)
    option1_entry = tk.Entry(add_win, width=50)
    option1_entry.pack(pady=7)

    option2_label = tk.Label(add_win, text="Option 2")
    option2_label.pack(pady=7)
    option2_entry = tk.Entry(add_win, width=50)
    option2_entry.pack(pady=7)

    option3_label = tk.Label(add_win, text="Option 3")
    option3_label.pack(pady=7)
    option3_entry = tk.Entry(add_win, width=50)
    option3_entry.pack(pady=7)

    option4_label = tk.Label(add_win, text="Option 4")
    option4_label.pack(pady=7)
    option4_entry = tk.Entry(add_win, width=50)
    option4_entry.pack(pady=7)

    correct_option_label = tk.Label(add_win, text="Correct Option (1-4)")
    correct_option_label.pack(pady=7)
    correct_option_entry = tk.Entry(add_win, width=50)
    correct_option_entry.pack(pady=7)

    level_label = tk.Label(add_win, text="Level (easy, medium, hard)")
    level_label.pack(pady=7)
    level_entry = tk.Entry(add_win, width=50)
    level_entry.pack(pady=7)

    def save_question():
        question = question_entry.get()
        option1 = option1_entry.get()
        option2 = option2_entry.get()
        option3 = option3_entry.get()
        option4 = option4_entry.get()
        correct_option = correct_option_entry.get()
        level = level_entry.get()

        if correct_option not in ['1', '2', '3', '4']:
            messagebox.showerror("Error", "Please enter a valid correct option (1-4).")
            return

        cursor.execute("SELECT * FROM questions WHERE question_text = %s", (question,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Question already exists.")
        else:
            cursor.execute(
                "INSERT INTO questions (question_text, option1, option2, option3, option4, correct_option, level) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (question, option1, option2, option3, option4, correct_option, level))
            db.commit()
            messagebox.showinfo("Success", "Question added successfully!")
            add_win.destroy()
            dashboard_win.deiconify()

    save_button = tk.Button(add_win, text="Save Question", command=save_question)
    save_button.pack(pady=15)

def remove_question(root, cursor, db, dashboard_win):
    remove_win = tk.Toplevel(root)
    remove_win.title("Remove Question")
    remove_win.geometry("300x200")

    back_button = tk.Button(remove_win, text="Back", command=lambda: [remove_win.destroy(), dashboard_win.deiconify()])
    back_button.pack(anchor="nw", padx=10, pady=10)

    question_label = tk.Label(remove_win, text="Question")
    question_label.pack(pady=7)
    question_entry = tk.Entry(remove_win)
    question_entry.pack(pady=7)

    def delete_question():
        question = question_entry.get()

        cursor.execute("SELECT * FROM questions WHERE question_text = %s", (question,))
        result = cursor.fetchone()

        if result:
            cursor.execute("DELETE FROM questions WHERE question_text = %s", (question,))
            db.commit()
            messagebox.showinfo("Success", "Question removed successfully!")
            remove_win.destroy()
            dashboard_win.deiconify()
        else:
            messagebox.showerror("Error", "Question not found in the database.")

    delete_button = tk.Button(remove_win, text="Delete Question", command=delete_question)
    delete_button.pack(pady=15)

def show_questions(root, cursor, dashboard_win):
    show_win = tk.Toplevel(root)
    show_win.title("All Questions")
    show_win.geometry("900x400")

    back_button = tk.Button(show_win, text="Back", command=lambda: [show_win.destroy(), dashboard_win.deiconify()])
    back_button.pack(anchor="nw", padx=10, pady=10)

    columns = ("sr_no", "question", "option1", "option2", "option3", "option4", "correct_option")
    tree = ttk.Treeview(show_win, columns=columns, show="headings")

    tree.heading("sr_no", text="Sr. No")
    tree.column("sr_no", width=50, anchor="center")

    tree.heading("question", text="Question")
    tree.column("question", width=530, anchor="w")

    tree.heading("option1", text="Option 1")
    tree.column("option1", width=70, anchor="center")

    tree.heading("option2", text="Option 2")
    tree.column("option2", width=70, anchor="center")

    tree.heading("option3", text="Option 3")
    tree.column("option3", width=70, anchor="center")

    tree.heading("option4", text="Option 4")
    tree.column("option4", width=70, anchor="center")

    tree.heading("correct_option", text="Correct Option")
    tree.column("correct_option", width=50, anchor="center")

    scrollbar = ttk.Scrollbar(show_win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    cursor.execute("SELECT id, question_text, option1, option2, option3, option4, correct_option FROM questions")
    questions = cursor.fetchall()

    for i, question in enumerate(questions, start=1):
        wrapped_question = "\n".join(wrap(question[1], width=50))
        tree.insert("", "end", values=(i, wrapped_question, *question[2:]))

    style = ttk.Style()
    style.configure("Treeview", rowheight=100, borderwidth=1, relief="solid")  # Default rowheight
    tree.pack(fill="both", expand=True)

    show_win.protocol("WM_DELETE_WINDOW", lambda: [show_win.destroy(), dashboard_win.deiconify()])

def close_all_windows(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

def close_connection(db, root):
    db.close()
    root.destroy()
