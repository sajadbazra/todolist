import tkinter as tk
from tkinter import ttk, messagebox
import jdatetime
import os

FILE_NAME = 'tasks.txt'
WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List سجاد بزرا")
        self.root.geometry("650x550")
        self.root.configure(bg="#f4f4f4")

        self.tasks = []
        self.tab_objects = {}
        self.tab_selected_index = 0

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', pady=10)

        for i, day in enumerate(WEEKDAYS):
            frame = tk.Frame(self.notebook, bg="#fefefe")
            self.notebook.add(frame, text=day)
            self.tab_objects[i] = {
                'frame': frame,
                'listbox': tk.Listbox(frame, width=70, height=12, font=("Vazirmatn", 12)),
                'entry': tk.Entry(frame, width=50, font=("Vazirmatn", 12))
            }

            self.tab_objects[i]['listbox'].pack(pady=10)
            self.tab_objects[i]['entry'].pack(pady=5)

            btn_frame = tk.Frame(frame, bg="#fefefe")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="اضافه", width=12, bg="#4CAF50", fg="white",
                      font=("Vazirmatn", 11), command=lambda i=i: self.add_task(i)).grid(row=0, column=0, padx=5)
            tk.Button(btn_frame, text="حذف", width=12, bg="#f44336", fg="white",
                      font=("Vazirmatn", 11), command=lambda i=i: self.delete_task(i)).grid(row=0, column=1, padx=5)
            tk.Button(btn_frame, text="تغییر وضعیت", width=12, bg="#2196F3", fg="white",
                      font=("Vazirmatn", 11), command=lambda i=i: self.toggle_done(i)).grid(row=0, column=2, padx=5)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.load_tasks()
        self.refresh_all_tabs()

    def get_selected_date_by_index(self, index):
        today = jdatetime.date.today()
        current_index = today.weekday()
        delta = index - current_index
        return today + jdatetime.timedelta(days=delta)

    def on_tab_changed(self, event):
        self.tab_selected_index = self.notebook.index(self.notebook.select())
        self.refresh_tab(self.tab_selected_index)

    def add_task(self, index):
        entry = self.tab_objects[index]['entry']
        text = entry.get().strip()
        if not text:
            messagebox.showwarning("هشدار", "لطفاً عنوان وارد کنید.")
            return
        date_str = self.get_selected_date_by_index(index).strftime("%Y/%m/%d")
        self.tasks.append({'text': text, 'done': False, 'date': date_str})
        entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_tab(index)

    def delete_task(self, index):
        listbox = self.tab_objects[index]['listbox']
        selected = listbox.curselection()
        if selected:
            task = self.get_filtered_tasks(index)[selected[0]]
            self.tasks.remove(task)
            self.save_tasks()
            self.refresh_tab(index)

    def toggle_done(self, index):
        listbox = self.tab_objects[index]['listbox']
        selected = listbox.curselection()
        if selected:
            task = self.get_filtered_tasks(index)[selected[0]]
            task['done'] = not task['done']
            self.save_tasks()
            self.refresh_tab(index)

    def get_filtered_tasks(self, index):
        date_str = self.get_selected_date_by_index(index).strftime("%Y/%m/%d")
        return [task for task in self.tasks if task['date'] == date_str]

    def refresh_tab(self, index):
        listbox = self.tab_objects[index]['listbox']
        listbox.delete(0, tk.END)
        for task in self.get_filtered_tasks(index):
            display = f"{'✔' if task['done'] else '⬜'} {task['text']} - {task['date']}"
            listbox.insert(tk.END, display)
            if task['done']:
                listbox.itemconfig(tk.END, fg="#999", selectbackground="#ccf2d1")
            else:
                listbox.itemconfig(tk.END, fg="#000", selectbackground="#dceeff")

    def refresh_all_tabs(self):
        for i in range(7):
            self.refresh_tab(i)

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
