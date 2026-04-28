import tkinter as tk
from tkinter import messagebox
import random
import string
import json

try:
    with open("passwords.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = []

def save_data():
    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def refresh_list():
    history_list.delete(0, tk.END)
    if not data:
        history_list.insert(0, "Нет паролей")
        return
    for i, h in enumerate(data[-8:], 1):
        history_list.insert(tk.END, f"{i}. {h['pwd']} [{h['len']}]")

def get_password():
    # Длина
    if var_len.get() == "короткий":
        length = 8
    elif var_len.get() == "средний":
        length = 12
    else:
        length = 16
    
    # Символы
    chars = ""
    if use_letters.get():
        chars += string.ascii_letters
    if use_numbers.get():
        chars += string.digits
    if use_special.get():
        chars += "!@#$%&*"
    
    if not chars:
        messagebox.showerror("Ошибка", "Что-то выбери!")
        return
    
    pwd = "".join(random.choice(chars) for _ in range(length))
    
    result_label.config(text=pwd)
    
    # Сохраняем
    data.append({"pwd": pwd, "len": length})
    save_data()
    refresh_list()

def copy_password():
    txt = result_label.cget("text")
    if txt and txt != "----":
        root.clipboard_clear()
        root.clipboard_append(txt)
        messagebox.showinfo("Готово", "Скопировано!")

def clear_history():
    if messagebox.askyesno("Очистка", "Удалить всё?"):
        global data
        data = []
        save_data()
        refresh_list()

root = tk.Tk()
root.title("Генератор паролей")
root.geometry("420x520")  # Исправлено: x вместо _

tk.Label(root, text="ГЕНЕРАТОР ПАРОЛЕЙ", font=("Arial", 14, "bold")).pack(pady=10)

# Длина (радиокнопки)
tk.Label(root, text="Длина пароля:").pack()
var_len = tk.StringVar(value="средний")
tk.Radiobutton(root, text="Короткий (8)", variable=var_len, value="короткий").pack()
tk.Radiobutton(root, text="Средний (12)", variable=var_len, value="средний").pack()
tk.Radiobutton(root, text="Длинный (16)", variable=var_len, value="длинный").pack()

# Чекбоксы
use_letters = tk.BooleanVar(value=True)
use_numbers = tk.BooleanVar(value=True)
use_special = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Буквы", variable=use_letters).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Цифры", variable=use_numbers).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Спецсимволы", variable=use_special).pack(anchor="w", padx=40)

tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=get_password, bg="green", fg="white").pack(pady=10)

result_label = tk.Label(root, text="----", font=("Courier", 12, "bold"), fg="blue")
result_label.pack(pady=5)

tk.Button(root, text="КОПИРОВАТЬ", command=copy_password, bg="orange").pack()

tk.Label(root, text="ИСТОРИЯ", font=("Arial", 10, "bold")).pack(pady=5)
history_list = tk.Listbox(root, height=8, width=50)
history_list.pack(pady=5)

tk.Button(root, text="ОЧИСТИТЬ ИСТОРИЮ", command=clear_history, bg="red", fg="white").pack(pady=10)

refresh_list()
root.mainloop()