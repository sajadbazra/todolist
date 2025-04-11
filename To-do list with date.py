import tkinter as tk
from tkinter import messagebox, ttk
import jdatetime
import os

FILE_NAME = 'tasks.txt'
WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 برنامه To-Do با Combobox")
        self.root.geometry("600x530")
        self.root.configure(bg="#f2f2f2")

        self.tasks = []

        tk.Label(root, text="برنامه‌ریزی هفتگی", font=("Vazirmatn", 18, "bold"), bg="#f2f2f2").pack(pady=10)

        # Combobox انتخاب روز
        self.day_selector = ttk.Combobox(root, values=WEEKDAYS, font=("Vazirmatn", 12), state="readonly", width=20)
        self.day_selector.pack(pady=5)
        self.day_selector.current(0)
        self.day_selector.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        # لیست کارها
        self.task_listbox = tk.Listbox(root, width=70, height=12, font=("Vazirmatn", 12))
        self.task_listbox.pack(pady=10)

        # ورود عنوان
        self.entry = tk.Entry(root, width=50, font=("Vazirmatn", 12))
        self.entry.pack(pady=5)

        # دکمه‌ها
        self.btn_frame = tk.Frame(root, bg="#f2f2f2")
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
        today = jdatetime.date.today()
        current_day_index = today.weekday()
        selected_day_index = self.day_selector.current()
        delta = selected_day_index - current_day_index
        return today + jdatetime.timedelta(days=delta)

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            task_date = self.get_selected_date().strftime("%Y/%m/%d")
            self.tasks.append({'text': task_text, 'done': False, 'date': task_date})
            self.entry.delete(0, tk.END)
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("هشدار", "لطفاً یک عنوان وارد کنید.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            current_tasks = self.get_filtered_tasks()
            index = self.tasks.index(current_tasks[selected[0]])
            del self.tasks[index]
            self.save_tasks()
            self.refresh_tasks()

    def toggle_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            current_tasks = self.get_filtered_tasks()
            task = current_tasks[selected[0]]
            task['done'] = not task['done']
            self.save_tasks()
            self.refresh_tasks()

    def get_filtered_tasks(self):
        selected_date = self.get_selected_date().strftime("%Y/%m/%d")
        return [task for task in self.tasks if task['date'] == selected_date]

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.get_filtered_tasks():
            display = f"{'✔' if task['done'] else '⬜'} {task['text']} - {task['date']}"
            self.task_listbox.insert(tk.END, display)
            if task['done']:
                self.task_listbox.itemconfig(tk.END, fg="#888", selectbackground="#ccf2d1")
            else:
                self.task_listbox.itemconfig(tk.END, fg="#000", selectbackground="#e1f0ff")

    def save_tasks(self):
        with open(FILE_NAME,  'w', encoding='utf-8') as f:
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
