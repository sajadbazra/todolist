import tkinter as tk
import jdatetime
import os

TODO_FILE = "todo.txt"

class CalendarWithTodo(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f2f6fc", padx=20, pady=20)
        self.master.title("📅 تقویم شمسی + To-Do List")
        self.grid()
        self.today = jdatetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_day = self.today.day
        self.selected_circle = None
        self.day_circles = []
        self.month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                            'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

        self.build_header()
        self.build_calendar()
        self.build_todo_section()
        self.load_tasks()

    def build_header(self):
        header = tk.Frame(self, bg="#f2f6fc")
        header.grid(row=0, column=0, columnspan=7, pady=(0, 15))

        tk.Label(header, text="ماه:", font=("Helvetica", 13), bg="#f2f6fc").pack(side=tk.LEFT, padx=5)
        self.month_var = tk.StringVar()
        self.month_menu = tk.OptionMenu(header, self.month_var, *self.month_names, command=self.update_calendar)
        self.month_menu.config(font=("Helvetica", 12), bg="#e0ecff", fg="#333", bd=0, highlightthickness=0)
        self.month_menu.pack(side=tk.LEFT, padx=5)
        self.month_var.set(self.month_names[self.current_month - 1])

        tk.Label(header, text=f"سال: {self.current_year}", font=("Helvetica", 13, "bold"), bg="#f2f6fc", fg="#444").pack(side=tk.LEFT, padx=20)

        tk.Button(header, text="امروز", command=self.go_to_today,
                  font=("Helvetica", 12, "bold"), bg="#4da6ff", fg="white", relief="flat",
                  padx=10, pady=2).pack(side=tk.LEFT, padx=10)

    def build_calendar(self):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.canvas = tk.Canvas(self, width=500, height=370, bg="#f2f6fc", highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=7)

        self.day_circles = []
        self.selected_circle = None

        weekdays = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']
        for i, name in enumerate(weekdays[::-1]):
            x = 60 + i * 55
            self.canvas.create_text(x, 25, text=name, font=("Helvetica", 13, "bold"), fill="#333")

        first_day = jdatetime.date(self.current_year, self.current_month, 1)
        start_weekday = first_day.weekday()
        start_col = 6 - start_weekday
        days_in_month = self.get_days_in_month(self.current_year, self.current_month)

        row = 0
        col = start_col

        for day in range(1, days_in_month + 1):
            x = 60 + col * 55
            y = 60 + row * 55

            is_today = (self.today.year == self.current_year and
                        self.today.month == self.current_month and
                        self.today.day == day)

            is_friday = ((6 - col) == 6)
            text_color = "#d22" if is_friday else "#222"
            circle_color = "#ffffff"

            if is_today:
                circle_color = "#a5d6ff"

            circle = self.canvas.create_oval(x-22, y-22, x+22, y+22, fill=circle_color, outline="#cccccc", width=1)
            text = self.canvas.create_text(x, y, text=str(day), font=("Helvetica", 11, "bold"), fill=text_color)

            self.canvas.tag_bind(circle, "<Button-1>", lambda e, d=day, c=circle: self.select_day(d, c))
            self.canvas.tag_bind(text, "<Button-1>", lambda e, d=day, c=circle: self.select_day(d, c))

            self.day_circles.append((circle, text))
            col -= 1
            if col < 0:
                col = 6
                row += 1

    def build_todo_section(self):
        self.todo_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.todo_frame.grid(row=2, column=0, columnspan=7, pady=10, sticky="ew")

        self.todo_title = tk.Label(self.todo_frame, text="", font=("Helvetica", 13, "bold"), bg="#ffffff")
        self.todo_title.pack(anchor="w")

        self.todo_list = tk.Listbox(self.todo_frame, width=50, height=5, font=("Helvetica", 11))
        self.todo_list.pack(pady=5)

        self.todo_entry = tk.Entry(self.todo_frame, font=("Helvetica", 11), width=30)
        self.todo_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(self.todo_frame, text="➕ افزودن", font=("Helvetica", 11),
                  bg="#4CAF50", fg="white", command=self.add_task).pack(side=tk.LEFT)

        tk.Button(self.todo_frame, text="🗑 حذف", font=("Helvetica", 11),
                  bg="#e53935", fg="white", command=self.delete_task).pack(side=tk.LEFT, padx=5)

        tk.Button(self.todo_frame, text="✅ تغییر وضعیت", font=("Helvetica", 11),
                  bg="#039be5", fg="white", command=self.toggle_task).pack(side=tk.LEFT)

    def get_selected_date_str(self):
        return f"{self.current_year:04d}/{self.current_month:02d}/{self.selected_day:02d}"

    def select_day(self, day, circle):
        self.selected_day = day
        if self.selected_circle:
            self.canvas.itemconfig(self.selected_circle, outline="#ccc", width=1)
        self.canvas.itemconfig(circle, outline="#3399ff", width=2, fill="#e0f0ff")
        self.selected_circle = circle
        self.load_tasks()

    def load_tasks(self):
        self.todo_list.delete(0, tk.END)
        self.todo_title.config(text=f"🗓 کارهای روز {self.get_selected_date_str()}")
        if not os.path.exists(TODO_FILE):
            return
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "::" in line:
                    date, task = line.strip().split("::", 1)
                    if date == self.get_selected_date_str():
                        self.todo_list.insert(tk.END, task)

    def save_all_tasks(self, all_lines):
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            f.writelines(all_lines)

    def add_task(self):
        task = self.todo_entry.get().strip()
        if task:
            full_task = f"[ ] {task}"
            with open(TODO_FILE, "a", encoding="utf-8") as f:
                f.write(f"{self.get_selected_date_str()}::{full_task}\n")
            self.todo_entry.delete(0, tk.END)
            self.load_tasks()

    def delete_task(self):
        selection = self.todo_list.curselection()
        if not selection:
            return
        selected_task = self.todo_list.get(selection[0])
        new_lines = []
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if f"{self.get_selected_date_str()}::{selected_task}" not in line.strip():
                    new_lines.append(line)
        self.save_all_tasks(new_lines)
        self.load_tasks()

    def toggle_task(self):
        selection = self.todo_list.curselection()
        if not selection:
            return
        selected_task = self.todo_list.get(selection[0])
        toggled = ""
        if selected_task.startswith("[✓]"):
            toggled = selected_task.replace("[✓]", "[ ]", 1)
        elif selected_task.startswith("[ ]"):
            toggled = selected_task.replace("[ ]", "[✓]", 1)
        else:
            return

        new_lines = []
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if f"{self.get_selected_date_str()}::{selected_task}" in line.strip():
                    new_lines.append(f"{self.get_selected_date_str()}::{toggled}\n")
                else:
                    new_lines.append(line)
        self.save_all_tasks(new_lines)
        self.load_tasks()

    def update_calendar(self, selected_month):
        self.current_month = self.month_names.index(selected_month) + 1
        self.build_calendar()

    def go_to_today(self):
        self.current_month = self.today.month
        self.selected_day = self.today.day
        self.month_var.set(self.month_names[self.current_month - 1])
        self.build_calendar()
        self.load_tasks()

    @staticmethod
    def get_days_in_month(year, month):
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:
            return 30 if jdatetime.date(year, month, 30).is_valid() else 29

# اجرای برنامه
root = tk.Tk()
app = CalendarWithTodo(master=root)
root.mainloop()
