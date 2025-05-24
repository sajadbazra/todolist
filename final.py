import tkinter as tk
from tkinter import messagebox

def calculate(operation):
    try:
        num1 = int(entry1.get())
        num2 = int(entry2.get())
        result = 0

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                messagebox.showerror("خطا", "عدد وارد کن صفر نمیشه")
            result = num1 / num2

        result_label.config(text=f"نتیجه: {result}")
    except ValueError:
        messagebox.showerror("خطا", "فقط عدد بزنید.")

root = tk.Tk()
root.title("ماشین حساب")
root.geometry("350x350")

tk.Label(root, text="عدد اول:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="عدد دوم:").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Button(root, text="+ جمع", width=15, command=lambda: calculate('+')).pack(pady=7)
tk.Button(root, text="- تفریق", width=20, command=lambda: calculate('-')).pack(pady=7)
tk.Button(root, text="× ضرب", width=15, command=lambda: calculate('*')).pack(pady=7)
tk.Button(root, text="÷ تقسیم", width=20, command=lambda: calculate('/')).pack(pady=7)

result_label = tk.Label(root, text="خروجی:")
result_label.pack(pady=10)
root.mainloop()