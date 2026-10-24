import customtkinter as ctk
from tkinter import messagebox
from database import create_user
import bcrypt
import os
import tkinter as tk
from PIL import Image, ImageTk

class SignUpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  

        self.title("Sign Up")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        base = os.path.dirname(os.path.abspath(__file__))
        ico_path  = os.path.join(base, "assets", "my_logo.ico")
        png_path  = os.path.join(base, "assets", "my_logo16.png")

        if os.path.exists(ico_path):
            self.wm_iconbitmap(default=ico_path)
        elif os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            self.wm_iconphoto(True, img)
            self._icon_ref = img 
        
        self.left_frame = ctk.CTkFrame(self, fg_color="#f4f4f4")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self, width=400, fg_color="#B01927", corner_radius=0)
        self.right_frame.pack(side="right", fill="both", expand=False)

        logo_path = os.path.join(base, "assets", "test.png")

        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).resize((110, 90))
            self.logo_left_img = ImageTk.PhotoImage(logo_img)
            ctk.CTkLabel(self.left_frame, text="", image=self.logo_left_img).place(x=25, y=20)

        ctk.CTkLabel(
            self.left_frame,
            text="Study Online.\nAnytime, Anywhere.",
            font=("Arial", 20, "bold"),
            text_color="black"
        ).place(x=25, y=130)

        ctk.CTkButton(
            self.left_frame,
            text="LOGIN",
            fg_color="#181888",
            hover_color="#09093B",
            text_color="white",
            width=120,
            height=35,
            corner_radius=8,
            font=("Arial", 13, "bold"),
            command=self.open_login
        ).place(x=30, y=190)

        self.signup_container = ctk.CTkFrame(
            self.right_frame,
            fg_color="white",
            corner_radius=0,
            width=300,
            height=380
        )
        self.signup_container.place(relx=0.5, rely=0.5, anchor="center")
        self.signup_container.pack_propagate(False)

        if os.path.exists(logo_path):
            logo_img2 = Image.open(logo_path).resize((110, 90))
            self.logo_right_img = ImageTk.PhotoImage(logo_img2)
            ctk.CTkLabel(self.signup_container, text="", image=self.logo_right_img).pack(pady=(20, 5))

        self.entry_user = ctk.CTkEntry(self.signup_container, placeholder_text="Email", width=250)
        self.entry_user.pack(pady=10)

        self.option_menu = ctk.CTkOptionMenu(
            self.signup_container,
            values=["Professor", "Advisor", "Panel"],
            font=("Arial", 12, "bold"),
            dropdown_font=("Arial", 12, "bold"),
            dropdown_fg_color="#E9E9E9",
            dropdown_text_color="#000000",
            text_color="#000000",
            button_color="#FFFFFF",
            button_hover_color= "#555555",
            fg_color="#E9E9E9",
            width=250
        )

        self.option_menu.set("Professor")
        self.option_menu.pack()

        self.entry_pass = ctk.CTkEntry(self.signup_container, placeholder_text="Password", show="*", width=250)
        self.entry_pass.pack(pady=10)

        self.entry_confirm = ctk.CTkEntry(self.signup_container, placeholder_text="Confirm Password", show="*", width=250)
        self.entry_confirm.pack(pady=10)

        ctk.CTkButton(
            self.signup_container,
            text="SIGN UP",
            font=("Arial", 14, "bold"),
            fg_color="#181888",
            hover_color="#09093B",
            text_color="white",
            width=120,
            height=35,
            corner_radius=8,
            command=self._on_signup
        ).pack(pady=20)

        person_path = os.path.join(base, "assets", "new-model.png")
        if os.path.exists(person_path):
            person_img = Image.open(person_path).resize((300, 320))  
            self.person_img = ImageTk.PhotoImage(person_img)
            ctk.CTkLabel(self.left_frame, text="", image=self.person_img).place(x=280, y=280)

        robot_path = os.path.join(base, "assets", "OED-Robot.png")
        if os.path.exists(robot_path):
            robot_img = Image.open(robot_path).resize((150, 150))  
            self.robot_img = ImageTk.PhotoImage(robot_img)
            ctk.CTkLabel(self.left_frame, text="", image=self.robot_img).place(x=50, y=430)

    def open_login(self):
        from login import LoginWindow
        self.parent.deiconify()
        self.destroy()

    def _on_signup(self):
        email = self.entry_user.get().strip()
        role = self.option_menu.get().strip()
        password = self.entry_pass.get().strip()
        confirm = self.entry_confirm.get().strip()

        if not email or not role or not password or not confirm:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        if password != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            create_user(email, role, hashed)
            messagebox.showinfo("Success", "Account created successfully.")
            self.parent.deiconify()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")
