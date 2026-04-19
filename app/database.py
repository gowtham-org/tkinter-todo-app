import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            category    TEXT DEFAULT 'General',
            priority    TEXT DEFAULT 'Medium',
            due_date    TEXT DEFAULT NULL,
            done        INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, category, priority, due_date, done
        FROM tasks
        ORDER BY
            done ASC,
            CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END,
            due_date ASC
    ''')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title, category, priority, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, category, priority, due_date) VALUES (?, ?, ?, ?)",
        (title, category, priority, due_date or None)
    )
    conn.commit()
    conn.close()

def mark_done(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM tasks")
    cats = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cats

def update_task(task_id, title, category, priority, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title=?, category=?, priority=?, due_date=?
        WHERE id=?
    ''', (title, category, priority, due_date or None, task_id))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=1")
    done = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=0")
    pending = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=0 AND due_date < date('now')")
    overdue = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE priority='High' AND done=0")
    high = cursor.fetchone()[0]
    conn.close()
    return {
        "Total": total,
        "Done": done,
        "Pending": pending,
        "Overdue": overdue,
        "High Priority": high
    }