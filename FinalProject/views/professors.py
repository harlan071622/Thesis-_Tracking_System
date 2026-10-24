import flet as ft

from database import get_all_students_with_status, get_professor_names
from views.charts_util import render_donut_chart


def _prof_students(students, prof_name):
    return [s for s in students if s[5] and prof_name.strip() in s[5]]


def build(app):
    page = app.page
    professors = get_professor_names()
    if not professors:
        return ft.Column(
            [
                ft.Text("Professors", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("No professors found in the database."),
            ]
        )

    state = {"active_prof": professors[0], "active_subtab": "Overview"}
    prof_buttons = {}
    subtab_buttons = {}
    content_area = ft.Container(expand=True)

    def render_overview(prof_name):
        students = get_all_students_with_status()
        prof_students = _prof_students(students, prof_name)
        if not prof_students:
            return ft.Text("No students found for this professor.", italic=True)

        headers = ["ID", "Name", "Email", "Course", "Subject", "Status"]
        col_flex = [1, 2, 3, 1, 2, 1]

        header_row = ft.Container(
            content=ft.Row(
                [
                    ft.Container(ft.Text(h, weight=ft.FontWeight.BOLD), expand=flex)
                    for h, flex in zip(headers, col_flex)
                ],
                spacing=10,
            ),
            bgcolor="#f4f4f4",
            padding=ft.Padding(left=10, top=10, right=10, bottom=10),
        )

        data_rows = []
        for s in prof_students:
            values = [str(s[0]), s[1] or "", s[2] or "", s[3] or "", s[4] or "", s[9] or ""]
            data_rows.append(
                ft.Container(
                    content=ft.Row(
                        [ft.Container(ft.Text(v), expand=flex) for v, flex in zip(values, col_flex)],
                        spacing=10,
                    ),
                    padding=ft.Padding(left=10, top=8, right=10, bottom=8),
                    border=ft.Border(bottom=ft.BorderSide(1, "#e0e0e0")),
                )
            )

        return ft.Column([header_row] + data_rows, expand=True, scroll=ft.ScrollMode.AUTO)

    def render_statistics(prof_name):
        students = get_all_students_with_status()
        prof_students = _prof_students(students, prof_name)
        student_count = len(prof_students)
        subject_count = len({s[4].strip() for s in prof_students if s[4]})
        course_count = len({s[3].strip() for s in prof_students if s[3]})

        if student_count + subject_count + course_count == 0:
            return ft.Text("No data available", size=16)

        labels, sizes = [], []
        if student_count:
            labels.append("Students")
            sizes.append(student_count)
        if subject_count:
            labels.append("Subjects")
            sizes.append(subject_count)
        if course_count:
            labels.append("Courses")
            sizes.append(course_count)

        colors = ["#66BB6A", "#42A5F5", "#FFA726"]
        src = render_donut_chart(labels, sizes, f"Stats for {prof_name}", colors=colors[: len(sizes)])
        return ft.Container(
            content=ft.Image(src=src, expand=True, fit=ft.BoxFit.CONTAIN),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    def render_content():
        prof = state["active_prof"]
        try:
            if state["active_subtab"] == "Overview":
                content_area.content = render_overview(prof)
            else:
                content_area.content = render_statistics(prof)
        except Exception as ex:
            content_area.content = ft.Text(f"Failed to load: {ex}", color="#be1e2d")

    def switch_subtab(name):
        state["active_subtab"] = name
        for n, btn in subtab_buttons.items():
            active = n == name
            btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        render_content()
        page.update()

    def switch_prof(name):
        state["active_prof"] = name
        state["active_subtab"] = "Overview"
        for n, btn in prof_buttons.items():
            active = n == name
            btn.content.bgcolor = "#181888" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        for n, btn in subtab_buttons.items():
            active = n == "Overview"
            btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        render_content()
        page.update()

    for name in professors:
        btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text(name, weight=ft.FontWeight.BOLD, color="#000000"),
                bgcolor="#FFFFFF", border_radius=5, padding=10,
            ),
            on_click=lambda e, n=name: switch_prof(n),
        )
        prof_buttons[name] = btn

    for name in ["Overview", "Statistics"]:
        btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text(name, weight=ft.FontWeight.BOLD, color="#000000"),
                bgcolor="#FFFFFF", border_radius=5, padding=8,
            ),
            on_click=lambda e, n=name: switch_subtab(n),
        )
        subtab_buttons[name] = btn

    for n, btn in prof_buttons.items():
        active = n == state["active_prof"]
        btn.content.bgcolor = "#181888" if active else "#FFFFFF"
        btn.content.content.color = "#FFFFFF" if active else "#000000"
    for n, btn in subtab_buttons.items():
        active = n == "Overview"
        btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
        btn.content.content.color = "#FFFFFF" if active else "#000000"

    render_content()

    return ft.Column(
        [
            ft.Text("Professors", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row(list(prof_buttons.values()), spacing=5, wrap=True),
            ft.Row(list(subtab_buttons.values()), spacing=5),
            content_area,
        ],
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )
