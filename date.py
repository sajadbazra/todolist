import tkinter as tk
import jdatetime

class RoundCalendar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f2f6fc", padx=20, pady=20)
        self.master.title("📅 تقویم شمسی زیبا و گرد")
        self.grid()
        self.today = jdatetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_day = None
        self.selected_circle = None
        self.day_circles = []
        self.month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                            'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        self.build_header()
        self.build_calendar()

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

            self.canvas.tag_bind(circle, "<Enter>", lambda e, c=circle: self.canvas.itemconfig(c, fill="#e6f0ff"))
            self.canvas.tag_bind(circle, "<Leave>", lambda e, c=circle, d=day: self.reset_hover(c, d))
            self.canvas.tag_bind(text, "<Enter>", lambda e, c=circle: self.canvas.itemconfig(c, fill="#e6f0ff"))
            self.canvas.tag_bind(text, "<Leave>", lambda e, c=circle, d=day: self.reset_hover(c, d))

            self.canvas.tag_bind(circle, "<Button-1>", lambda e, d=day, c=circle: self.select_day(d, c))
            self.canvas.tag_bind(text, "<Button-1>", lambda e, d=day, c=circle: self.select_day(d, c))

            self.day_circles.append((circle, text))
            col -= 1
            if col < 0:
                col = 6
                row += 1

    def reset_hover(self, circle, day):
        if self.selected_circle == circle:
            self.canvas.itemconfig(circle, fill="#e0f0ff")
        elif (self.today.year == self.current_year and
              self.today.month == self.current_month and
              self.today.day == day):
            self.canvas.itemconfig(circle, fill="#a5d6ff")
        else:
            self.canvas.itemconfig(circle, fill="#ffffff")

    def select_day(self, day, circle):
        self.selected_day = day
        if self.selected_circle:
            self.canvas.itemconfig(self.selected_circle, outline="#ccc", width=1)
        self.canvas.itemconfig(circle, outline="#3399ff", width=2, fill="#e0f0ff")
        self.selected_circle = circle
        print(f"روز انتخاب‌شده: {self.current_year}/{self.current_month}/{day}")

    def update_calendar(self, selected_month):
        self.current_month = self.month_names.index(selected_month) + 1
        self.build_calendar()

    def go_to_today(self):
        self.current_month = self.today.month
        self.month_var.set(self.month_names[self.current_month - 1])
        self.build_calendar()

    @staticmethod
    def get_days_in_month(year, month):
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:
            return 30 if jdatetime.date(year, month, 30).is_valid() else 29

# اجرای تقویم
root = tk.Tk()
calendar = RoundCalendar(master=root)
root.mainloop()
