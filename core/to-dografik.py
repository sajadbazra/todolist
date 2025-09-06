import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = 'tasks.txt'

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 برنامه To-Do List")
        self.root.geometry("500x450")
        self.root.configure(bg="#f7f7f7")

        self.tasks = []

        title = tk.Label(root, text="لیست کارها", font=("Vazirmatn", 18, "bold"), bg="#f7f7f7", fg="#333")
        title.pack(pady=10)

        self.task_listbox = tk.Listbox(root, width=50, height=12, font=("Vazirmatn", 12), activestyle='dotbox')
        self.task_listbox.pack(pady=10)

        self.entry = tk.Entry(root, width=40, font=("Vazirmatn", 12))
        self.entry.pack(pady=5)

        btn_frame = tk.Frame(root, bg="#f7f7f7")
        btn_frame.pack(pady=10)

        self.add_btn = tk.Button(btn_frame, text="➕ اضافه کردن", width=12, bg="#4CAF50", fg="white",
                                 font=("Vazirmatn", 11), command=self.add_task)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.del_btn = tk.Button(btn_frame, text="🗑 حذف", width=12, bg="#f44336", fg="white",
                                 font=("Vazirmatn", 11), command=self.delete_task)
        self.del_btn.grid(row=0, column=1, padx=5)

        self.toggle_btn = tk.Button(btn_frame, text="✅ تغییر وضعیت", width=12, bg="#2196F3", fg="white",
                                    font=("Vazirmatn", 11), command=self.toggle_done)
        self.toggle_btn.grid(row=0, column=2, padx=5)

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
                display = "✔ " + text
                self.task_listbox.insert(tk.END, display)
                self.task_listbox.itemconfig(tk.END, fg="#888", selectbackground="#d1ffd1")
            else:
                self.task_listbox.insert(tk.END, text)
                self.task_listbox.itemconfig(tk.END, fg="#000", selectbackground="#cce7ff")

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
