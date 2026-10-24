import customtkinter as ctk
from tkinter import ttk
from database import get_all_students_with_status
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

def create_professor_stats(prof_name, parent_frame):
    students = get_all_students_with_status()
    prof_key = prof_name.replace("Prof. ", "").strip()
    prof_students = [s for s in students if s[5] and prof_key in s[5]]

    student_count = len(prof_students)
    subject_count = len({s[4].strip() for s in prof_students if s[4]})
    course_count = len({s[3].strip() for s in prof_students if s[3]})

    total = student_count + subject_count + course_count
    if total == 0:
        ctk.CTkLabel(parent_frame, text="No data available", font=ctk.CTkFont(size=16)).pack(expand=True)
        return

    labels = []
    sizes = []
    colors = ['#66BB6A', '#42A5F5', '#00FF69']
    if student_count:
        labels.append("Students")
        sizes.append(student_count)
    if subject_count:
        labels.append("Subjects")
        sizes.append(subject_count)
    if course_count:
        labels.append("Courses")
        sizes.append(course_count)

    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors[:len(sizes)],
        autopct=lambda pct: str(int(pct * sum(sizes) / 100)),
        startangle=90,
        pctdistance=0.85,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
    centre_circle = Circle((0, 0), 0.60, fc='#f0f0f0', edgecolor='w')
    legend_labels = [f"{label} ({size})" for label, size in zip(labels, sizes)]
    ax.add_artist(centre_circle)
    ax.legend(
        wedges, legend_labels, 
        title="Legend", 
        loc="best", 
        fontsize=10
    )
    ax.set_title(f"Stats for {prof_name}", fontsize=14)
    ax.axis('equal')
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def add_professor_overview_treeview(parent_frame, prof_name):
    tree = ttk.Treeview(parent_frame, columns=["ID","Name","Email","Course","Subject","Status"], show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)
    tree.pack(fill="both", expand=True, padx=5, pady=5)

    students = get_all_students_with_status()
    prof_key = prof_name.replace("Prof. ", "").strip()
    prof_students = [s for s in students if s[5] and prof_key in s[5]]
    for s in prof_students:
        tree.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4], s[9]))

class ProfessorWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF")
        self.main_tabview = ctk.CTkTabview(self, fg_color="#FFFFFF")
        self.main_tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.main_tabview.add("Professors")
        profs_frame = self.main_tabview.tab("Professors")
        profs_frame.configure(fg_color="white")

        professors_list = [
            "Prof. Ervin ",
            "Prof. Josephine",
            "Prof. Jonathan ",
            "Prof. Joanalyn ",
            "Prof. Dan",
        ]
        subtabs = ["Overview", "Statistics"]

        nested_prof_tabview = ctk.CTkTabview(profs_frame, fg_color="#FFFFFF")
        nested_prof_tabview.pack(expand=True, fill="both", padx=10, pady=10)

        for prof_name in professors_list:
            nested_prof_tabview.add(prof_name)
            prof_tab_frame = nested_prof_tabview.tab(prof_name)

            prof_subtabview = ctk.CTkTabview(prof_tab_frame, fg_color="#FFFFFF")
            prof_subtabview.pack(expand=True, fill="both", padx=5, pady=5)

            subtab_frames = {}
            for tab in subtabs:
                prof_subtabview.add(tab)
                tab_frame = prof_subtabview.tab(tab)
                tab_frame.configure(fg_color="white")
                subtab_frames[tab] = tab_frame
                if tab == "Overview":
                    add_professor_overview_treeview(tab_frame, prof_name)
                else:
                    ctk.CTkLabel(tab_frame, text="Select the Statistics tab to view chart").pack(pady=20)

            def make_callback(pname, tv, frames):
                def on_tab_change():
                    if tv.get() == "Statistics":
                        stats_frame = frames["Statistics"]
                        if not hasattr(stats_frame, 'loaded'):
                            create_professor_stats(pname, stats_frame)
                            stats_frame.loaded = True
                return on_tab_change

            nested = nested_prof_tabview
            nested_tab = prof_subtabview
            prof_subtabview.configure(command=make_callback(prof_name, prof_subtabview, subtab_frames))
