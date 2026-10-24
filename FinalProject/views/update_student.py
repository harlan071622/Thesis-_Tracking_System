from datetime import datetime

import flet as ft

import database
from database import get_student_by_id, get_subjects_by_course, update_student
from views.ui import show_alert

STATUS_OPTIONS = ["Pending", "Re-Defense", "Revise", "Hard Bound", "Re-present"]


def build(app, student_id):
    page = app.page
    state = {"edit": False, "enroll_date": None}

    student, status = get_student_by_id(student_id)
    if not student:
        show_alert(page, "Error", "Student not found.")
        app.show_student_list()
        return ft.Container()

    (s_name, s_email, s_course, s_subject, s_professor, s_advisor, s_panel, s_chairman, s_active_status, s_enroll_date) = student
    state["enroll_date"] = str(s_enroll_date) if s_enroll_date else None

    name_field = ft.TextField(label="Name", value=s_name, expand=True, disabled=True)
    email_field = ft.TextField(label="Email", value=s_email, expand=True, disabled=True)

    def opts(options, current):
        values = list(options) if options else []
        if current and current not in values:
            values = [current] + values
        return values

    course_dropdown = ft.Dropdown(
        label="Course", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.COURSE_OPTIONS, s_course)],
        value=s_course,
    )
    subject_dropdown = ft.Dropdown(
        label="Subject", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.SUBJECT_OPTIONS, s_subject)],
        value=s_subject,
    )
    professor_dropdown = ft.Dropdown(
        label="Professor", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.PROFESSOR_OPTIONS, s_professor)],
        value=s_professor,
    )
    advisor_dropdown = ft.Dropdown(
        label="Advisor", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.ADVISOR_OPTIONS, s_advisor)],
        value=s_advisor,
    )
    panel_dropdown = ft.Dropdown(
        label="Panel", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.PANEL_OPTIONS, s_panel)],
        value=s_panel,
    )
    chairman_dropdown = ft.Dropdown(
        label="Chairman", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.CHAIRMAN_OPTIONS, s_chairman)],
        value=s_chairman,
    )
    thesis_status_dropdown = ft.Dropdown(
        label="Thesis Status", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(database.THESIS_ACTIVE_STATUS_OPTIONS, s_active_status)],
        value=s_active_status,
    )
    status_dropdown = ft.Dropdown(
        label="Status", expand=True, disabled=True,
        options=[ft.DropdownOption(key=c, text=c) for c in opts(STATUS_OPTIONS, status)],
        value=status,
    )

    date_label = ft.Text(
        f"Enrollment Date: {state['enroll_date'] or 'Not set'}", weight=ft.FontWeight.BOLD
    )

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

    pick_date_btn = ft.Button("Pick Date", bgcolor="#181888", color="white", on_click=open_date_picker, disabled=True)

    error_text = ft.Text("", color="#be1e2d")

    all_fields = [
        name_field, email_field, course_dropdown, subject_dropdown, professor_dropdown,
        advisor_dropdown, panel_dropdown, chairman_dropdown, thesis_status_dropdown, status_dropdown,
    ]

    def toggle_edit(e):
        state["edit"] = not state["edit"]
        for f in all_fields:
            f.disabled = not state["edit"]
        pick_date_btn.disabled = not state["edit"]
        edit_btn.text = "Cancel Edit" if state["edit"] else "Edit"
        save_btn.disabled = not state["edit"]
        page.update()

    def save_changes(e):
        try:
            update_student(
                student_id,
                (name_field.value or "").strip(),
                (email_field.value or "").strip(),
                course_dropdown.value,
                subject_dropdown.value,
                professor_dropdown.value,
                advisor_dropdown.value,
                panel_dropdown.value,
                chairman_dropdown.value,
                thesis_status_dropdown.value,
                state["enroll_date"],
                status_dropdown.value,
            )
            show_alert(page, "Saved", "Student updated successfully.")
            app.show_update_student(student_id)
        except Exception as ex:
            error_text.value = f"Failed to save: {ex}"
            page.update()

    edit_btn = ft.Button("Edit", bgcolor="#181888", color="white", on_click=toggle_edit)
    save_btn = ft.Button("Save Changes", bgcolor="#be1e2d", color="white", on_click=save_changes, disabled=True)
    back_btn = ft.TextButton("< Back to List", on_click=lambda e: app.show_student_list())

    form = ft.Column(
        all_fields + [error_text, ft.Row([edit_btn, save_btn], spacing=10)],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        col={"xs": 12, "md": 7},
    )

    calendar_area = ft.Column(
        [ft.Text("Enrollment Date", size=18, weight=ft.FontWeight.BOLD), date_label, pick_date_btn],
        spacing=10,
        col={"xs": 12, "md": 5},
    )

    return ft.Column(
        [
            back_btn,
            ft.Text("View / Edit Student", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.ResponsiveRow([form, calendar_area], spacing=40, run_spacing=20),
        ],
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )
