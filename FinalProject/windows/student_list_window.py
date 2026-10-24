import customtkinter as ctk
from tkinter import messagebox, ttk
from database import get_all_students_with_status, archive_student
import webbrowser
import urllib.parse


def open_gmail_compose(to_email="", subject="", body=""):
    params = {
        "to": to_email,
        "su": subject,
        "body": body
    }
    encoded = urllib.parse.urlencode(params)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&{encoded}"
    webbrowser.open_new(gmail_url)


class StudentListWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#FFFFFF")

        ctk.CTkLabel(self, text="Student List", font=("Arial", 20, "bold"), text_color="black").pack(pady=10)

        # Tab Buttons Frame
        tab_button_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=8)
        tab_button_frame.pack(pady=(0, 10), padx=20)

        self.tabs = ["Software Engineering", "Capstones", "MIT & MIS"]
        self.tab_buttons = {}
        self.tab_frames = {}

        for tab_name in self.tabs:
            btn = ctk.CTkButton(
                tab_button_frame,
                text=tab_name,
                command=lambda name=tab_name: self.show_tab(name),
                width=180,
                height=35,
                fg_color="#FFFFFF",
                font=("Arial", 14, "bold"),
                corner_radius=5
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[tab_name] = btn

        # Tab Content Area
        self.content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for tab_name in self.tabs:
            frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.tab_frames[tab_name] = frame
            self.populate_tab(tab_name, frame)

        self.show_tab("Software Engineering")

    def populate_tab(self, tab_name, frame):
        tree = self.create_treeview(frame)
        self.treeviews = getattr(self, "treeviews", {})
        self.treeviews[tab_name] = tree

        try:
            students = get_all_students_with_status()
            for row in students:
                course = (row[3] or "").strip().lower()
                subject = (row[4] or "").strip().lower()

                if tab_name == "Software Engineering" and "software engineering" in subject:
                    tree.insert("", "end", values=row)
                elif tab_name == "MIT & MIS" and course in ["mit", "mis"]:
                    tree.insert("", "end", values=row)
                elif tab_name == "Capstones" and course in ["bsit", "bscs", "bscpe"] and "software engineering" not in subject:
                    tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student data: {e}")

    def show_tab(self, tab_name):
        for name in self.tab_frames:
            self.tab_frames[name].place_forget()
            self.tab_buttons[name].configure(
                fg_color="#FFFFFF",
                text_color="#000000",
                hover_color="#C2C2C2"
            )

        self.tab_frames[tab_name].place(relx=0, rely=0, relwidth=1, relheight=1)
        self.tab_buttons[tab_name].configure(
            fg_color="#be1e2d",
            hover_color="#a61a26",
            text_color="#FFFFFF"
        )

    def create_treeview(self, parent):
        columns = [
            "ID", "Name", "Email", "Course", "Subject", "Professor",
            "Advisor", "Panel", "Chairman", "Status", "Active Status", "Status Changes"
        ]
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=110)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
        btn_frame.pack(pady=5)

        ctk.CTkButton(
            btn_frame,
            text="Update Selected",
            command=lambda: self.on_update_button(tree),
            fg_color="#181888",
            hover_color="#09093B",
            text_color="#FFFFFF"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Archive Selected",
            command=lambda: self.on_archive_button(tree),
            fg_color="#181888",
            hover_color="#09093B",
            text_color="#FFFFFF"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Send Reminder",
            command=lambda: self.send_reminder(tree),
            fg_color="#181888",
            hover_color="#09093B",
            text_color="#FFFFFF"
        ).pack(side="left", padx=5)

        return tree

    def on_update_button(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to update.")
            return
        student_id = tree.item(selected[0])["values"][0]
        self.master.master.show_update_student(student_id)

    def on_archive_button(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to archive.")
            return
        student_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Archive", f"Archive student ID {student_id}?"):
            try:
                archive_student(student_id)
                messagebox.showinfo("Archived", "Student archived successfully.")
                tree.delete(selected[0])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to archive: {e}")

    def send_reminder(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student.")
            return

        row = tree.item(selected[0])["values"]
        email = row[2]  # Assuming column index 2 is Email
        name = row[1]

        subject = "Reminder: Thesis Progress"
        body = f"Hello {name},\n\nThis is a reminder to check and update your thesis progress.\n\nBest regards,\nThesis Coordinator"

        open_gmail_compose(to_email=email, subject=subject, body=body)
