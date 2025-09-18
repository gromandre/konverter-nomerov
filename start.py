import re
import tkinter as tk
from tkinter import messagebox

def normalize_phone(digits: str) -> str:
    digits = re.sub(r"\D", "", digits)
    if not digits:
        return ""
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    elif len(digits) == 11 and digits.startswith("7"):
        pass
    elif len(digits) == 10:
        digits = "7" + digits
    else:
        return ""
    return digits

def extract_phones_from_line(line: str) -> list:
    result = []
    # добавляем все виды тире/дефисов, включая необычные (‑, –, —, ‒)
    candidates = re.findall(r"[+\d\(\)\s\-\–\—\‒\‑]{5,}", line)
    for cand in candidates:
        groups = re.findall(r"\d+", cand)
        i = 0
        while i < len(groups):
            found = None
            for k in range(i, len(groups)):
                comb = "".join(groups[i:k+1])
                if 10 <= len(comb) <= 11:
                    found = comb
                    i = k + 1
                    break
                if len(comb) > 11:
                    break
            if not found:
                grp = groups[i]
                if 10 <= len(grp) <= 11:
                    found = grp
                i += 1
            if found:
                norm = normalize_phone(found)
                if norm:
                    result.append(norm)
    return result



def format_numbers():
    raw_text = left_text.get("1.0", tk.END)
    phones = []
    seen = set()
    for line in raw_text.splitlines():
        for phone in extract_phones_from_line(line):
            if phone not in seen:
                phones.append(phone)
                seen.add(phone)
    # выводим результат
    right_text.delete("1.0", tk.END)
    if phones:
        right_text.insert(tk.END, "\n".join(phones))
    else:
        messagebox.showinfo("Результат", "Не найдено ни одного номера.")

def copy_to_clipboard():
    formatted = right_text.get("1.0", tk.END).strip()
    if formatted:
        root.clipboard_clear()
        root.clipboard_append(formatted)
        messagebox.showinfo("Скопировано", "Форматированные номера скопированы в буфер обмена!")
    else:
        messagebox.showwarning("Пусто", "Нет данных для копирования.")

# GUI
root = tk.Tk()
root.title("Форматирование телефонов")
root.geometry("800x500")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Левое поле (ввод)
left_label = tk.Label(frame, text="Вставьте список номеров")
left_label.grid(row=0, column=0, padx=5, pady=5)

left_text = tk.Text(frame, wrap="word")
left_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Правое поле (результат)
right_label = tk.Label(frame, text="Форматированные номера")
right_label.grid(row=0, column=1, padx=5, pady=5)

right_text = tk.Text(frame, wrap="word")
right_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Кнопки
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

format_btn = tk.Button(btn_frame, text="Форматировать →", command=format_numbers)
format_btn.pack(side="left", padx=10)

copy_btn = tk.Button(btn_frame, text="Скопировать в буфер", command=copy_to_clipboard)
copy_btn.pack(side="left", padx=10)

# Адаптивная сетка
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

root.mainloop()
