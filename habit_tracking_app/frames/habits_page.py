from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations
from habit_tracking_app.frames.functions.display_data_frame import DisplayData

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class Habits(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes habits frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        with DatabaseOperations() as dbo:
            data = dbo.return_habits_data()

        display_frame = DisplayData(self, data)
        display_frame.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 10), sticky="nsew")

        habits_add_button = customtkinter.CTkButton(
            self, text="Add", command=lambda: controller.display_frame("add_new_habit_frame")
        )
        habits_add_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 20))

        habits_edit_button = customtkinter.CTkButton(
            self, text="Edit", command=lambda: controller.display_frame("edit_habit_frame")
        )
        habits_edit_button.grid(row=1, column=1, padx=(10, 10), pady=(10, 20))

        habits_delete_button = customtkinter.CTkButton(
            self, text="Delete", command=lambda: controller.display_frame("delete_habit_frame")
        )
        habits_delete_button.grid(row=1, column=2, padx=(10, 10), pady=(10, 20))

        habits_mark_as_completed_button = customtkinter.CTkButton(
            self, text="Mark as completed", command=lambda: controller.display_frame("mark_as_completed_frame")
        )
        habits_mark_as_completed_button.grid(row=1, column=3, padx=(10, 20), pady=(10, 20))
