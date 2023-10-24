import tkinter as tk
from tkinter import messagebox
import sqlite3

# Создание базы данных SQLite и таблицы "employees"
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()
#Проверка на валидность имени
def alphabet_checker(a):
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
                "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", " "]
    for i in a.lower():
        if i not in alphabet:
            return False
        break
    return True
#Проверка на валидность телефона
def phone_checker(a):
    simbols = ["1","2","3","4","5","6","7","8","9","0","+","-",]
    for i in a:
        if i not in simbols:
            return False
        break
    return True
# Функция для добавления нового сотрудника в базу данных
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if name and phone and email and salary and len(name.split(" ")) == 3 and email[-10::] == "@gmail.com" and salary.isdigit() and (phone[0] == "8" or phone[0:2] == "+7") and (len(phone) == 12 or len(phone) == 11) and alphabet_checker(name) == True:
        cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)',
                       (name, phone, email, salary))
        conn.commit()
        messagebox.showinfo('Успех', 'Сотрудник успешно добавлен в базу данных.')
        clear_entries()
        update_employee_list()
    else:
        print(email[-10::])
        messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля.')


# Функция для изменения сотрудника в базе данных
def update_employee():
    id = selected_employee_id.get()
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if id:
        if name and phone and email and salary:
            cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?',
                           (name, phone, email, salary, id))
            conn.commit()
            messagebox.showinfo('Успех', 'Данные сотрудника успешно обновлены.')
            clear_entries()
            update_employee_list()
        else:
            messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля.')
    else:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите сотрудника для изменения.')


# Функция для удаления сотрудника из базы данных
def delete_employee():
    id = selected_employee_id.get()

    if id:
        confirmed = messagebox.askyesno('Подтверждение', 'Вы уверены, что хотите удалить выбранного сотрудника?')
        if confirmed:
            cursor.execute('DELETE FROM employees WHERE id=?', (id,))
            conn.commit()
            messagebox.showinfo('Успех', 'Сотрудник успешно удален из базы данных.')
            clear_entries()
            update_employee_list()
    else:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите сотрудника для удаления.')


# Функция для поиска сотрудника по ФИО
def search_employee():
    search_name = search_entry.get()

    if search_name:
        cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + search_name + '%',))
        rows = cursor.fetchall()
        if rows:
            employee_listbox.delete(0, tk.END)
            for row in rows:
                employee_listbox.insert(tk.END, f'{row[0]}. {row[1]}')
        else:
            messagebox.showinfo('Уведомление', 'Сотрудники не найдены.')
    else:
        update_employee_list()


# Функция для очистки полей ввода
def clear_entries():
    selected_employee_id.set('')
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)


# Функция для обновления списка сотрудников
def update_employee_list():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    employee_listbox.delete(0, tk.END)
    for row in rows:
        employee_listbox.insert(tk.END, f'{row[0]}. {row[1]}')


# Создание главного окна
root = tk.Tk()
root.title('Список сотрудников компании')

# Создание и размещение элементов интерфейса
selected_employee_id = tk.StringVar()

name_label = tk.Label(root, text='ФИО:')
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

phone_label = tk.Label(root, text='Телефон:')
phone_label.grid(row=1, column=0, padx=10, pady=5)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

email_label = tk.Label(root, text='Email:')
email_label.grid(row=2, column=0, padx=10, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1, padx=10, pady=5)

salary_label = tk.Label(root, text='Заработная плата:')
salary_label.grid(row=3, column=0, padx=10, pady=5)
salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1, padx=10, pady=5)

add_button = tk.Button(root, text='Добавить', command=add_employee)
add_button.grid(row=0, column=2, padx=10, pady=5)

update_button = tk.Button(root, text='Изменить', command=update_employee)
update_button.grid(row=1, column=2, padx=10, pady=5)

delete_button = tk.Button(root, text='Удалить', command=delete_employee)
delete_button.grid(row=2, column=2, padx=10, pady=5)

search_entry = tk.Entry(root)
search_entry.grid(row=4, column=0, padx=10, pady=5)

search_button = tk.Button(root, text='Поиск', command=search_employee)
search_button.grid(row=4, column=1, padx=10, pady=5)

clear_button = tk.Button(root, text='Очистить', command=clear_entries)
clear_button.grid(row=4, column=2, padx=10, pady=5)

employee_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
employee_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
employee_listbox.bind('<<ListboxSelect>>', lambda evt: selected_employee_id.set(
    str(employee_listbox.get(employee_listbox.curselection())).split('.')[0]))

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=5, column=3, sticky='ns')
employee_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=employee_listbox.yview)

# Обновление начального списка сотрудников
update_employee_list()

# Запуск основного цикла приложения
root.mainloop()