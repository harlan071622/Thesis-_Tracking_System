import urllib.parse

import flet as ft

from database import archive_student, get_all_students_with_status
from views.ui import show_alert, show_confirm

TABS = ["Software Engineering", "Capstones", "MIT & MIS"]
COLUMNS = [
    "ID", "Name", "Email", "Course", "Subject", "Professor",
    "Advisor", "Panel", "Chairman", "Status", "Active Status", "Status Changes",
]


def _filter_rows(students, tab_name):
    rows = []
    for row in students:
        course = (row[3] or "").strip().lower()
        subject = (row[4] or "").strip().lower()
        if tab_name == "Software Engineering" and "software engineering" in subject:
            rows.append(row)
        elif tab_name == "MIT & MIS" and course in ["mit", "mis"]:
            rows.append(row)
        elif tab_name == "Capstones" and course in ["bsit", "bscs", "bscpe"] and "software engineering" not in subject:
            rows.append(row)
    return rows


def build(app):
    page = app.page
    state = {"active_tab": TABS[0], "selected": {t: None for t in TABS}}
    tab_buttons = {}
    table_container = ft.Container(expand=True)

    def open_gmail_compose(to_email, subject, body):
        params = {"to": to_email, "su": subject, "body": body}
        url = "https://mail.google.com/mail/?view=cm&fs=1&" + urllib.parse.urlencode(params)
        page.launch_url(url)

    def render():
        tab_name = state["active_tab"]
        try:
            students = get_all_students_with_status()
        except Exception as ex:
            table_container.content = ft.Text(f"Failed to load student data: {ex}", color="#be1e2d")
            return

        rows_data = _filter_rows(students, tab_name)
        selected_id = state["selected"].get(tab_name)

        def select_row(sid):
            state["selected"][tab_name] = sid
            render()
            page.update()

        data_rows = []
        for row in rows_data:
            data_rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(v) if v is not None else "")) for v in row],
                    selected=(row[0] == selected_id),
                    on_select_change=lambda e, sid=row[0]: select_row(sid),
                )
            )

        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(c, weight=ft.FontWeight.BOLD)) for c in COLUMNS],
            rows=data_rows,
            show_checkbox_column=True,
            column_spacing=20,
            heading_row_color="#f4f4f4",
        )

        def on_update(e):
            sid = state["selected"].get(tab_name)
            if not sid:
                show_alert(page, "No Selection", "Please select a student to update.")
                return
            app.show_update_student(sid)

        def on_archive(e):
            sid = state["selected"].get(tab_name)
            if not sid:
                show_alert(page, "No Selection", "Please select a student to archive.")
                return

            def do_archive():
                try:
                    archive_student(sid)
                    state["selected"][tab_name] = None
                    render()
                    page.update()
                    show_alert(page, "Archived", "Student archived successfully.")
                except Exception as ex:
                    show_alert(page, "Error", f"Failed to archive: {ex}")

            show_confirm(page, "Confirm Archive", f"Archive student ID {sid}?", do_archive)

        def on_reminder(e):
            sid = state["selected"].get(tab_name)
            if not sid:
                show_alert(page, "No Selection", "Please select a student.")
                return
            row = next((r for r in rows_data if r[0] == sid), None)
            if not row:
                return
            name, email = row[1], row[2]
            subject = "Reminder: Thesis Progress"
            body = (
                f"Hello {name},\n\nThis is a reminder to check and update your thesis progress."
                f"\n\nBest regards,\nThesis Coordinator"
            )
            open_gmail_compose(email, subject, body)

        btn_row = ft.Row(
            [
                ft.Button("Update Selected", bgcolor="#181888", color="white", on_click=on_update),
                ft.Button("Archive Selected", bgcolor="#181888", color="white", on_click=on_archive),
                ft.Button("Send Reminder", bgcolor="#181888", color="white", on_click=on_reminder),
            ],
            spacing=10,
        )

        table_scroll_area = ft.Column(
            [ft.Row([table], scroll=ft.ScrollMode.AUTO)],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        table_container.content = ft.Column(
            [
                table_scroll_area,
                btn_row,
            ],
            expand=True,
        )

    def switch_tab(tab_name):
        state["active_tab"] = tab_name
        for name, btn in tab_buttons.items():
            active = name == tab_name
            btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        render()
        page.update()

    for tab_name in TABS:
        btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text(tab_name, weight=ft.FontWeight.BOLD, color="#000000"),
                bgcolor="#FFFFFF",
                border_radius=5,
                padding=10,
            ),
            on_click=lambda e, t=tab_name: switch_tab(t),
        )
        tab_buttons[tab_name] = btn

    for name, btn in tab_buttons.items():
        active = name == TABS[0]
        btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
        btn.content.content.color = "#FFFFFF" if active else "#000000"
    render()

    return ft.Column(
        [
            ft.Text("Student List", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row(list(tab_buttons.values()), spacing=5),
            table_container,
        ],
        expand=True,
        spacing=10,
    )
