import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

PRIORITIES = ["High", "Medium", "Low"]
DEFAULT_CATEGORIES = ["General", "Work", "Personal", "Shopping", "Health"]

class TaskForm(tk.Toplevel):
    def __init__(self, parent, on_save, task=None, theme=None):
        super().__init__(parent)
        self.on_save = on_save
        self.task = task
        self.theme = theme or {}

        mode = "Edit Task" if task else "Add New Task"
        self.title(mode)
        self.geometry("420x320")
        self.resizable(False, False)

        bg = self.theme.get("bg", "#f5f5f5")
        self.configure(bg=bg)
        self._build_ui(bg)

        # Wait for window to be visible BEFORE grab_set
        self.update_idletasks()
        self.lift()
        self.focus_force()
        self.grab_set()  # moved here — after window is actually rendered

        # Pre-fill if editing
        if task:
            self.title_entry.insert(0, task["title"])
            self.category_var.set(task["category"])
            self.priority_var.set(task["priority"])
            if task["due_date"] and task["due_date"] != "-":
                self.due_date_entry.insert(0, task["due_date"])

    def _build_ui(self, bg):
        fg = self.theme.get("label_fg", "#333")
        entry_bg = self.theme.get("entry_bg", "white")
        entry_fg = self.theme.get("entry_fg", "black")
        pad = {"padx": 15, "pady": 5}

        tk.Label(self, text="Task Title *", font=("Arial", 10, "bold"),
                 bg=bg, fg=fg).pack(anchor="w", **pad)
        self.title_entry = tk.Entry(self, font=("Arial", 11), width=42,
                                     bg=entry_bg, fg=entry_fg,
                                     insertbackground=entry_fg)
        self.title_entry.pack(anchor="w", padx=15)
        self.title_entry.focus()

        tk.Label(self, text="Category", font=("Arial", 10, "bold"),
                 bg=bg, fg=fg).pack(anchor="w", **pad)
        self.category_var = tk.StringVar(value="General")
        ttk.Combobox(self, textvariable=self.category_var,
                     values=DEFAULT_CATEGORIES, width=22).pack(anchor="w", padx=15)

        tk.Label(self, text="Priority", font=("Arial", 10, "bold"),
                 bg=bg, fg=fg).pack(anchor="w", **pad)
        self.priority_var = tk.StringVar(value="Medium")
        pf = tk.Frame(self, bg=bg)
        pf.pack(anchor="w", padx=15)
        for p in PRIORITIES:
            tk.Radiobutton(pf, text=p, variable=self.priority_var,
                           value=p, font=("Arial", 10),
                           bg=bg, fg=fg,
                           selectcolor=entry_bg).pack(side="left", padx=5)

        tk.Label(self, text="Due Date (YYYY-MM-DD)", font=("Arial", 10, "bold"),
                 bg=bg, fg=fg).pack(anchor="w", **pad)
        self.due_date_entry = tk.Entry(self, font=("Arial", 11), width=22,
                                        bg=entry_bg, fg=entry_fg,
                                        insertbackground=entry_fg)
        self.due_date_entry.pack(anchor="w", padx=15)

        label = "Save Changes" if self.task else "Add Task"
        tk.Button(self, text=label, command=self._save,
                  bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"), width=16).pack(pady=15)

    def _save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Missing", "Task title can't be empty.", parent=self)
            return

        due_date = self.due_date_entry.get().strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Use format YYYY-MM-DD", parent=self)
                return

        self.on_save(
            title=title,
            category=self.category_var.get(),
            priority=self.priority_var.get(),
            due_date=due_date
        )
        self.destroy()