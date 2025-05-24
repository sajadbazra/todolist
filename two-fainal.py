import tkinter as tk
from tkinter import messagebox

def click_button(value):
    entry.insert(tk.END, value)

def clear_entry():
    entry.delete(0, tk.END)
fg='red'
def calculate():
    try:
        expression = entry.get().replace('×', '*').replace('÷', '/')
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except ZeroDivisionError:
        messagebox.showerror("خطا", "تقسیم بر صفر مجاز نیست.")
        clear_entry()
    except Exception:
        messagebox.showerror("خطا", "ورودی نامعتبر است.")
        clear_entry()

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("ماشین حساب گرافیکی")
root.geometry("300x400")
root.resizable(False, False)

# فیلد ورودی
entry = tk.Entry(root, font=("Arial", 20), borderwidth=3, relief="ridge", justify="right")
entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

# فریم دکمه‌ها
btns_frame = tk.Frame(root)
btns_frame.pack()

buttons = [
    ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('÷', 0, 3),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3),
    ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
    ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
    ('C', 4, 0, 4)  # دکمه پاک‌سازی با عرض بیشتر
]

for btn in buttons:
    text = btn[0]
    row = btn[1]
    col = btn[2]
    colspan = btn[3] if len(btn) == 4 else 1

    if text == '=':
        action = calculate
    elif text == 'C':
        action = clear_entry
    else:
        action = lambda val=text: click_button(val)

    tk.Button(btns_frame, text=text, width=7*colspan, height=2, font=("Arial", 14),
              command=action).grid(row=row, column=col, columnspan=colspan, padx=3, pady=3)

root.mainloop()
