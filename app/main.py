import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
import database
from ui.main_window import MainWindow

if __name__ == "__main__":
    database.init_db()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()