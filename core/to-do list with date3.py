import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import jdatetime
import datetime
import os

FILE_NAME = 'tasks.txt'

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📅 To-Do List با تقویم شمسی")
        self.root.geometry("600x600")
        self.root.configure(bg="#f4f4f4")

        self.tasks = []

        # تقویم میلادی با تبدیل به شمسی
        self.cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd", font=("Vazirmatn", 12))
        self.cal.pack(pady=10)

        self.date_label = tk.Label(root, text="", font=("Vazirmatn", 13, "bold"), bg="#f4f4f4")
        self.date_label.pack(pady=5)

        self.cal.bind("<<CalendarSelected>>", lambda e: self.refresh_tasks())

        # لیست کارها
        self.task_listbox = tk.Listbox(root, width=70, height=12, font=("Vazirmatn", 12))
        self.task_listbox.pack(pady=10)

        # ورود عنوان
        self.entry = tk.Entry(root, width=50, font=("Vazirmatn", 12))
        self.entry.pack(pady=5)

        # دکمه‌ها
        self.btn_frame = tk.Frame(root, bg="#f4f4f4")
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="➕ اضافه", width=12, bg="#4CAF50", fg="white",
                  font=("Vazirmatn", 11), command=self.add_task).grid(row=0, column=0, padx=5)

        tk.Button(self.btn_frame, text="🗑 حذف", width=12, bg="#f44336", fg="white",
                  font=("Vazirmatn", 11), command=self.delete_task).grid(row=0, column=1, padx=5)

        tk.Button(self.btn_frame, text="✅ وضعیت", width=12, bg="#2196F3", fg="white",
                  font=("Vazirmatn", 11), command=self.toggle_done).grid(row=0, column=2, padx=5)

        self.load_tasks()
        self.refresh_tasks()

    def get_selected_date(self):
        miladi = datetime.datetime.strptime(self.cal.get_date(), "%Y-%m-%d").date()
        shamsi = jdatetime.date.fromgregorian(date=miladi)
        return shamsi.strftime("%Y/%m/%d")

    def add_task(self):
        task_text = self.entry.get().strip()
        if not task_text:
            messagebox.showwarning("هشدار", "لطفاً یک عنوان وارد کنید.")
            return
        date_str = self.get_selected_date()
        self.tasks.append({'text': task_text, 'done': False, 'date': date_str})
        self.entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            current_tasks = self.get_filtered_tasks()
            self.tasks.remove(current_tasks[selected[0]])
            self.save_tasks()
            self.refresh_tasks()

    def toggle_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            current_tasks = self.get_filtered_tasks()
            current_tasks[selected[0]]['done'] = not current_tasks[selected[0]]['done']
            self.save_tasks()
            self.refresh_tasks()

    def get_filtered_tasks(self):
        date_str = self.get_selected_date()
        return [task for task in self.tasks if task['date'] == date_str]

    def refresh_tasks(self):
        shamsi = self.get_selected_date()
        self.date_label.config(text=f"🗓 کارهای روز: {shamsi}")

        self.task_listbox.delete(0, tk.END)
        for task in self.get_filtered_tasks():
            display = f"{'✔' if task['done'] else '⬜'} {task['text']} - {task['date']}"
            self.task_listbox.insert(tk.END, display)
            if task['done']:
                self.task_listbox.itemconfig(tk.END, fg="#999", selectbackground="#ccf2d1")
            else:
                self.task_listbox.itemconfig(tk.END, fg="#000", selectbackground="#e1f0ff")

    def save_tasks(self):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for task in self.tasks:
                f.write(f"{task['text']}||{task['done']}||{task['date']}\n")

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('||')
                    if len(parts) == 3:
                        text, done, date = parts
                        self.tasks.append({'text': text, 'done': done == 'True', 'date': date})

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
