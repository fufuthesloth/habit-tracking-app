from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class DeleteHabit(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes delete habit frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        delete_habit_frame_label = customtkinter.CTkLabel(self, text="Select habit to remove:", anchor="e")
        delete_habit_frame_label.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        with DatabaseOperations() as dbo:
            list_of_habits = dbo.list_of_habits()

        self.delete_habit_optionmenu = customtkinter.CTkOptionMenu(self, values=list_of_habits)
        self.delete_habit_optionmenu.grid(row=1, column=3, padx=(10, 20), pady=(20, 10), sticky="nsew")

        delete_habit_yes_button = customtkinter.CTkButton(self, text="Remove", command=self.delete_habit)
        delete_habit_yes_button.grid(row=2, column=2, padx=(20, 10), pady=(10, 20))

        delete_habit_no_button = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: controller.display_frame("habits_frame")
        )
        delete_habit_no_button.grid(row=2, column=3, padx=(10, 20), pady=(10, 20))

    def delete_habit(self) -> None:
        """Passes the id of habit to delete to DatabaseOperations.delete_habit and reinitializes the frame
        :return: None
        """
        with DatabaseOperations() as dbo:
            dbo.delete_habit(self.delete_habit_optionmenu.get()[0])
        self.controller.reinitialize_container("habits_frame")
