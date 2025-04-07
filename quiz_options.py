import tkinter as tk
from tkinter import messagebox
import mysql.connector
import time
import random

# Global variables
questions = []
current_question_index = 0
start_time = 0
selected_answers = []

def close_all_windows(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

def open_quiz_options(root, cursor, db, username):
    close_all_windows(root)
    quiz_options_win = tk.Toplevel(root)
    quiz_options_win.title("Quiz Options")
    quiz_options_win.geometry("300x200")
    
    welcome_label = tk.Label(quiz_options_win, text=f"Welcome, {username}!", font=("Helvetica", 16))
    welcome_label.pack(pady=20)
    
    easy_button = tk.Button(quiz_options_win, text="Easy", command=lambda: start_quiz(root, cursor, db, "easy", username))
    easy_button.pack(pady=10)
    
    medium_button = tk.Button(quiz_options_win, text="Medium", command=lambda: start_quiz(root, cursor, db, "medium", username))
    medium_button.pack(pady=10)
    
    hard_button = tk.Button(quiz_options_win, text="Hard", command=lambda: start_quiz(root, cursor, db, "hard", username))
    hard_button.pack(pady=10)

def start_quiz(root, cursor, db, level, username):
    global current_question_index, start_time, questions, selected_answers

    cursor.execute("SELECT id, question_text, option1, option2, option3, option4, correct_option FROM questions WHERE level = %s", (level,))
    all_questions = cursor.fetchall()

    questions = random.sample(all_questions, 5)  
    selected_answers = [None] * len(questions)  
    current_question_index = 0
    start_time = time.time()
    show_question_window(root, cursor, db, level, username)

def show_question_window(root, cursor, db, level, username):
    close_all_windows(root)
    question_win = tk.Toplevel(root)
    question_win.title("Quiz")
    question_win.geometry("800x500")

    global current_question_index

    # Display question tracker
    tracker_frame = tk.Frame(question_win)
    tracker_frame.pack(pady=10)
    
    tracker_label = tk.Label(tracker_frame, text="Questions: ")
    tracker_label.pack(side=tk.LEFT)

    question_tracker_text = " ".join([str(i + 1) + ("✓" if selected_answers[i] is not None else "✗") for i in range(len(questions))])
    question_tracker = tk.Label(tracker_frame, text=question_tracker_text)
    question_tracker.pack(side=tk.LEFT)

    def submit_answer(direction):
        global current_question_index

        selected_option = option_var.get()
        if selected_option:
            selected_answers[current_question_index] = selected_option

        if direction == "next" and current_question_index < len(questions) - 1:
            current_question_index += 1
        elif direction == "prev" and current_question_index > 0:
            current_question_index -= 1

        if current_question_index < len(questions):
            show_question_window(root, cursor, db, level, username)
        else:
            end_quiz(cursor, db, level, username)

    def end_quiz(cursor, db, level, username):
        try:
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            score = sum(1 for i in range(len(questions)) if questions[i][6] == selected_answers[i])

            # Save the score in the database
            cursor.execute("INSERT INTO score (username, score, quiz_level, date_taken) VALUES (%s, %s, %s, NOW())", (username, score, level))
            db.commit()

            correct_answers = []
            incorrect_answers = []

            for i, (question_id, question, option1, option2, option3, option4, correct_option) in enumerate(questions):
                if selected_answers[i] == correct_option:
                    correct_answers.append(f"Q{i + 1}: {question} - Correct")
                else:
                    incorrect_answers.append(f"Q{i + 1}: {question} - Incorrect (Correct Answer: {correct_option})")

            result_message = f"Your score: {score}/{len(questions)}\nTime taken: {elapsed_time} seconds\n\n"
            result_message += "Correct Answers:\n" + "\n".join(correct_answers) + "\n\n"
            result_message += "Incorrect Answers:\n" + "\n".join(incorrect_answers)

            messagebox.showinfo("Quiz Ended", result_message)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred while saving your score: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            question_win.destroy()

    try:
        question_id, question, option1, option2, option3, option4, correct_option = questions[current_question_index]
    except IndexError:
        messagebox.showerror("Error", "No questions available.")
        return

    # Function to break a long question into multiple lines
    def wrap_text(text, max_length=80):
        lines = []
        while len(text) > max_length:
            split_point = text.rfind(' ', 0, max_length)
            if split_point == -1:
                split_point = max_length
            lines.append(text[:split_point])
            text = text[split_point:].lstrip()
        if text:
            lines.append(text)
        return lines

    # Wrap the question text
    wrapped_question = wrap_text(question)

    # Create labels for each wrapped line of the question
    for i, line in enumerate(wrapped_question):
        if i == 0:
            question_label = tk.Label(question_win, text=f"Question {current_question_index + 1}: {line}", font=("Helvetica", 10))
        else:
            question_label = tk.Label(question_win, text=line, font=("Helvetica", 10))
        question_label.pack(pady=5)

    option_var = tk.StringVar(value=selected_answers[current_question_index] if selected_answers[current_question_index] else "")

    tk.Radiobutton(question_win, text=option1, variable=option_var, value="1").pack(anchor="w")
    tk.Radiobutton(question_win, text=option2, variable=option_var, value="2").pack(anchor="w")
    tk.Radiobutton(question_win, text=option3, variable=option_var, value="3").pack(anchor="w")
    tk.Radiobutton(question_win, text=option4, variable=option_var, value="4").pack(anchor="w")

    prev_button = tk.Button(question_win, text="Previous", command=lambda: submit_answer("prev"))
    prev_button.pack(side=tk.LEFT, padx=20, pady=20)

    if current_question_index == len(questions) - 1:
        next_button = tk.Button(question_win, text="Finish", command=lambda: end_quiz(cursor, db, level, username))
    else:
        next_button = tk.Button(question_win, text="Next", command=lambda: submit_answer("next"))
    next_button.pack(side=tk.RIGHT, padx=20, pady=20)

def open_score_page(root, cursor, db, username):
    close_all_windows(root)
    score_win = tk.Toplevel(root)
    score_win.title("Your Quiz Scores")
    score_win.geometry("400x300")

    score_label = tk.Label(score_win, text=f"{username}'s Scores", font=("Helvetica", 16))
    score_label.pack(pady=10)

    try:
        cursor.execute("SELECT quiz_level, score, date_taken FROM score WHERE username = %s ORDER BY date_taken DESC", (username,))
        scores = cursor.fetchall()

        if scores:
            for i, (level, score, date_taken) in enumerate(scores, start=1):
                score_entry = tk.Label(score_win, text=f"{i}. {level.capitalize()} Level - Score: {score} - Date: {date_taken}")
                score_entry.pack(anchor="w", pady=5)
        else:
            no_scores_label = tk.Label(score_win, text="No scores available.", font=("Helvetica", 14))
            no_scores_label.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred while fetching your scores: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main():
    root = tk.Tk()
    root.title("Quiz Application")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="py_project"
    )

    cursor = db.cursor()

    # Placeholder: Replace with the actual logged-in username

def open_welcome_screen(root, cursor, db, username):
    close_all_windows(root)
    welcome_win = tk.Toplevel(root)
    welcome_win.title("Welcome")
    welcome_win.geometry("400x300")

    welcome_label = tk.Label(welcome_win, text=f"Welcome to the Quiz Application, {username}!", font=("Helvetica", 16))
    welcome_label.pack(pady=20)

    start_button = tk.Button(welcome_win, text="Start Quiz", command=lambda: open_quiz_options(root, cursor, db, username))
    start_button.pack(pady=10)

    score_button = tk.Button(welcome_win, text="View Scores", command=lambda: open_score_page(root, cursor, db, username))
    score_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
