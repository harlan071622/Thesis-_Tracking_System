import customtkinter as ctk
import calendar
from datetime import datetime

class CustomCalendar(ctk.CTkFrame):
    def __init__(self, master, on_date_selected=None):
        super().__init__(master, fg_color="#FFFFFF")

        self.on_date_selected = on_date_selected
        self.today = datetime.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_date = None

        self.header_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.header_label.grid(row=0, column=1, columnspan=5, pady=5)

        ctk.CTkButton(self, text="<", width=30, command=self.prev_month).grid(row=0, column=0)
        ctk.CTkButton(self, text=">", width=30, command=self.next_month).grid(row=0, column=6)

        self.day_labels = []
        for idx, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            lbl = ctk.CTkLabel(self, text=day)
            lbl.grid(row=1, column=idx, padx=2, pady=2)

        self.date_buttons = []
        for row in range(6):
            btn_row = []
            for col in range(7):
                btn = ctk.CTkButton(self, text="", width=40, command=lambda r=row, c=col: self.select_date(r, c))
                btn.grid(row=row+2, column=col, padx=2, pady=2)
                btn_row.append(btn)
            self.date_buttons.append(btn_row)

        self.selected_label = ctk.CTkLabel(self, text="Selected Date: None")
        self.selected_label.grid(row=8, column=0, columnspan=7, pady=5)

        self.update_calendar()

    def update_calendar(self):
        self.header_label.configure(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        for r in range(6):
            for c in range(7):
                try:
                    day = month_days[r][c]
                except IndexError:
                    day = 0
                btn = self.date_buttons[r][c]
                if day == 0:
                    btn.configure(text="", state="disabled")
                else:
                    btn.configure(text=str(day), state="normal")

    def select_date(self, row, col):
        day_str = self.date_buttons[row][col].cget("text")
        if day_str:
            day = int(day_str)
            self.selected_date = datetime(self.current_year, self.current_month, day)
            date_str = self.selected_date.strftime("%Y-%m-%d")
            self.selected_label.configure(text=f"Selected Date: {date_str}")
            if self.on_date_selected:
                self.on_date_selected(date_str)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def set_date(self, date_str):
        """Set calendar to a specific date (format: YYYY-MM-DD)."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            self.current_year = date_obj.year
            self.current_month = date_obj.month
            self.selected_date = date_obj.date()
            self.update_calendar()
        except ValueError:
            print("Invalid date format passed to set_date")

    def disable(self):
        for child in self.winfo_children():
            try:
                child.configure(state="disabled")
            except:
                pass

    def enable(self):
        for child in self.winfo_children():
            try:
                child.configure(state="normal")
            except:
                pass