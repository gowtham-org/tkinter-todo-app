import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
import csv
import database
from ui.task_form import TaskForm
from ui.dashboard import Dashboard
from theme import THEMES


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo Manager")
        self.root.geometry("900x600")
        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()
        self.dark_mode = False
        self.theme = THEMES["light"]

        self.search_var.trace_add("write", lambda *_: self.load_tasks())

        self._build_ui()
        self.load_tasks()

    # ── UI CONSTRUCTION ──────────────────────────────────────────────

    def _build_ui(self):
        self._build_top_bar()
        self._build_tabs()

    def _build_top_bar(self):
        self.top = tk.Frame(self.root, bg=self.theme["top_bar"], pady=10)
        self.top.pack(fill="x")

        tk.Label(self.top, text="Todo Manager",
                 font=("Arial", 17, "bold"),
                 bg=self.theme["top_bar"],
                 fg=self.theme["top_fg"]).pack(side="left", padx=20)

        # Right side buttons
        btn_cfg = dict(bg=self.theme["top_bar"], fg=self.theme["top_fg"],
                       font=("Arial", 10), relief="flat", cursor="hand2")

        self.dark_btn = tk.Button(self.top, text="Dark Mode",
                                   command=self.toggle_dark, **btn_cfg)
        self.dark_btn.pack(side="right", padx=10)

        tk.Button(self.top, text="Export CSV",
                  command=self.export_csv, **btn_cfg).pack(side="right", padx=10)

        tk.Button(self.top, text="+ Add Task",
                  command=self.open_add_form,
                  bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"),
                  relief="flat", padx=10,
                  cursor="hand2").pack(side="right", padx=10)

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tasks Tab
        self.tasks_frame = tk.Frame(self.notebook,
                                     bg=self.theme["bg"])
        self.notebook.add(self.tasks_frame, text="  Tasks  ")
        self._build_tasks_tab()

        # Dashboard Tab
        self.dashboard = Dashboard(self.notebook, self.theme)
        self.notebook.add(self.dashboard, text="  Dashboard  ")

    def _build_tasks_tab(self):
        bg = self.theme["bg"]
        fg = self.theme["label_fg"]

        # Search bar
        search_frame = tk.Frame(self.tasks_frame, bg=bg, pady=6)
        search_frame.pack(fill="x", padx=20)
        tk.Label(search_frame, text="Search:",
                 font=("Arial", 10), bg=bg, fg=fg).pack(side="left")
        self.search_entry = tk.Entry(search_frame,
                                      textvariable=self.search_var,
                                      font=("Arial", 11), width=30,
                                      bg=self.theme["entry_bg"],
                                      fg=self.theme["entry_fg"],
                                      insertbackground=self.theme["entry_fg"])
        self.search_entry.pack(side="left", padx=8)
        tk.Button(search_frame, text="✕",
                  command=lambda: self.search_var.set(""),
                  bg=bg, fg=fg, relief="flat",
                  font=("Arial", 10)).pack(side="left")

        # Filter bar
        filter_frame = tk.Frame(self.tasks_frame, bg=bg, pady=4)
        filter_frame.pack(fill="x", padx=20)
        tk.Label(filter_frame, text="Filter:",
                 font=("Arial", 10), bg=bg, fg=fg).pack(side="left")
        for label in ["All", "Pending", "Done", "High", "Medium", "Low", "Overdue"]:
            tk.Radiobutton(filter_frame, text=label,
                           variable=self.filter_var, value=label,
                           command=self.load_tasks,
                           bg=bg, fg=fg,
                           selectcolor=self.theme["entry_bg"],
                           font=("Arial", 10)).pack(side="left", padx=4)

        # Treeview
        tree_frame = tk.Frame(self.tasks_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=self.theme["tree_bg"],
                         foreground=self.theme["tree_fg"],
                         fieldbackground=self.theme["tree_bg"],
                         rowheight=26)
        style.configure("Treeview.Heading",
                         background=self.theme["top_bar"],
                         foreground="white",
                         font=("Arial", 10, "bold"))
        style.map("Treeview",
                  background=[("selected", self.theme["tree_select"])])

        columns = ("title", "category", "priority", "due_date", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                  show="headings", height=18)

        for col, text, width in [
            ("title",    "Task",     320),
            ("category", "Category", 110),
            ("priority", "Priority",  90),
            ("due_date", "Due Date", 110),
            ("status",   "Status",    90),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width,
                              anchor="center" if col != "title" else "w")

        self.tree.tag_configure("overdue", foreground=self.theme["overdue_fg"])
        self.tree.tag_configure("today",   foreground=self.theme["today_fg"])
        self.tree.tag_configure("done",    foreground=self.theme["done_fg"])
        self.tree.tag_configure("High",    foreground=self.theme["high_fg"])
        self.tree.tag_configure("Medium",  foreground=self.theme["medium_fg"])
        self.tree.tag_configure("Low",     foreground=self.theme["low_fg"])

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.open_edit_form)

        # Bottom buttons
        btn_frame = tk.Frame(self.tasks_frame, bg=bg, pady=8)
        btn_frame.pack()
        tk.Button(btn_frame, text="Mark Done",
                  command=self.mark_done,
                  bg="#2196F3", fg="white",
                  font=("Arial", 10, "bold"), width=14).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Delete Task",
                  command=self.delete_task,
                  bg="#f44336", fg="white",
                  font=("Arial", 10, "bold"), width=14).pack(side="left", padx=8)

    # ── TASK OPERATIONS ───────────────────────────────────────────────

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = database.get_all_tasks()
        f = self.filter_var.get()
        keyword = self.search_var.get().strip().lower()
        today = date.today().isoformat()

        for task in tasks:
            task_id, title, category, priority, due_date, done = task

            # Search filter
            if keyword and keyword not in title.lower() \
                       and keyword not in category.lower():
                continue

            # Status/priority filter
            if f == "Pending" and done:
                continue
            if f == "Done" and not done:
                continue
            if f in ("High", "Medium", "Low") and priority != f:
                continue
            if f == "Overdue":
                if done or not due_date or due_date >= today:
                    continue

            status = "Done" if done else "Pending"

            # Determine row tag
            if done:
                tag = "done"
            elif due_date and due_date < today:
                tag = "overdue"
                status = "Overdue!"
            elif due_date and due_date == today:
                tag = "today"
                status = "Due Today"
            else:
                tag = priority

            self.tree.insert("", "end", iid=str(task_id),
                             values=(title, category, priority,
                                     due_date or "-", status),
                             tags=(tag,))

    def open_add_form(self):
        def on_save(**kwargs):
            database.add_task(**kwargs)
            self.load_tasks()
        TaskForm(self.root, on_save=on_save, theme=self.theme)

    def open_edit_form(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        values = self.tree.item(selected[0])["values"]
        task = {
            "id":       task_id,
            "title":    values[0],
            "category": values[1],
            "priority": values[2],
            "due_date": values[3],
        }

        def on_save(**kwargs):
            database.update_task(task_id, **kwargs)
            self.load_tasks()

        TaskForm(self.root, on_save=on_save, task=task, theme=self.theme)

    def _get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        return int(selected[0])

    def mark_done(self):
        task_id = self._get_selected_id()
        if task_id:
            database.mark_done(task_id)
            self.load_tasks()

    def delete_task(self):
        task_id = self._get_selected_id()
        if task_id:
            if messagebox.askyesno("Delete", "Delete this task?"):
                database.delete_task(task_id)
                self.load_tasks()

    # ── EXPORT ────────────────────────────────────────────────────────

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save tasks as CSV"
        )
        if not path:
            return
        tasks = database.get_all_tasks()
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Category", "Priority", "Due Date", "Done"])
            for task in tasks:
                task_id, title, category, priority, due_date, done = task
                writer.writerow([task_id, title, category, priority,
                                  due_date or "", "Yes" if done else "No"])
        messagebox.showinfo("Exported", f"Tasks exported to:\n{path}")

    # ── DARK MODE ─────────────────────────────────────────────────────

    def toggle_dark(self):
        self.dark_mode = not self.dark_mode
        self.theme = THEMES["dark"] if self.dark_mode else THEMES["light"]
        self.dark_btn.config(text="Light Mode" if self.dark_mode else "Dark Mode")

        # Rebuild UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self.load_tasks()