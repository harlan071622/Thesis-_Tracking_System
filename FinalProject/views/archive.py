import flet as ft

from database import get_archived_students, unarchive_student
from views.ui import show_alert, show_confirm

COLUMNS = [
    "ID", "Name", "Email", "Course", "Subject", "Professor",
    "Advisor", "Panel", "Chairman", "Status", "Enrollment Date", "Date Added", "Archived At",
]


def build(app):
    page = app.page
    state = {"selected": None}
    table_container = ft.Container(expand=True)

    def render():
        try:
            archived = get_archived_students()
        except Exception as ex:
            table_container.content = ft.Text(f"Failed to load archive: {ex}", color="#be1e2d")
            return

        def select_row(sid):
            state["selected"] = sid
            render()
            page.update()

        data_rows = [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(v) if v is not None else "")) for v in row],
                selected=(row[0] == state["selected"]),
                on_select_change=lambda e, sid=row[0]: select_row(sid),
            )
            for row in archived
        ]

        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(c, weight=ft.FontWeight.BOLD)) for c in COLUMNS],
            rows=data_rows,
            show_checkbox_column=True,
            column_spacing=20,
            heading_row_color="#f4f4f4",
        )

        def on_unarchive(e):
            sid = state["selected"]
            if not sid:
                show_alert(page, "No Selection", "Please select an archived student to unarchive.")
                return

            def do_unarchive():
                try:
                    unarchive_student(sid)
                    state["selected"] = None
                    render()
                    page.update()
                    show_alert(page, "Restored", "Student has been unarchived.")
                except Exception as ex:
                    show_alert(page, "Error", f"Failed to unarchive: {ex}")

            show_confirm(page, "Confirm Unarchive", f"Restore student ID {sid} to active list?", do_unarchive)

        def on_refresh(e):
            state["selected"] = None
            render()
            page.update()

        btn_row = ft.Row(
            [
                ft.Button("Unarchive Selected", bgcolor="#181888", color="white", on_click=on_unarchive),
                ft.Button("Refresh", bgcolor="#181888", color="white", on_click=on_refresh),
            ],
            spacing=10,
        )

        scroll_content = [ft.Row([table], scroll=ft.ScrollMode.AUTO)]
        if not archived:
            scroll_content.insert(0, ft.Text("No archive data yet.", italic=True))

        table_scroll_area = ft.Column(scroll_content, expand=True, scroll=ft.ScrollMode.AUTO)

        table_container.content = ft.Column(
            [table_scroll_area, btn_row],
            expand=True,
        )

    render()

    return ft.Column(
        [
            ft.Text("Archived Students", size=20, weight=ft.FontWeight.BOLD, color="black"),
            table_container,
        ],
        expand=True,
        spacing=10,
    )
