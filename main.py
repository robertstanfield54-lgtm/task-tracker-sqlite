# main.py
from datetime import datetime
from typing import Optional
import db


def prompt_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_value <= value <= max_value:
                return value
            print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Please enter a valid whole number.")


def prompt_date(prompt: str) -> Optional[str]:
    """
    Accepts YYYY-MM-DD or blank for none.
    Returns ISO date string or None.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Date must be in YYYY-MM-DD format (example: 2026-01-15). Or leave blank.")


def print_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.\n")
        return

    print("\nID  Done  Pri  Due Date     Title")
    print("--  ----  ---  ----------  ------------------------------")
    for t in tasks:
        done = "Yes" if t["completed"] == 1 else "No"
        due = t["due_date"] if t["due_date"] else "—"
        print(f'{t["id"]:<3} {done:<5} {t["priority"]:<3} {due:<10}  {t["title"]}')
    print()


def menu():
    print("=== Task Tracker (SQLite) ===")
    print("1) Add task")
    print("2) List tasks (all)")
    print("3) List tasks (open only)")
    print("4) Mark task complete")
    print("5) Delete task")
    print("0) Exit")


def main():
    db.init_db()

    while True:
        menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("Title cannot be empty.\n")
                continue

            due_date = prompt_date("Due date (YYYY-MM-DD) or blank: ")
            priority = prompt_int("Priority (1=high, 5=low): ", 1, 5)

            new_id = db.add_task(title=title, due_date=due_date, priority=priority)
            print(f"Added task with ID {new_id}.\n")

        elif choice == "2":
            tasks = db.list_tasks(show_all=True)
            print_tasks(tasks)

        elif choice == "3":
            tasks = db.list_tasks(show_all=False)
            print_tasks(tasks)

        elif choice == "4":
            task_id = prompt_int("Enter task ID to mark complete: ", 1, 10_000_000)
            ok = db.mark_complete(task_id)
            print("Marked complete.\n" if ok else "Task ID not found.\n")

        elif choice == "5":
            task_id = prompt_int("Enter task ID to delete: ", 1, 10_000_000)
            ok = db.delete_task(task_id)
            print("Deleted.\n" if ok else "Task ID not found.\n")

        elif choice == "6":
            tasks = db.list_due_soon(7)
            print_tasks(tasks)


        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()