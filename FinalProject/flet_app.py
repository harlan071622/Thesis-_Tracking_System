import truststore

truststore.inject_into_ssl()

import flet as ft

from views.app_state import AppState


def main(page: ft.Page):
    page.title = "Thesis Tracker"
    page.padding = 0
    page.bgcolor = "#f4f4f4"

    app = AppState(page)
    app.go_login()


ft.run(main)
