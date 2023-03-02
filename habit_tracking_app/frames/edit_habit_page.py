from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

import customtkinter
from tkcalendar import DateEntry

from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class EditHabit(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes edit habit frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 6), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        habit_to_edit_label = customtkinter.CTkLabel(self, text="Select habit to edit:", anchor="e")
        habit_to_edit_label.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        with DatabaseOperations() as dbo:
            list_of_habits = dbo.list_of_habits()

        self.habit_to_edit_combobox = customtkinter.CTkOptionMenu(self, values=list_of_habits)
        self.habit_to_edit_combobox.grid(row=1, column=3, padx=(10, 20), pady=(20, 10), sticky="nsew")

        new_habit_title_label = customtkinter.CTkLabel(self, text="Enter new title of the habit:", anchor="e")
        new_habit_title_label.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_title_entry = customtkinter.CTkEntry(self, placeholder_text="New title")
        self.new_habit_title_entry.grid(row=2, column=3, padx=(10, 20), pady=(10, 10), sticky="nsew")

        new_habit_period_label = customtkinter.CTkLabel(self, text="Select new period of the habit:", anchor="e")
        new_habit_period_label.grid(row=3, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_period_optionmenu = customtkinter.CTkOptionMenu(self, values=["daily", "weekly"])
        self.new_habit_period_optionmenu.grid(row=3, column=3, padx=(10, 20), pady=(10, 10), sticky="nsew")

        new_habit_start_date_label = customtkinter.CTkLabel(
            self, text="Select new starting date of the habit:", anchor="e"
        )
        new_habit_start_date_label.grid(row=4, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.new_habit_start_date_date_entry = DateEntry(self, mindate=date.today(), date_pattern="y-mm-dd")
        self.new_habit_start_date_date_entry.grid(row=4, column=3, padx=(10, 20), pady=(10, 10))

        edit_habit_submit_button = customtkinter.CTkButton(self, text="Submit", command=self.edit_habit)
        edit_habit_submit_button.grid(row=5, column=2, padx=(20, 10), pady=(10, 20))

        edit_habit_cancel_button = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: controller.display_frame("habits_frame")
        )
        edit_habit_cancel_button.grid(row=5, column=3, padx=(10, 20), pady=(10, 20))

    def edit_habit(self) -> None:
        """Collects the values, passes them to DatabaseOperations.update_habit and reinitializes the frame
        :return: None
        """
        id_ = self.habit_to_edit_combobox.get()[0]
        new_title = self.new_habit_title_entry.get()
        new_period = self.new_habit_period_optionmenu.get()
        new_starting_date = self.new_habit_start_date_date_entry.get()
        with DatabaseOperations() as dbo:
            dbo.update_habit(id_, new_title, new_period, new_starting_date)
        self.controller.reinitialize_container("habits_frame")
