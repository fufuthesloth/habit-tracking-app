from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class MarkAsCompleted(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes mark as completed frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        mark_as_completed_frame_label = customtkinter.CTkLabel(
            self, text="Select habit to mark as completed:", anchor="e"
        )
        mark_as_completed_frame_label.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        with DatabaseOperations() as dbo:
            list_of_habits = dbo.list_of_habits()

        self.mark_as_completed_optionmenu = customtkinter.CTkOptionMenu(self, values=list_of_habits)
        self.mark_as_completed_optionmenu.grid(row=1, column=3, padx=(10, 20), pady=(20, 10), sticky="nsew")

        mark_as_completed_yes_button = customtkinter.CTkButton(self, text="Submit", command=self.mark_as_completed)
        mark_as_completed_yes_button.grid(row=2, column=2, padx=(20, 10), pady=(10, 20))

        mark_as_completed_no_button = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: controller.display_frame("habits_frame")
        )
        mark_as_completed_no_button.grid(row=2, column=3, padx=(10, 20), pady=(10, 20))

    def mark_as_completed(self) -> None:
        """Passes the id of habit to mark as completed to DatabaseOperations.mark_as_completed
        and reinitializes the frame
        :return: None
        """
        with DatabaseOperations() as dbo:
            dbo.mark_as_completed(self.mark_as_completed_optionmenu.get()[0])
        self.controller.reinitialize_container("habits_frame")
