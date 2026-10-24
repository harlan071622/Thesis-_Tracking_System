import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import database
from CustomCalendar import CustomCalendar
import os


STATUS_OPTION = ["Pending", "Re-Defense", "Revise", "Hard Bound", "Re-present"]
class UpdateStudentWindow(ctk.CTkToplevel):
    def __init__(self, master, student_id):
        super().__init__(master, fg_color="#FFFFFF")

        # Icon Setup
        project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ico_path = os.path.join(project_base, "assets", "my_logo.ico")
        png_path = os.path.join(project_base, "assets", "my_logo16.png")

        if os.path.exists(ico_path):
            self.wm_iconbitmap(default=ico_path)
        elif os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            self.iconphoto(True, img)
            self._icon_ref = img

        self.title("View Student")
        self.geometry("900x600")
        self.student_id = student_id
        self.entries = {}
        self.is_edit_mode = False

        self.build_form()

    def build_form(self):
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        calendar_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
        calendar_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.enrollment_label = ctk.CTkLabel(calendar_frame, text="Enrollment Date: Loading...", font=ctk.CTkFont("Arial", size=24, weight="bold"))
        self.enrollment_label.pack(pady=(0, 10))

        self.calendar = CustomCalendar(calendar_frame, on_date_selected=None)
        self.calendar.pack()
        self.calendar.disable()

        fields_and_options = [
            ("Name", None),
            ("Email", None),
            ("Course", database.COURSE_OPTIONS),
            ("Subject", database.SUBJECT_OPTIONS),
            ("Professor", database.PROFESSOR_OPTIONS),
            ("Advisor", database.ADVISOR_OPTIONS),
            ("Panel", database.PANEL_OPTIONS),
            ("Chairman", database.CHAIRMAN_OPTIONS),
            ("Thesis Status", database.THESIS_ACTIVE_STATUS_OPTIONS),
            ("Status", STATUS_OPTION),
        ]

        for row_idx, (field, options) in enumerate(fields_and_options):
            ctk.CTkLabel(form_frame, text=field).grid(row=row_idx, column=0, sticky="w", padx=10, pady=4)
            if options and len(options) > 1:
                dropdown = ctk.CTkOptionMenu(form_frame, values=options)
                dropdown.grid(row=row_idx, column=1, sticky="ew", padx=10, pady=4)
                dropdown.configure(state="disabled")
                if field == "Course":
                    self.course_dropdown = dropdown
                    dropdown.configure(command=self.update_subject_options)
                elif field == "Subject":
                    self.subject_dropdown = dropdown
                self.entries[field] = dropdown
            else:
                entry = ctk.CTkEntry(form_frame)
                entry.grid(row=row_idx, column=1, sticky="ew", padx=10, pady=4)
                entry.configure(state="disabled")
                self.entries[field] = entry

        self.edit_btn = ctk.CTkButton(form_frame, text="Edit", command=self.toggle_edit_mode)
        self.edit_btn.grid(row=len(fields_and_options), column=0, pady=20)

        self.save_btn = ctk.CTkButton(form_frame, text="Save Changes", command=self.save_changes, state="disabled")
        self.save_btn.grid(row=len(fields_and_options), column=1, pady=20)

        self.load_student_data()

    def toggle_edit_mode(self):
        self.is_edit_mode = not self.is_edit_mode

        for field, widget in self.entries.items():
            if isinstance(widget, ctk.CTkEntry) or isinstance(widget, ctk.CTkOptionMenu):
                widget.configure(state="normal" if self.is_edit_mode else "disabled")

        self.calendar.enable() if self.is_edit_mode else self.calendar.disable()

        self.save_btn.configure(state="normal" if self.is_edit_mode else "disabled")
        self.edit_btn.configure(text="Cancel Edit" if self.is_edit_mode else "Edit")
        self.title("Edit Student" if self.is_edit_mode else "View Student")

    def update_subject_options(self, selected_course):
        from database import get_subjects_by_course
        subjects = get_subjects_by_course(selected_course)
        if not subjects:
            subjects = ["Select an option"]
        self.subject_dropdown.configure(values=subjects)
        self.subject_dropdown.set(subjects[0])

    def load_student_data(self):
        conn = database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT name, email, course, subject, professor, advisor,
                       panel, chairman, active_status, enrollment_date
                FROM students WHERE id = %s
            """, (self.student_id,))
            student_data = cursor.fetchone()

            cursor.execute("SELECT status FROM progress WHERE student_id = %s", (self.student_id,))
            status_data = cursor.fetchone()

            if not student_data:
                messagebox.showerror("Error", "Student not found.")
                self.destroy()
                return

            fields = ["Name", "Email", "Course", "Subject", "Professor", "Advisor",
                      "Panel", "Chairman", "Thesis Status"]

            for i, field in enumerate(fields):
                widget = self.entries[field]
                value = student_data[i]
                if isinstance(widget, ctk.CTkOptionMenu):
                    widget.set(value)
                else:
                    widget.configure(state="normal")
                    widget.delete(0, "end")
                    widget.insert(0, value)
                    widget.configure(state="disable")

            if status_data:
                self.update_subject_options(student_data[2])
                self.entries["Status"].set(status_data[0])

            if student_data and len(student_data) >= 10:
                enroll_date = student_data[9]
                if enroll_date:
                    self.enrollment_label.configure(text=f"Enrollment Date: {enroll_date}")
                    self.calendar.set_date(str(enroll_date))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student data: {e}")
        finally:
            cursor.close()
            conn.close()

    def save_changes(self):
        # Same as your existing code, no changes needed
        ...
