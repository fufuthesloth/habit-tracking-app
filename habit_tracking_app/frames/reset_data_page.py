from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class ResetData(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Intializes reset data frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        reset_data_frame_label = customtkinter.CTkLabel(self, text="Are you sure you want to remove all data?")
        reset_data_frame_label.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")

        reset_data_frame_yes_button = customtkinter.CTkButton(self, text="Yes", command=self.reset_data)
        reset_data_frame_yes_button.grid(row=2, column=2, padx=(20, 10), pady=(10, 20))

        reset_data_frame_no_button = customtkinter.CTkButton(
            self, text="No", command=lambda: self.controller.display_frame("settings_frame")
        )
        reset_data_frame_no_button.grid(row=2, column=3, padx=(10, 20), pady=(10, 20))

    def reset_data(self) -> None:
        """Initializes function to reset all data and reinitializes main frame
        :return: None
        """
        with DatabaseOperations() as dbo:
            dbo.reset_data()
        self.controller.reinitialize_container("settings_frame")
