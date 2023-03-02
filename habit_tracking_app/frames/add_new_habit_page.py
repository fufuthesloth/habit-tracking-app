from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

import customtkinter
from tkcalendar import DateEntry

from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class AddNewHabit(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes add new habit frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 5), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        new_habit_title_label = customtkinter.CTkLabel(self, text="Enter title of new habit:", anchor="e")
        new_habit_title_label.grid(row=1, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_title_entry = customtkinter.CTkEntry(self, placeholder_text="Title")
        self.new_habit_title_entry.grid(row=1, column=3, padx=(10, 20), pady=(10, 10), sticky="nsew")

        new_habit_period_label = customtkinter.CTkLabel(self, text="Select period of new habit:", anchor="e")
        new_habit_period_label.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_period_optionmenu = customtkinter.CTkOptionMenu(self, values=["daily", "weekly"])
        self.new_habit_period_optionmenu.grid(row=2, column=3, padx=(10, 20), pady=(10, 10), sticky="nsew")

        new_habit_start_date_label = customtkinter.CTkLabel(self, text="Select starting date of new habit:", anchor="e")
        new_habit_start_date_label.grid(row=3, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_start_date_date_entry = DateEntry(self, mindate=date.today(), date_pattern="y-mm-dd")
        self.new_habit_start_date_date_entry.grid(row=3, column=3, padx=(10, 20), pady=(10, 10))

        add_new_habit_submit_button = customtkinter.CTkButton(self, text="Submit", command=self.create_new_habit)
        add_new_habit_submit_button.grid(row=4, column=2, padx=(20, 10), pady=(10, 20))

        add_new_habit_cancel_button = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: controller.display_frame("habits_frame")
        )
        add_new_habit_cancel_button.grid(row=4, column=3, padx=(10, 20), pady=(10, 20))

    def create_new_habit(self) -> None:
        """Collects the values, passes them to DatabaseOperations.insert_new_habit and reinitializes the frame
        :return: None
        """
        title = self.new_habit_title_entry.get()
        period = self.new_habit_period_optionmenu.get()
        start_date = self.new_habit_start_date_date_entry.get()
        with DatabaseOperations() as dbo:
            dbo.insert_new_habit(title, period, start_date)
        self.controller.reinitialize_container("habits_frame")
