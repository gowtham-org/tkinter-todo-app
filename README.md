# Todo Manager — Tkinter Desktop App

A feature-rich desktop Todo application built with Python and Tkinter, backed by SQLite for persistent storage.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- **Add / Edit / Delete tasks** — double-click any row to edit
- **Priority levels** — High, Medium, Low with color coding
- **Categories** — General, Work, Personal, Shopping, Health
- **Due dates** — with overdue and due-today highlights
- **Search** — live keyword filter across tasks
- **Filter bar** — All, Pending, Done, High, Medium, Low, Overdue
- **Dashboard** — bar chart and pie chart showing task stats
- **Export CSV** — save all tasks to a `.csv` file
- **Dark mode** — toggle between light and dark theme
- **Persistent storage** — tasks saved in local SQLite database

---

## Project Structure
tkinter-todo-app/
├── app/
│   ├── main.py              # Entry point
│   ├── database.py          # SQLite operations
│   ├── theme.py             # Light and dark theme config
│   └── ui/
│       ├── main_window.py   # Main app layout and logic
│       ├── task_form.py     # Add / Edit task popup
│       └── dashboard.py     # Dashboard charts tab
├── requirements.txt
├── .gitignore
└── README.md

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tkinter-todo-app.git
cd tkinter-todo-app
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app/main.py
```

---

## Requirements

- Python 3.10+
- `matplotlib` — for dashboard charts
- `tkinter` — included in Python standard library
- `sqlite3` — included in Python standard library

---

## Usage

| Action | How |
|---|---|
| Add a task | Click **+ Add Task** button |
| Edit a task | **Double-click** any row |
| Mark as done | Select row → click **Mark Done** |
| Delete a task | Select row → click **Delete Task** |
| Search | Type in the search bar (filters live) |
| Filter | Use the filter radio buttons |
| Export | Click **Export CSV** → choose save location |
| Dark mode | Click **Dark Mode** toggle in top bar |
| Dashboard | Click the **Dashboard** tab |

---

## Status Colors

| Color | Meaning |
|---|---|
| Red | High priority or Overdue |
| Orange | Medium priority or Due Today |
| Green | Low priority |
| Gray | Completed task |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| GUI | Tkinter |
| Database | SQLite |
| Charts | Matplotlib |
| Version Control | Git + GitHub |

---

## License

MIT License — free to use and modify.