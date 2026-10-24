import customtkinter as ctk
from tkinter import ttk, messagebox
from database import get_archived_students, unarchive_student

class ArchiveWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF")

        ctk.CTkLabel(self, text="Archived Students", font=ctk.CTkFont(size=20)).pack(pady=10)

        # Container for treeview and buttons
        container = ctk.CTkFrame(self, fg_color="#FFFFFF")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview setup
        columns = [
            "ID", "Name", "Email", "Course", "Subject", "Professor",
            "Advisor", "Panel", "Chairman", "Status", "Archived At"
        ]
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        tree_frame = ctk.CTkFrame(container)
        tree_frame.pack(side="top", fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)

        # Buttons frame
        btn_frame = ctk.CTkFrame(container, fg_color="#FFFFFF")
        btn_frame.pack(side="bottom", pady=10)

        unarchive_btn = ctk.CTkButton(
            btn_frame, text="Unarchive Selected", command=self.on_unarchive_button)
        unarchive_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(
            btn_frame, text="Refresh", command=self.load_archived)
        refresh_btn.pack(side="left", padx=5)

        self.load_archived()

    def load_archived(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        archived = get_archived_students()
        if not archived:
            # Show placeholder row
            self.tree.insert("", "end", values=("", "No archive data yet"))
            return

        for row in archived:
            self.tree.insert("", "end", values=row)

    def on_unarchive_button(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an archived student to unarchive.")
            return

        item = self.tree.item(selected[0])
        student_id = item["values"][0]
        confirm = messagebox.askyesno(
            "Confirm Unarchive", f"Restore student ID {student_id} to active list?"
        )
        if not confirm:
            return

        try:
            unarchive_student(student_id)
            messagebox.showinfo("Restored", "Student has been unarchived.")
            self.load_archived()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unarchive: {e}")
