from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import uuid

# File where tasks are stored (project_root/tasks.json)
TASKS_FILE = (Path(__file__).resolve().parents[1] / "tasks.json")

DATE_FMT = "%Y-%m-%d"

@dataclass
class Task:
    id: str
    title: str
    created_at: str
    due_date: Optional[str] = None  # YYYY-MM-DD
    priority: int = 3               # 1 (high) to 5 (low)
    completed: bool = False

def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_tasks() -> List[Task]:
    if not TASKS_FILE.exists():
        return []
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        return [Task(**item) for item in data]
    except Exception:
        # If file is corrupted, back it up and start fresh
        backup = TASKS_FILE.with_suffix(".bak.json")
        TASKS_FILE.rename(backup)
        return []

def save_tasks(tasks: List[Task]) -> None:
    TASKS_FILE.write_text(
        json.dumps([asdict(t) for t in tasks], ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def add_task(title: str, due_date: Optional[str] = None, priority: int = 3) -> Task:
    tasks = load_tasks()
    task = Task(
        id=str(uuid.uuid4()),
        title=title.strip(),
        created_at=_now_str(),
        due_date=due_date,
        priority=priority,
        completed=False
    )
    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks(show_completed: Optional[bool] = None) -> List[Task]:
    tasks = load_tasks()
    if show_completed is None:
        return tasks
    return [t for t in tasks if t.completed == show_completed]

def complete_task(task_id: str) -> bool:
    tasks = load_tasks()
    changed = False
    for t in tasks:
        if t.id.startswith(task_id):
            t.completed = True
            changed = True
            break
    if changed:
        save_tasks(tasks)
    return changed

def delete_task(task_id: str) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if not t.id.startswith(task_id)]
    if len(new_tasks) != len(tasks):
        save_tasks(new_tasks)
        return True
    return False

def parse_due_date(s: str) -> Optional[str]:
    s = s.strip()
    if not s:
        return None
    try:
        dt = datetime.strptime(s, DATE_FMT)
        return dt.strftime(DATE_FMT)
    except ValueError:
        return None

def input_int(prompt: str, default: int) -> int:
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        val = int(raw)
        return min(5, max(1, val))
    except ValueError:
        return default

def print_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("No tasks yet. Add one!")
        return
    # Sort: incomplete first, then by due date, then priority, then created_at
    def sort_key(t: Task):
        due = t.due_date or "9999-12-31"
        return (t.completed, due, t.priority, t.created_at)
    tasks_sorted = sorted(tasks, key=sort_key)
    # Header
    print(f"{'ID':8} {'Title':30} {'Due':10} {'Pri':3} {'Status':9} {'Created'}")
    print("-"*80)
    for t in tasks_sorted:
        short_id = t.id.split("-")[0]
        title = (t.title[:27] + "...") if len(t.title) > 30 else t.title
        due = t.due_date or "-"
        pri = t.priority
        status = "done" if t.completed else "todo"
        print(f"{short_id:8} {title:30} {due:10} {pri:<3} {status:9} {t.created_at}")

def menu() -> None:
    while True:
        print("\nTask Tracker")
        print("1) Add task")
        print("2) List tasks")
        print("3) Complete task")
        print("4) Delete task")
        print("5) List only TODO")
        print("6) List only DONE")
        print("0) Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            due = parse_due_date(input("Due date (YYYY-MM-DD, optional): "))
            pri = input_int("Priority (1=high..5=low, default 3): ", 3)
            task = add_task(title, due, pri)
            print(f"Added task {task.title} (id={task.id.split('-')[0]}).")
        elif choice == "2":
            print_tasks(list_tasks())
        elif choice == "3":
            tid = input("Enter task id (you can paste the short id): ").strip()
            ok = complete_task(tid)
            print("Marked complete." if ok else "Task not found.")
        elif choice == "4":
            tid = input("Enter task id to delete: ").strip()
            ok = delete_task(tid)
            print("Deleted." if ok else "Task not found.")
        elif choice == "5":
            print_tasks(list_tasks(show_completed=False))
        elif choice == "6":
            print_tasks(list_tasks(show_completed=True))
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    # Ensure data file exists
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        save_tasks([])
    menu()
