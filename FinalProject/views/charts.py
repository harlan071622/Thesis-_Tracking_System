import flet as ft

from database import get_all_students_with_status, get_archived_students
from views.charts_util import count_by, render_donut_chart

ACTIVE_SPECS = [
    ("Status Distribution", 9, "Thesis Status Distribution"),
    ("Course Breakdown", 3, "Course Breakdown"),
    ("Subject Breakdown", 4, "Subject Breakdown"),
    ("Professor Breakdown", 5, "Professor Breakdown"),
    ("Advisor Breakdown", 6, "Advisor Breakdown"),
    ("Panel Breakdown", 7, "Panel Breakdown"),
    ("Chairman Breakdown", 8, "Chairman Breakdown"),
]


def build(app):
    page = app.page
    state = {"main_tab": "Active Students", "active_sub": ACTIVE_SPECS[0][0]}
    main_buttons = {}
    sub_buttons = {}
    content_area = ft.Container(expand=True, alignment=ft.Alignment.CENTER)
    sub_tabs_row = ft.Row([], spacing=5, wrap=True)

    def render_active_vs_inactive():
        data = get_all_students_with_status()
        counts = {"Active": 0, "Inactive": 0}
        for rec in data:
            status = rec[10] or "Active"
            counts[status] = counts.get(status, 0) + 1
        labels, sizes = list(counts.keys()), list(counts.values())
        if sum(sizes) == 0:
            return ft.Text("No data available")
        src = render_donut_chart(labels, sizes, "Active vs Inactive")
        return ft.Image(src=src, expand=True, fit=ft.BoxFit.CONTAIN)

    def render_breakdown(index, title):
        data = get_all_students_with_status()
        labels, sizes = count_by(data, index)
        if not sizes:
            return ft.Text("No data available")
        src = render_donut_chart(labels, sizes, title)
        return ft.Image(src=src, expand=True, fit=ft.BoxFit.CONTAIN)

    def render_archived_vs_not():
        archived = len(get_archived_students())
        active = len(get_all_students_with_status())
        if archived + active == 0:
            return ft.Text("No data available")
        src = render_donut_chart(["Archived", "Not Archived"], [archived, active], "Archived vs Not Archived")
        return ft.Image(src=src, expand=True, fit=ft.BoxFit.CONTAIN)

    def render_content():
        try:
            if state["main_tab"] == "Archived Students":
                content_area.content = render_archived_vs_not()
                return
            sub = state["active_sub"]
            if sub == "Active vs Inactive":
                content_area.content = render_active_vs_inactive()
                return
            for label, index, title in ACTIVE_SPECS:
                if label == sub:
                    content_area.content = render_breakdown(index, title)
                    return
        except Exception as ex:
            content_area.content = ft.Text(f"Failed to load chart: {ex}", color="#be1e2d")

    def switch_sub(name):
        state["active_sub"] = name
        for n, btn in sub_buttons.items():
            active = n == name
            btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        render_content()
        page.update()

    def switch_main(name):
        state["main_tab"] = name
        for n, btn in main_buttons.items():
            active = n == name
            btn.content.bgcolor = "#181888" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"
        sub_tabs_row.visible = name == "Active Students"
        render_content()
        page.update()

    for name in ["Active Students", "Archived Students"]:
        btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text(name, weight=ft.FontWeight.BOLD, color="#000000"),
                bgcolor="#FFFFFF", border_radius=5, padding=10,
            ),
            on_click=lambda e, n=name: switch_main(n),
        )
        main_buttons[name] = btn

    all_sub_names = [s[0] for s in ACTIVE_SPECS] + ["Active vs Inactive"]
    for name in all_sub_names:
        btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text(name, weight=ft.FontWeight.BOLD, color="#000000", size=12),
                bgcolor="#FFFFFF", border_radius=5, padding=8,
            ),
            on_click=lambda e, n=name: switch_sub(n),
        )
        sub_buttons[name] = btn
    sub_tabs_row.controls = list(sub_buttons.values())

    for n, btn in main_buttons.items():
        active = n == state["main_tab"]
        btn.content.bgcolor = "#181888" if active else "#FFFFFF"
        btn.content.content.color = "#FFFFFF" if active else "#000000"
    for n, btn in sub_buttons.items():
        active = n == state["active_sub"]
        btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
        btn.content.content.color = "#FFFFFF" if active else "#000000"

    render_content()

    return ft.Column(
        [
            ft.Text("Charts", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row(list(main_buttons.values()), spacing=5),
            sub_tabs_row,
            content_area,
        ],
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )
