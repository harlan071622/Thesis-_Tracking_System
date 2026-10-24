import flet as ft


class AppState:
    def __init__(self, page: ft.Page):
        self.page = page
        self.username = None
        self.content = ft.Container(expand=True, bgcolor="#FFFFFF", padding=10)
        self.nav_buttons = {}
        self.active_nav = None
        self.selected_student_id = None

    # --- top level views ---
    def go_login(self):
        from views import login

        self.username = None
        self.page.controls.clear()
        self.page.controls.append(login.build(self))
        self.page.update()

    def go_signup(self):
        from views import signup

        self.page.controls.clear()
        self.page.controls.append(signup.build(self))
        self.page.update()

    def go_main(self, username):
        self.username = username
        from database import fetch_dropdown_options

        fetch_dropdown_options()

        self.page.controls.clear()
        self.page.controls.append(self._build_shell())
        self.page.update()
        self.show_student_list()

    def _build_shell(self):
        nav_specs = [
            ("Student List", self.show_student_list),
            ("Add Student", self.show_add_student),
            ("Show Archive", self.show_archive),
            ("Professors", self.show_professors),
            ("Charts", self.show_charts),
        ]

        self.nav_buttons = {}
        nav_items = []
        for label, handler in nav_specs:
            btn = ft.TextButton(
                content=ft.Container(
                    content=ft.Text(label, color="#000000", weight=ft.FontWeight.BOLD),
                    bgcolor="#FFFFFF",
                    border_radius=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                ),
                on_click=lambda e, h=handler: h(),
                style=ft.ButtonStyle(padding=0),
            )
            self.nav_buttons[label] = btn
            nav_items.append(btn)

        logout_btn = ft.TextButton(
            content=ft.Container(
                content=ft.Text("Logout", color="#000000", weight=ft.FontWeight.BOLD),
                bgcolor="#FFFFFF",
                border_radius=10,
                padding=10,
                alignment=ft.Alignment.CENTER,
            ),
            on_click=lambda e: self.go_login(),
            style=ft.ButtonStyle(padding=0),
        )

        sidebar = ft.Container(
            width=200,
            bgcolor="#181888",
            padding=10,
            content=ft.Column(
                [
                    ft.Column(nav_items, spacing=8),
                    ft.Container(expand=True),
                    logout_btn,
                ],
                expand=True,
            ),
        )

        return ft.Row([sidebar, self.content], expand=True, spacing=0)

    def _set_active_nav(self, label):
        self.active_nav = label
        for name, btn in self.nav_buttons.items():
            active = name == label
            btn.content.bgcolor = "#be1e2d" if active else "#FFFFFF"
            btn.content.content.color = "#FFFFFF" if active else "#000000"

    def set_content(self, control):
        self.content.content = control
        self.page.update()

    # --- screens ---
    def show_student_list(self):
        from views import student_list

        self._set_active_nav("Student List")
        self.set_content(student_list.build(self))

    def show_add_student(self):
        from database import fetch_dropdown_options

        fetch_dropdown_options()
        from views import add_student

        self._set_active_nav("Add Student")
        self.set_content(add_student.build(self))

    def show_update_student(self, student_id):
        from database import fetch_dropdown_options

        fetch_dropdown_options()
        from views import update_student

        self.selected_student_id = student_id
        self._set_active_nav("Student List")
        self.set_content(update_student.build(self, student_id))

    def show_archive(self):
        from views import archive

        self._set_active_nav("Show Archive")
        self.set_content(archive.build(self))

    def show_professors(self):
        from views import professors

        self._set_active_nav("Professors")
        self.set_content(professors.build(self))

    def show_charts(self):
        from views import charts

        self._set_active_nav("Charts")
        self.set_content(charts.build(self))
