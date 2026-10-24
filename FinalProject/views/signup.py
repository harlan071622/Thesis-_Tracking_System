import bcrypt
import flet as ft

from database import create_user


def build(app):
    page = app.page
    email_field = ft.TextField(label="Email", width=250)
    role_dropdown = ft.Dropdown(
        width=250,
        label="Position",
        options=[ft.DropdownOption(key=r, text=r) for r in ["Professor", "Advisor", "Panel"]],
    )
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=250)
    confirm_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=250)
    error_text = ft.Text("", color="#be1e2d", size=12)

    def do_signup(e):
        email = (email_field.value or "").strip()
        role = role_dropdown.label
        password = (password_field.value or "").strip()
        confirm = (confirm_field.value or "").strip()

        if not email or not role or not password or not confirm:
            error_text.value = "All fields are required."
            page.update()
            return
        if password != confirm:
            error_text.value = "Passwords do not match."
            page.update()
            return

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        try:
            create_user(email, role, hashed)
            error_text.color = "#1a7a1a"
            error_text.value = "Account created successfully."
            page.update()
        except Exception as ex:
            error_text.color = "#be1e2d"
            error_text.value = f"Failed to create account: {ex}"
            page.update()

    signup_card = ft.Container(
        width=300,
        height=360,
        bgcolor="white",
        border_radius=4,
        padding=30,
        margin=40,
        content=ft.Column(
            [
                email_field,
                role_dropdown,
                password_field,
                confirm_field,
                error_text,
                ft.Button("SIGN UP", bgcolor="#181888", color="white", width=160, height=35, on_click=do_signup),
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
                ft.Button("LOGIN", bgcolor="#181888", color="white", width=120, height=35, on_click=lambda e: app.go_login()),
            ],
            spacing=20,
        ),
    )

    right_panel = ft.Container(
        expand=1,
        bgcolor="#B01927",
        alignment=ft.Alignment.CENTER,
        content=signup_card,
    )

    return ft.Row([left_panel, right_panel], expand=True, spacing=0)
