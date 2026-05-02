import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from taskhub_cli import load_tasks


CLI_SCRIPT = Path(__file__).resolve().with_name("taskhub_cli.py")


def run_cli_command(*args):
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        message = result.stderr.strip() or "Команду CLI не вдалося виконати."
        messagebox.showerror("Помилка CLI", message)
        return

    refresh_list()


def refresh_list():
    listbox.delete(0, tk.END)
    tasks = load_tasks()

    for i, task in enumerate(tasks, start=1):
        status = "✓" if task.get("done") else " "
        listbox.insert(tk.END, f"{i}. [{status}] {task.get('text', '')}")


def add_task_gui():
    text = entry.get().strip()

    if text == "":
        messagebox.showwarning("Помилка", "Текст завдання не може бути порожнім!")
        return

    run_cli_command("add", text)
    entry.delete(0, tk.END)


def get_selected_index():
    selected = listbox.curselection()

    if not selected:
        return None

    return selected[0] + 1


def delete_task_gui():
    index = get_selected_index()

    if index is None:
        messagebox.showwarning("Помилка", "Оберіть завдання для видалення!")
        return

    answer = messagebox.askyesno("Підтвердження", "Видалити вибране завдання?")
    if answer:
        run_cli_command("delete", str(index))


def edit_task_gui():
    index = get_selected_index()

    if index is None:
        messagebox.showwarning("Помилка", "Оберіть завдання для редагування!")
        return

    text = entry.get().strip()

    if text == "":
        messagebox.showwarning("Помилка", "Новий текст завдання не може бути порожнім!")
        return

    run_cli_command("edit", str(index), text)
    entry.delete(0, tk.END)


def done_task_gui():
    index = get_selected_index()

    if index is None:
        messagebox.showwarning("Помилка", "Оберіть завдання для позначення виконаним!")
        return

    run_cli_command("done", str(index))


def clear_tasks_gui():
    tasks = load_tasks()

    if not tasks:
        messagebox.showinfo("Інформація", "Список завдань уже порожній.")
        return

    answer = messagebox.askyesno("Підтвердження", "Видалити всі завдання?")
    if answer:
        run_cli_command("clear")


def insert_selected_task_to_entry(event):
    index = get_selected_index()

    if index is None:
        return

    tasks = load_tasks()
    entry.delete(0, tk.END)
    entry.insert(0, tasks[index - 1].get("text", ""))


root = tk.Tk()
root.title("TaskHub GUI")
root.geometry("560x460")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="TaskHub - графічний список завдань",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12), width=48)
entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Додати", width=14, command=add_task_gui)
add_button.grid(row=0, column=0, padx=5, pady=5)

edit_button = tk.Button(button_frame, text="Редагувати", width=14, command=edit_task_gui)
edit_button.grid(row=0, column=1, padx=5, pady=5)

done_button = tk.Button(button_frame, text="Виконано", width=14, command=done_task_gui)
done_button.grid(row=0, column=2, padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Видалити", width=14, command=delete_task_gui)
delete_button.grid(row=1, column=0, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Очистити", width=14, command=clear_tasks_gui)
clear_button.grid(row=1, column=1, padx=5, pady=5)

exit_button = tk.Button(button_frame, text="Вихід", width=14, command=root.destroy)
exit_button.grid(row=1, column=2, padx=5, pady=5)

listbox = tk.Listbox(root, font=("Arial", 12), width=60, height=13)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", insert_selected_task_to_entry)

info_label = tk.Label(
    root,
    text="Для редагування оберіть завдання, змініть текст у полі та натисніть 'Редагувати'.",
    font=("Arial", 9)
)
info_label.pack(pady=5)

refresh_list()

root.mainloop()
