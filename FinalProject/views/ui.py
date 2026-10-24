import flet as ft


def show_alert(page: ft.Page, title, message):
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(str(message)),
        actions=[ft.TextButton("OK", on_click=lambda e: page.pop_dialog())],
    )
    page.show_dialog(dlg)


def show_confirm(page: ft.Page, title, message, on_confirm):
    def _confirm(e):
        page.pop_dialog()
        on_confirm()

    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(str(message)),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: page.pop_dialog()),
            ft.Button("Confirm", bgcolor="#be1e2d", color="white", on_click=_confirm),
        ],
    )
    page.show_dialog(dlg)
