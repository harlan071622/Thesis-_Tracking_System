import customtkinter as ctk
from tkinter import messagebox
import database
from database import get_connection
from CustomCalendar import CustomCalendar

class AddStudentWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#FFFFFF")
        self.entries = {}
        self.selected_enroll_date = None

        ctk.CTkLabel(self, text="Add Student", font=ctk.CTkFont(size=20)).pack(pady=10)

        layout_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF"
        )
        layout_frame.pack(fill="both", expand=True)
        

        form_frame = ctk.CTkFrame(layout_frame, fg_color="#FFFFFF")
        form_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=10)

        calendar_frame = ctk.CTkFrame(layout_frame, fg_color="#FFFFFF")
        calendar_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=10)

        enroll_label = ctk.CTkLabel(calendar_frame, text="Enrollment Date", font=ctk.CTkFont("Arial", size=24, weight="bold"))
        enroll_label.grid(row=0, column=0, sticky="w")

        self.calendar = CustomCalendar(calendar_frame, on_date_selected=self.on_date_picked)
        self.calendar.grid(row=1, column=0, pady=(5, 0))

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
        ]

        for row_idx, (field, options) in enumerate(fields_and_options):
            ctk.CTkLabel(form_frame, text=field).grid(row=row_idx, column=0, sticky="w", padx=10, pady=4)

            if options and isinstance(options, list) and len(options) > 1:
                if field == "Course":
                    dropdown = ctk.CTkOptionMenu(form_frame, values=options, command=self.update_subject_options)
                    self.course_dropdown = dropdown
                elif field == "Subject":
                    dropdown = ctk.CTkOptionMenu(form_frame, values=["Select an option"])
                    self.subject_dropdown = dropdown
                else:
                    dropdown = ctk.CTkOptionMenu(form_frame, values=options)

                dropdown.set(options[0] if field != "Subject" else "Select an option")
                dropdown.grid(row=row_idx, column=1, sticky="ew", padx=10, pady=4)
                self.entries[field] = dropdown
            else:
                entry = ctk.CTkEntry(form_frame)
                entry.grid(row=row_idx, column=1, sticky="ew", padx=10, pady=4)
                self.entries[field] = entry

        ctk.CTkButton(self, text="Save Student", command=self.save_student).pack(pady=20)

    def on_date_picked(self, date_str):
        print("Enrollment Date Selected:", date_str)
        self.selected_enroll_date = date_str

    def update_subject_options(self, selected_course):
        from database import get_subjects_by_course
        subjects = get_subjects_by_course(selected_course)
        if not subjects:
            subjects = ["Select an option"]
        self.subject_dropdown.configure(values=subjects)
        self.subject_dropdown.set(subjects[0])

    def save_student(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            name = self.entries["Name"].get().strip()
            email = self.entries["Email"].get().strip()
            course = self.entries["Course"].get()
            subject = self.entries["Subject"].get()
            professor = self.entries["Professor"].get()
            advisor = self.entries["Advisor"].get()
            panel = self.entries["Panel"].get()
            chairman = self.entries["Chairman"].get()
            thesis_status = self.entries["Thesis Status"].get()

            if not all([name, email]) or any(
                x in ["Select an option"] for x in [course, subject, professor, advisor, panel, chairman, thesis_status]
            ):
                messagebox.showerror("Missing Data", "Please fill in all fields and make valid selections.")
                return

            enroll_date = self.selected_enroll_date
            if not enroll_date:
                messagebox.showerror("Missing Date", "Please select an enrollment date.")
                return

            cursor.execute("""
                INSERT INTO students (name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, email, course, subject, professor, advisor, panel, chairman, thesis_status, enroll_date))

            student_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO progress (student_id, student_name, status)
                VALUES (%s, %s, %s)
            """, (student_id, name, 'Pending'))

            conn.commit()
            messagebox.showinfo("Saved", "Student data saved successfully.")

            for widget in self.entries.values():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                elif isinstance(widget, ctk.CTkOptionMenu):
                    widget.set("Select an option")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
        finally:
            cursor.close()
            conn.close()
