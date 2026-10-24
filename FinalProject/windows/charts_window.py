import customtkinter as ctk
from tkinter import messagebox
from database import get_all_students_with_status, get_archived_students
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

class ChartsWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#FFFFFF")

        main_tabview = ctk.CTkTabview(self, fg_color="#FFFFFF")
        main_tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create two primary tabs
        active_tab = main_tabview.add("Active Students")
        archived_tab = main_tabview.add("Archived Students")

        # === ACTIVE STUDENTS TAB CHARTS ===
        active_tabview = ctk.CTkTabview(active_tab, fg_color="#FFFFFF")
        active_tabview.pack(fill="both", expand=True)

        active_specs = [
            ("Status Distribution", self._draw_status_distribution),
            ("Course Breakdown", self._draw_course_breakdown),
            ("Subject Breakdown", self._draw_subject_breakdown),
            ("Professor Breakdown", self._draw_professor_breakdown),
            ("Advisor Breakdown", self._draw_advisor_breakdown),
            ("Panel Breakdown", self._draw_panel_breakdown),
            ("Chairman Breakdown", self._draw_chairman_breakdown),
            ("Active vs Inactive", self._draw_active_inactive),
        ]
        for title, drawer in active_specs:
            active_tabview.add(title)
            frame = active_tabview.tab(title)
            try:
                drawer(frame)
            except Exception as e:
                messagebox.showerror("Chart Error", f"Failed to load {title}: {e}")

        # === ARCHIVED STUDENTS TAB CHARTS ===
        archived_tabview = ctk.CTkTabview(archived_tab)
        archived_tabview.pack(fill="both", expand=True)

        archived_tabview.add("Archived vs Not Archived")
        frame = archived_tabview.tab("Archived vs Not Archived")
        try:
            self._draw_archived_not_archived(frame)
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to load Archived Chart: {e}")

    def _create_donut(self, frame, labels, sizes, title):
        fig = Figure(figsize=(7.5, 7.5), dpi=100)
        ax = fig.add_subplot(111)
        wedges, _, autotexts = ax.pie(
            sizes,
            labels=None,
            autopct=lambda pct: str(int(pct * sum(sizes) / 100)),
            startangle=90,
            pctdistance=0.75,
            wedgeprops=dict(width=0.4, edgecolor='w')
        )
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(12)
        centre = Circle((0, 0), 0.60, fc='white', edgecolor='w')
        legend_labels = [f"{label} ({size})" for label, size in zip(labels, sizes)]
        ax.add_artist(centre)
        ax.set_title(title, pad=20)
        ax.axis('equal')
        ax.legend(
            wedges, legend_labels,
            title="Legend",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            ncol=1
        )
        fig.tight_layout(pad=3.5)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _draw_status_distribution(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            status = rec[9] or 'Unknown'
            counts[status] = counts.get(status, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Thesis Status Distribution")

    def _draw_course_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            course = rec[3] or 'Unknown'
            counts[course] = counts.get(course, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Course Breakdown")

    def _draw_subject_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            subj = rec[4] or 'Unknown'
            counts[subj] = counts.get(subj, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Subject Breakdown")

    def _draw_professor_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            prof = (rec[5] or 'Unknown').strip()
            counts[prof] = counts.get(prof, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Professor Breakdown")

    def _draw_advisor_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            adv = (rec[6] or 'Unknown').strip()
            counts[adv] = counts.get(adv, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Advisor Breakdown")

    def _draw_panel_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            panel = (rec[7] or 'Unknown').strip()
            counts[panel] = counts.get(panel, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Panel Breakdown")

    def _draw_chairman_breakdown(self, frame):
        data = get_all_students_with_status()
        counts = {}
        for rec in data:
            chair = (rec[8] or 'Unknown').strip()
            counts[chair] = counts.get(chair, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if not sizes:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Chairman Breakdown")

    def _draw_active_inactive(self, frame):
        data = get_all_students_with_status()
        counts = {"Active": 0, "Inactive": 0}

        for rec in data:
            status = rec[10] or "Active"  # rec[10] = active_status
            counts[status] = counts.get(status, 0) + 1

        labels = list(counts.keys())
        sizes = list(counts.values())
        if not sizes or sum(sizes) == 0:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return

        self._create_donut(frame, labels, sizes, "Active vs Inactive")

    def _draw_archived_not_archived(self, frame):
        archived = len(get_archived_students())
        active = len(get_all_students_with_status())
        labels = ["Archived", "Not Archived"]
        sizes = [archived, active]
        if archived + active == 0:
            ctk.CTkLabel(frame, text="No data available").pack(expand=True)
            return
        self._create_donut(frame, labels, sizes, "Archived vs Not Archived")
