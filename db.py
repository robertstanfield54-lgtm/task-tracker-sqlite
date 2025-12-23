# db.py
import sqlite3
from typing import Optional, List, Dict, Any

DB_NAME = "tasks.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                priority INTEGER DEFAULT 3,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        conn.commit()


def add_task(title: str, due_date: Optional[str], priority: int) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO tasks (title, due_date, priority, completed)
            VALUES (?, ?, ?, 0);
            """,
            (title, due_date, priority),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_tasks(show_all: bool = True) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        if show_all:
            cur = conn.execute(
                """
                SELECT id, title, due_date, priority, completed, created_at
                FROM tasks
                ORDER BY completed ASC, priority ASC, due_date ASC, id ASC;
                """
            )
        else:
            cur = conn.execute(
                """
                SELECT id, title, due_date, priority, completed, created_at
                FROM tasks
                WHERE completed = 0
                ORDER BY priority ASC, due_date ASC, id ASC;
                """
            )

        rows = cur.fetchall()
        return [dict(r) for r in rows]

def list_due_soon(days: int = 7) -> List[Dict[str, Any]]:
    """
    List open tasks due within the next N days.
    due_date must be stored as YYYY-MM-DD.
    """
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, title, due_date, priority, completed, created_at
            FROM tasks
            WHERE completed = 0
              AND due_date IS NOT NULL
              AND date(due_date) <= date('now', ?)
            ORDER BY date(due_date) ASC, priority ASC, id ASC;
            """,
            (f"+{days} days",),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def mark_complete(task_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?;",
            (task_id,),
        )
        conn.commit()
        return cur.rowcount == 1


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM tasks WHERE id = ?;",
            (task_id,),
        )
        conn.commit()
        return cur.rowcount == 1
