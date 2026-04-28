import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.filename = "expenses.json"
        self.expenses = self.load_data()

        # UI элементы
        self.create_widgets()
        self.update_table(self.expenses)

    def create_widgets(self):
        # Поля ввода
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0)
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(frame_input, text="Категория:").grid(row=1, column=0)
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.combo_category.grid(row=1, column=1)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=2, column=1)

        tk.Button(frame_input, text="Добавить расход", command=self.add_expense).grid(row=3, columnspan=2, pady=10)

        # Фильтры
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация и Итоги", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10)

        tk.Label(frame_filter, text="Категория:").pack(side="left")
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.filter_cat.set("Все")
        self.filter_cat.pack(side="left", padx=5)

        tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter).pack(side="left", padx=5)
        
        self.label_total = tk.Label(frame_filter, text="Итого: 0", font=('Arial', 10, 'bold'))
        self.label_total.pack(side="right")

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combo_category.get()
        date_str = self.entry_date.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность суммы (>0) и даты (ГГГГ-ММ-ДД)")
            return

        if not category:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return

        new_expense = {"amount": amount, "category": category, "date": date_str}
        self.expenses.append(new_expense)
        self.save_data()
        self.apply_filter()
        
        # Очистка полей
        self.entry_amount.delete(0, tk.END)

    def apply_filter(self):
        cat = self.filter_cat.get()
        filtered = [e for e in self.expenses if cat == "Все" or e['category'] == cat]
        self.update_table(filtered)

    def update_table(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        total = 0
        for e in data:
            self.tree.insert("", "end", values=(e['amount'], e['category'], e['date']))
            total += e['amount']
        
        self.label_total.config(text=f"Итого: {total:.2f}")

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
