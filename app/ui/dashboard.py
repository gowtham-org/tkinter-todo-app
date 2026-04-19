import tkinter as tk
from tkinter import ttk
import database

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class Dashboard(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme.get("bg", "#f5f5f5"))
        self.theme = theme
        self._build_ui()

    def _build_ui(self):
        bg = self.theme.get("bg", "#f5f5f5")
        fg = self.theme.get("label_fg", "#333")

        tk.Label(self, text="Task Dashboard", font=("Arial", 16, "bold"),
                 bg=bg, fg=fg).pack(pady=10)

        tk.Button(self, text="Refresh", command=self.render_charts,
                  bg="#2196F3", fg="white", font=("Arial", 10)).pack(pady=4)

        self.chart_frame = tk.Frame(self, bg=bg)
        self.chart_frame.pack(fill="both", expand=True)

        self.render_charts()

    def render_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not MATPLOTLIB_AVAILABLE:
            tk.Label(self.chart_frame,
                     text="matplotlib not installed.\nRun: pip install matplotlib",
                     font=("Arial", 12), bg=self.theme.get("bg")).pack(pady=40)
            return

        stats = database.get_stats()
        bg = self.theme.get("bg", "#f5f5f5")
        is_dark = bg == "#1e1e1e"
        plot_bg = "#2d2d2d" if is_dark else "#ffffff"
        text_color = "#e0e0e0" if is_dark else "#333333"

        fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
        fig.patch.set_facecolor(plot_bg)

        # Bar chart — all stats
        ax1 = axes[0]
        ax1.set_facecolor(plot_bg)
        labels = list(stats.keys())
        values = list(stats.values())
        bar_colors = ["#5c85d6", "#4CAF50", "#ffa500", "#f44336", "#9c27b0"]
        bars = ax1.bar(labels, values, color=bar_colors, edgecolor="none")
        ax1.set_title("Task Overview", color=text_color, fontsize=11)
        ax1.tick_params(colors=text_color, labelsize=8)
        ax1.xaxis.label.set_color(text_color)
        for spine in ax1.spines.values():
            spine.set_edgecolor(plot_bg)
        for bar, val in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     str(val), ha="center", va="bottom",
                     color=text_color, fontsize=9)

        # Pie chart — done vs pending
        ax2 = axes[1]
        ax2.set_facecolor(plot_bg)
        done = stats["Done"]
        pending = stats["Pending"]
        if done + pending > 0:
            ax2.pie(
                [done, pending],
                labels=["Done", "Pending"],
                colors=["#4CAF50", "#ffa500"],
                autopct="%1.0f%%",
                textprops={"color": text_color},
                startangle=90
            )
        else:
            ax2.text(0.5, 0.5, "No tasks yet", ha="center",
                     va="center", transform=ax2.transAxes, color=text_color)
        ax2.set_title("Done vs Pending", color=text_color, fontsize=11)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)
        plt.close(fig)