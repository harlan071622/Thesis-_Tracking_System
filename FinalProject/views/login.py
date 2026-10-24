import flet as ft

from database import validate_user, update_password


def build(app):
    page = app.page
    email_field = ft.TextField(label="EMAIL ADDRESS", hint_text="Enter email", width=220)
    password_field = ft.TextField(
        label="PASSWORD", hint_text="Enter password", password=True, can_reveal_password=True, width=220
    )
    error_text = ft.Text("", color="#be1e2d", size=12)

    def do_login(e):
        email = (email_field.value or "").strip()
        password = (password_field.value or "").strip()
        if not email or not password:
            error_text.value = "Please enter both email and password."
            page.update()
            return
        try:
            if validate_user(email, password):
                app.go_main(email)
            else:
                error_text.value = "Invalid email or password."
                page.update()
        except Exception as ex:
            error_text.value = f"Error: {ex}"
            page.update()

    password_field.on_submit = do_login

    reset_email = ft.TextField(label="Email", width=220)
    reset_new_password = ft.TextField(label="New Password", password=True, can_reveal_password=True, width=220)
    reset_message = ft.Text("", size=12)

    def do_reset(e):
        email = (reset_email.value or "").strip()
        new_pw = (reset_new_password.value or "").strip()
        if not email or not new_pw:
            reset_message.value = "Please enter both email and new password."
            reset_message.color = "#be1e2d"
            page.update()
            return
        try:
            if update_password(email, new_pw):
                reset_message.value = f"Password for {email} has been reset."
                reset_message.color = "#1a7a1a"
            else:
                reset_message.value = "No user found with that email."
                reset_message.color = "#be1e2d"
        except Exception as ex:
            reset_message.value = f"Error: {ex}"
            reset_message.color = "#be1e2d"
        page.update()

    reset_dialog = ft.AlertDialog(
        title=ft.Text("Reset Your Password"),
        content=ft.Column(
            [
                ft.Text("Enter your email address:"),
                reset_email,
                ft.Text("Enter new password:"),
                reset_new_password,
                reset_message,
            ],
            tight=True,
        ),
        actions=[
            ft.Button("Reset Password", bgcolor="#181888", color="white", on_click=do_reset),
            ft.TextButton("Cancel", on_click=lambda e: page.pop_dialog()),
        ],
    )

    def open_reset_dialog(e):
        reset_email.value = ""
        reset_new_password.value = ""
        reset_message.value = ""
        page.show_dialog(reset_dialog)

    login_card = ft.Container(
        width=300,
        height=300,
        bgcolor="white",
        border_radius=4,
        padding=30,
        margin=40,
        content=ft.Column(
            [
                email_field,
                password_field,
                error_text,
                ft.Button("LOGIN", bgcolor="#be1e2d", color="white", width=160, height=35, on_click=do_login),
                ft.TextButton("Forgot Password?", on_click=open_reset_dialog),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,

        ),
    )

    left_panel = ft.Container(
        expand=2,
        bgcolor="#f4f4f4",
        padding=40,
        content=ft.Column(
            [
                ft.Text("Study Online.\nAnytime, Anywhere.", size=22, weight=ft.FontWeight.BOLD, color="black"),
                ft.Button("SIGN UP", bgcolor="#b01927", color="white", width=120, height=35, on_click=lambda e: app.go_signup()),
            ],
            spacing=20,
        ),
    )

    right_panel = ft.Container(
        expand=1,
        bgcolor="#181888",
        alignment=ft.Alignment.CENTER,
        content=login_card,
    )

    return ft.Row([left_panel, right_panel], expand=True, spacing=0)
