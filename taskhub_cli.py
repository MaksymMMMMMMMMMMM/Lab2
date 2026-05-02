import argparse
import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(tasks, list):
        return []

    return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def add_task(text):
    text = text.strip()

    if not text:
        print("Помилка: текст завдання не може бути порожнім.", file=sys.stderr)
        return False

    tasks = load_tasks()
    tasks.append({
        "text": text,
        "done": False
    })
    save_tasks(tasks)
    return True


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("Список завдань порожній.")
        return True

    for i, task in enumerate(tasks, start=1):
        status = "виконано" if task.get("done") else "не виконано"
        print(f"{i}. {task.get('text', '')} - {status}")

    return True


def delete_task(index):
    tasks = load_tasks()

    if index < 1 or index > len(tasks):
        print("Помилка: завдання з таким номером не існує.", file=sys.stderr)
        return False

    tasks.pop(index - 1)
    save_tasks(tasks)
    return True


def edit_task(index, new_text):
    new_text = new_text.strip()

    if not new_text:
        print("Помилка: новий текст завдання не може бути порожнім.", file=sys.stderr)
        return False

    tasks = load_tasks()

    if index < 1 or index > len(tasks):
        print("Помилка: завдання з таким номером не існує.", file=sys.stderr)
        return False

    tasks[index - 1]["text"] = new_text
    save_tasks(tasks)
    return True


def mark_done(index):
    tasks = load_tasks()

    if index < 1 or index > len(tasks):
        print("Помилка: завдання з таким номером не існує.", file=sys.stderr)
        return False

    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    return True


def clear_tasks():
    save_tasks([])
    return True


def main():
    parser = argparse.ArgumentParser(description="TaskHub CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Додати нове завдання")
    add_parser.add_argument("text", help="Текст завдання")

    subparsers.add_parser("list", help="Показати список завдань")

    delete_parser = subparsers.add_parser("delete", help="Видалити завдання")
    delete_parser.add_argument("index", type=int, help="Номер завдання")

    edit_parser = subparsers.add_parser("edit", help="Редагувати завдання")
    edit_parser.add_argument("index", type=int, help="Номер завдання")
    edit_parser.add_argument("text", help="Новий текст завдання")

    done_parser = subparsers.add_parser("done", help="Позначити завдання виконаним")
    done_parser.add_argument("index", type=int, help="Номер завдання")

    subparsers.add_parser("clear", help="Очистити список завдань")

    args = parser.parse_args()
    success = True

    if args.command == "add":
        success = add_task(args.text)
    elif args.command == "list":
        success = list_tasks()
    elif args.command == "delete":
        success = delete_task(args.index)
    elif args.command == "edit":
        success = edit_task(args.index, args.text)
    elif args.command == "done":
        success = mark_done(args.index)
    elif args.command == "clear":
        success = clear_tasks()
    else:
        parser.print_help()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
