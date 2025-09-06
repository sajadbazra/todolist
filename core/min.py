import tkinter as tk
from tkinter import messagebox, simpledialog
import os

FILE_NAME = 'tasks.txt'

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامه To-Do List")

        self.tasks = []

        self.task_listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="اضافه کردن کار", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="حذف کار", command=self.delete_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="تغییر وضعیت انجام", command=self.toggle_done).grid(row=0, column=2, padx=5)

        self.load_tasks()

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            self.tasks.append({'text': task_text, 'done': False})
            self.entry.delete(0, tk.END)
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("هشدار", "لطفا یک عنوان برای کار وارد کنید.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("هشدار", "لطفا یک کار را برای حذف انتخاب کنید.")

    def toggle_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]['done'] = not self.tasks[index]['done']
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("هشدار", "لطفا یک کار را انتخاب کنید.")

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            text = task['text']
            if task['done']:
                text = "✔ " + text
            self.task_listbox.insert(tk.END, text)

    def save_tasks(self):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            for task in self.tasks:
                line = f"{task['text']}||{task['done']}\n"
                f.write(line)

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('||')
                    if len(parts) == 2:
                        text, done = parts
                        self.tasks.append({'text': text, 'done': done == 'True'})
        self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
