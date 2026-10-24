import customtkinter as ctk
from tkinter import messagebox
from database import validate_user, update_password
from signup import SignUpWindow
import os
import tkinter as tk
from PIL import Image, ImageTk

base = os.path.dirname(os.path.abspath(__file__))
ico_path  = os.path.join(base, "assets", "my_logo.ico")
png_path  = os.path.join(base, "assets", "my_logo16.png")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("1000x600")
        self.resizable(False, False)

        if os.path.exists(ico_path):
            self.wm_iconbitmap(default=ico_path)
        elif os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            self.iconphoto(True, img)
            self._icon_ref = img 

        # Configure left and right frame
        self.left_frame = ctk.CTkFrame(self, fg_color="#f4f4f4")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self, width=400, fg_color="#181888",corner_radius=0)
        self.right_frame.pack(side="right", fill="both", expand=False)

        # Load images
        logo_path = os.path.join(base, "assets", "test.png")
        logo_path2 = os.path.join(base, "assets", "test.png")

        # Left side content
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
            text="SIGN UP",
            fg_color="#B01927",
            hover_color="#a61a26",
            text_color="white",
            width=120,
            height=35,
            corner_radius=8,
            font=("Arial", 13, "bold"),
            command=self.open_signup_window
        ).place(x=30, y=190)

        # Right side content - login container
        self.login_container = ctk.CTkFrame(
            self.right_frame,
            fg_color="white",
            corner_radius=0,
            width=300,
            height=380
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")
        self.login_container.pack_propagate(False)

        if os.path.exists(logo_path2):
            logo_img2 = Image.open(logo_path2).resize((110, 90))
            self.logo_right_img = ImageTk.PhotoImage(logo_img2)
            ctk.CTkLabel(self.login_container, text="", image=self.logo_right_img).pack(pady=(20, 5))

        # Email
        ctk.CTkLabel(self.login_container, text="EMAIL ADDRESS", font=("sans-serif typeface", 12, "bold"), text_color="#000").pack()
        self.entry_user = ctk.CTkEntry(self.login_container, placeholder_text="Enter email", width=220)
        self.entry_user.pack(pady=(5, 10))

        # Password
        ctk.CTkLabel(self.login_container, text="PASSWORD", font=("sans-serif typeface", 12, "bold"), text_color="#000").pack()
        self.entry_pass = ctk.CTkEntry(self.login_container, placeholder_text="Enter password", show="*", width=220)
        self.entry_pass.pack(pady=(5, 15))
        self.entry_pass.bind('<Return>', lambda e: self._on_login())

        # Login button
        ctk.CTkButton(
            self.login_container,
            text="LOGIN",
            command=self._on_login,
            fg_color="#be1e2d",
            hover_color="#a61a26",
            text_color="white",
            width=160,
            height=35,
            corner_radius=8,
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 8))

        # Forgot password link
        forgot_label = ctk.CTkLabel(
            self.login_container,
            text="Forgot Password?",
            font=("Arial", 11, "underline"),
            text_color="#181888",
            cursor="hand2"
        )
        forgot_label.pack(pady=(0, 20), anchor="center")
        forgot_label.bind("<Button-1>", lambda e: self.open_reset_password_window())

        person_path = os.path.join(base, "assets", "new-model.png")
        if os.path.exists(person_path):
            person_img = Image.open(person_path).resize((300, 320))  # adjust size as needed
            self.person_img = ImageTk.PhotoImage(person_img)
            ctk.CTkLabel(self.left_frame, text="", image=self.person_img).place(x=280, y=280)

        # Add Robot Image (bottom-left of left_frame)
        robot_path = os.path.join(base, "assets", "OED-Robot.png")
        if os.path.exists(robot_path):
            robot_img = Image.open(robot_path).resize((150, 150))  # adjust size as needed
            self.robot_img = ImageTk.PhotoImage(robot_img)
            ctk.CTkLabel(self.left_frame, text="", image=self.robot_img).place(x=50, y=430)

    def open_signup_window(self):
        self.withdraw()  # 👈 Hide login window
        signup = SignUpWindow(self)  # 👈 Open signup window
    
        def on_close():
            self.deiconify()  # 👈 Show login window again
            signup.destroy()

        signup.protocol("WM_DELETE_WINDOW", on_close)

    def _on_login(self):
        email = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return

        if validate_user(email, password):
            self.destroy()  # ✅ Close the login window

        # ✅ Launch the main app
            from main_app import MainApp  # make sure this is the correct filename
            app = MainApp(username=email)
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def open_reset_password_window(self):

        if os.path.exists(ico_path):
            self.wm_iconbitmap(default=ico_path)
        elif os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            self.iconphoto(True, img)
            self._icon_ref = img 
        
        reset_window = ctk.CTkToplevel(self)
        reset_window.title("Reset Password")
        reset_window.geometry("800x600")
        reset_window.resizable(False, False)
        reset_window.configure(fg_color="#181888")

        logo_path = os.path.join(base, "assets", "test.png")

        reset_frame = ctk.CTkFrame(
            reset_window, 
            border_width=2, 
            border_color="#000000", 
            fg_color="#FFFFFF",
            height=450,
            width=350,
            corner_radius=5
        )
        reset_frame.place(relx=.5, rely=.5, anchor="center")
        reset_frame.pack_propagate(False)

        if os.path.exists(logo_path):
            logo_img2 = Image.open(logo_path).resize((110, 90))
            self.logo_right_img = ImageTk.PhotoImage(logo_img2)
            ctk.CTkLabel(reset_frame, text="", image=self.logo_right_img).pack(pady=(20, 5))
        
        ctk.CTkLabel(reset_frame, text="Reset Your Password", font=("Arial", 24, "bold")).pack(pady=(30, 15))
        ctk.CTkLabel(reset_frame, text="Enter your email address:", font=("Arial", 16, "bold")).pack(pady=(5, 0))
        email_entry = ctk.CTkEntry(reset_frame, placeholder_text="Email", width=220)
        email_entry.pack(pady=(10, 20))

        ctk.CTkLabel(reset_frame, text="Enter new password:", font=("Arial", 16, "bold")).pack()
        new_pass_entry = ctk.CTkEntry(reset_frame, placeholder_text="New Password", show="*", width=220)
        new_pass_entry.pack(pady=(10, 20))

        def reset_action():
            email = email_entry.get().strip()
            new_pass = new_pass_entry.get().strip()

            if not email or not new_pass:
                messagebox.showerror("Input Error", "Please enter both email and new password.")
                return

            try:
                success = update_password(email, new_pass)
                if success:
                    messagebox.showinfo("Success", f"Password for {email} has been reset.")
                    reset_window.destroy()
                else:
                    messagebox.showwarning("Not Found", "No user found with that email.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset password:\n{e}")

        ctk.CTkButton(
            reset_frame, 
            text="Reset Password", 
            command=reset_action, 
            width=160,
            fg_color="#181888",
            text_color="#FFFFFF",
            hover_color="#09093B",
            font=("Arial", 16, "bold")
        ).pack(pady=(20, 10))

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
