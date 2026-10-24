import customtkinter as ctk
import tkinter as tk
import os

from windows.add_student_window import AddStudentWindow
from windows.archive_window import ArchiveWindow
from windows.update_student_window import UpdateStudentWindow
from windows.professor_window import ProfessorWindow
from windows.charts_window import ChartsWindow
from windows.student_list_window import StudentListWindow
from windows.add_student_window import AddStudentWindow
from database import fetch_dropdown_options
from windows.professor_window import ProfessorWindow
from windows.charts_window import ChartsWindow
from login import LoginWindow
from tkinter import messagebox
from database import fetch_dropdown_options

class MainApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        
        base      = os.path.dirname(__file__)
        ico_path  = os.path.join(base, "assets", "my_logo.ico")
        png_path  = os.path.join(base, "assets", "my_logo16.png")

        if os.path.exists(ico_path):
            self.wm_iconbitmap(default=ico_path)
        elif os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            self.iconphoto(True, img)
            self._icon_ref = img 
        
        self.title("Thesis Tracker – Main")
        self.geometry("1280x720")
        self.resizable(True, True)
        
        self.sidebar_expanded = True

        self.sidebar = ctk.CTkFrame(
            self, 
            width=200, 
            fg_color="#181888",
            corner_radius=0
            )
        self.sidebar.pack(side="left", fill="y")
        
        self.toggle_btn = ctk.CTkButton(
            self.sidebar,
            text="≡",
            width=30,
            command=self.toggle_sidebar
        )
        self.toggle_btn.pack(pady=10)

        self.sidebar_inner_frame = ctk.CTkFrame(self.sidebar, fg_color="#181888")
        self.sidebar_inner_frame.pack(fill="both", expand=True)

        self.top_button_frame = ctk.CTkFrame(self.sidebar_inner_frame, fg_color="#181888")
        self.top_button_frame.pack(fill="both", expand=True)

        self.bottom_button_frame = ctk.CTkFrame(self.sidebar_inner_frame, fg_color="#181888")
        self.bottom_button_frame.pack(fill="x", pady=10)


        self.btn_specs = [
            ("Student List", self.show_student_list),
            ("Add Student", self.show_add_student),
            ("Show Archive", self.show_archive),
            ("Professors", self.show_professors),
            ("Charts", self.show_charts)
        ]
        self.logout_spec = ("Logout", self.logout_user)

        self.buttons = []
        for text, cmd in self.btn_specs:
            btn = ctk.CTkButton(
                self.top_button_frame,
                text=text,
                command=cmd,
                fg_color="#FFFFFF",
                text_color="#000000",
                corner_radius=10,
                hover_color="#E9E9E9"
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons.append(btn)
        
        logout_btn = ctk.CTkButton(
            self.bottom_button_frame,
            text=self.logout_spec[0],
            command=self.logout_spec[1],
            fg_color="#FFFFFF",
            text_color="#000000",
            hover_color="#be1e2d",
            corner_radius=10
            )
        logout_btn.pack(fill="x", padx=10)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.show_student_list()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_inner_frame.pack_forget()  # 🔹 Hide all
            self.sidebar.configure(width=50)
        else:
            self.sidebar.configure(width=200)
            self.sidebar_inner_frame.pack(fill="both", expand=True)  # 🔹 Show all

        self.sidebar_expanded = not self.sidebar_expanded
        
    def _clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_add_student(self, username=None):
        fetch_dropdown_options()
        self._clear_content()
        AddStudentWindow(self.content_frame).pack(fill="both", expand=True)

    def show_student_list(self):
        self._clear_content()
        StudentListWindow(self.content_frame).pack(fill="both", expand=True)

    def show_update_student(self, student_id=None):
    # 1) If no ID was explicitly passed in, grab it from the Treeview
        if student_id is None:
            list_view = self.content_frame.winfo_children()[0]
            sel = list_view.tree.selection()
            if not sel:
                messagebox.showwarning("No selection", "Please select a student first.")
                return
            student_id = list_view.tree.item(sel[0], "values")[0]

        # 2) (optional) make sure your dropdown-data is loaded
        fetch_dropdown_options()

        # 3) launch the Toplevel popup — no pack(), no clear_content()
        UpdateStudentWindow(self, student_id)
        
    def show_archive(self):
        self._clear_content()
        ArchiveWindow(self.content_frame).pack(fill="both", expand=True)

    def show_professors(self):
        self._clear_content()
        ProfessorWindow(self.content_frame).pack(fill="both", expand=True)

    def show_charts(self):
        self._clear_content()
        ChartsWindow(self.content_frame).pack(fill="both", expand=True)
        
    def _placeholder_student_list(self, master):
        """Temporary placeholder content for student list."""
        frame = ctk.CTkFrame(master)
        lbl = ctk.CTkLabel(frame, text="Student List", font=ctk.CTkFont(size=20)).pack(pady=20)
        lbl(frame, text="(This will show a table of students later)").pack()
        return frame
        
    def _load_frame(self, frame_class):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if isinstance(frame_class, type):
            frame = frame_class(self.content_frame)
        else:
            frame = frame_class(self.content_frame)
        frame.pack(fill="both", expand=True)
    def logout_user(self):
        if not self.sidebar_expanded:
            self.toggle_sidebar()
        self.destroy()
        LoginWindow().mainloop()
        
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
