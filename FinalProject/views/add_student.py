from datetime import datetime

import flet as ft

import database
from database import create_student, get_subjects_by_course
from views.ui import show_alert


def build(app):
    page = app.page
    state = {"enroll_date": None}

    name_field = ft.TextField(label="Name", expand=True)
    email_field = ft.TextField(label="Email", expand=True)

    course_dropdown = ft.Dropdown(
        label="Course", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.COURSE_OPTIONS],
        value=database.COURSE_OPTIONS[0] if database.COURSE_OPTIONS else None,
    )
    subject_dropdown = ft.Dropdown(
        label="Subject", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.SUBJECT_OPTIONS],
        value=database.SUBJECT_OPTIONS[0] if database.SUBJECT_OPTIONS else None,
    )
    professor_dropdown = ft.Dropdown(
        label="Professor", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.PROFESSOR_OPTIONS],
        value=database.PROFESSOR_OPTIONS[0] if database.PROFESSOR_OPTIONS else None,
    )
    advisor_dropdown = ft.Dropdown(
        label="Advisor", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.ADVISOR_OPTIONS],
        value=database.ADVISOR_OPTIONS[0] if database.ADVISOR_OPTIONS else None,
    )
    panel_dropdown = ft.Dropdown(
        label="Panel", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.PANEL_OPTIONS],
        value=database.PANEL_OPTIONS[0] if database.PANEL_OPTIONS else None,
    )
    chairman_dropdown = ft.Dropdown(
        label="Chairman", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.CHAIRMAN_OPTIONS],
        value=database.CHAIRMAN_OPTIONS[0] if database.CHAIRMAN_OPTIONS else None,
    )
    thesis_status_dropdown = ft.Dropdown(
        label="Thesis Status", expand=True,
        options=[ft.DropdownOption(key=c, text=c) for c in database.THESIS_ACTIVE_STATUS_OPTIONS],
        value=database.THESIS_ACTIVE_STATUS_OPTIONS[0] if database.THESIS_ACTIVE_STATUS_OPTIONS else None,
    )

    date_label = ft.Text("Enrollment Date: Not selected", weight=ft.FontWeight.BOLD)

    def on_course_change(e):
        subjects = get_subjects_by_course(course_dropdown.value) or ["Select an option"]
        subject_dropdown.options = [ft.DropdownOption(key=s, text=s) for s in subjects]
        subject_dropdown.value = subjects[0]
        page.update()

    course_dropdown.on_change = on_course_change

    def on_date_change(e):
        if date_picker.value:
            state["enroll_date"] = date_picker.value.strftime("%Y-%m-%d")
            date_label.value = f"Enrollment Date: {state['enroll_date']}"
            page.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2015, 1, 1),
        last_date=datetime(2035, 12, 31),
        on_change=on_date_change,
    )
    page.overlay.append(date_picker)

    def open_date_picker(e):
        date_picker.open = True
        page.update()

    error_text = ft.Text("", color="#be1e2d")

    def save_student(e):
        name = (name_field.value or "").strip()
        email = (email_field.value or "").strip()
        course = course_dropdown.value
        subject = subject_dropdown.value
        professor = professor_dropdown.value
        advisor = advisor_dropdown.value
        panel = panel_dropdown.value
        chairman = chairman_dropdown.value
        thesis_status = thesis_status_dropdown.value

        invalid_selection = any(
            x in (None, "Select an option") for x in [course, subject, professor, advisor, panel, chairman, thesis_status]
        )
        if not name or not email or invalid_selection:
            error_text.value = "Please fill in all fields and make valid selections."
            page.update()
            return
        if not state["enroll_date"]:
            error_text.value = "Please select an enrollment date."
            page.update()
            return

        try:
            create_student(name, email, course, subject, professor, advisor, panel, chairman, thesis_status, state["enroll_date"])
            error_text.value = ""
            page.update()
            show_alert(page, "Saved", "Student data saved successfully.")
            app.show_add_student()
        except Exception as ex:
            error_text.value = f"An error occurred while saving: {ex}"
            page.update()

    form = ft.Column(
        [
            name_field,
            email_field,
            course_dropdown,
            subject_dropdown,
            professor_dropdown,
            advisor_dropdown,
            panel_dropdown,
            chairman_dropdown,
            thesis_status_dropdown,
            error_text,
            ft.Button("Save Student", bgcolor="#be1e2d", color="white", on_click=save_student),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    calendar_area = ft.Column(
        [
            ft.Text("Enrollment Date", size=18, weight=ft.FontWeight.BOLD),
            date_label,
            ft.Button("Pick Date", bgcolor="#181888", color="white", on_click=open_date_picker),
        ],
        spacing=10,
        col={"xs": 12, "md": 5},
    )

    form.col = {"xs": 12, "md": 7}

    return ft.Column(
        [
            ft.Text("Add Student", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.ResponsiveRow([form, calendar_area], spacing=40, run_spacing=20),
        ],
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )
