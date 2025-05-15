import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

# ----- Database Setup -----
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS report_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        subject TEXT NOT NULL,
        marks INTEGER NOT NULL
    )
''')
conn.commit()

# ----- Global Dictionary -----
student_data = {}

# ----- Functions -----
def add_subject():
    subject = subject_entry.get()
    try:
        marks = int(marks_entry.get())
        student_data[subject] = marks
        subjects_display.insert(tk.END, f"{subject}: {marks}\n")
        subject_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid marks.")

def generate_report():
    name = name_entry.get()
    roll = roll_entry.get()

    if not name or not roll or not student_data:
        messagebox.showerror("Missing Data", "Please fill all fields and add at least one subject.")
        return

    for subject, mark in student_data.items():
        cursor.execute('''
            INSERT INTO report_cards (name, roll_no, subject, marks)
            VALUES (?, ?, ?, ?)
        ''', (name, roll, subject, mark))
    conn.commit()

    messagebox.showinfo("Success", "Report card saved to database.")
    student_data.clear()
    subjects_display.delete("1.0", tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)

def view_reports():
    view_window = tk.Toplevel(root)
    view_window.title("Saved Reports")
    view_window.geometry("400x400")

    text_area = scrolledtext.ScrolledText(view_window, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT name, roll_no, subject, marks FROM report_cards")
    records = cursor.fetchall()

    if not records:
        text_area.insert(tk.END, "No records found.\n")
    else:
        current_student = ("", "")
        for name, roll, subject, mark in records:
            if (name, roll) != current_student:
                text_area.insert(tk.END, f"\n{name} (Roll No: {roll})\n")
                current_student = (name, roll)
            text_area.insert(tk.END, f" - {subject}: {mark}\n")

# ----- GUI Setup -----
root = tk.Tk()
root.title("Student Report Card")
root.geometry("400x500")

tk.Label(root, text="Student Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Roll Number").pack()
roll_entry = tk.Entry(root)
roll_entry.pack()

tk.Label(root, text="Subject").pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

tk.Label(root, text="Marks").pack()
marks_entry = tk.Entry(root)
marks_entry.pack()

tk.Button(root, text="Add Subject", command=add_subject).pack(pady=5)

subjects_display = tk.Text(root, height=10, width=40)
subjects_display.pack(pady=5)

tk.Button(root, text="Generate Report", command=generate_report).pack(pady=5)
tk.Button(root, text="View All Reports", command=view_reports).pack(pady=5)

root.mainloop()
conn.close()
