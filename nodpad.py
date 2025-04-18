import tkinter as tk
from tkinter import simpledialog, messagebox

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نوت‌پد ساده")

        self.text = tk.Text(root, height=15, width=50)
        self.text.pack(pady=10)

        menu_frame = tk.Frame(root)
        menu_frame.pack()

        tk.Button(menu_frame, text="جستجوی کلمه", command=self.search_word).pack(side=tk.LEFT)
        tk.Button(menu_frame, text="اضافه کردن کلمه", command=self.add_word).pack(side=tk.LEFT)
        tk.Button(menu_frame, text="حذف کردن کلمه", command=self.remove_word).pack(side=tk.LEFT)
        tk.Button(menu_frame, text="ویرایش متن", command=self.edit_text).pack(side=tk.LEFT)

        initial_text = simpledialog.askstring("ورودی اولیه", "متن اولیه را وارد کنید:")
        self.text.insert(tk.END, initial_text)

    def search_word(self):
        word = simpledialog.askstring("جستجوی کلمه", "کلمه‌ای که می‌خواهید جستجو کنید:")
        content = self.text.get("1.0", tk.END).split()
        count = content.count(word)
        messagebox.showinfo("نتیجه جستجو", f"کلمه '{word}' تعداد {count} بار یافت شد.")

    def add_word(self):
        new_word = simpledialog.askstring("اضافه کردن کلمه", "کلمه‌ای که می‌خواهید اضافه کنید:")
        self.text.insert(tk.END, f" {new_word}")

    def remove_word(self):
        word_to_remove = simpledialog.askstring("حذف کردن کلمه", "کلمه‌ای که می‌خواهید حذف کنید:")
        content = self.text.get("1.0", tk.END)
        words = content.split()
        if word_to_remove in words:
            words = [word for word in words if word != word_to_remove]
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, " ".join(words))
            messagebox.showinfo("نتیجه", "کلمه حذف شد.")
        else:
            messagebox.showwarning("هشدار", "کلمه پیدا نشد.")

    def edit_text(self):
        new_text = simpledialog.askstring("ویرایش متن", "متن جدید را وارد کنید:")
        if new_text is not None:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, new_text)


if __name__ == '__main__':
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()