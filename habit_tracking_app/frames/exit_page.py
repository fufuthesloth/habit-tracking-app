from __future__ import annotations
from sys import exit
from typing import TYPE_CHECKING

import customtkinter

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class Exit(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes exit frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        exit_frame_label = customtkinter.CTkLabel(self, text="Are you sure you want to exit?")
        exit_frame_label.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")

        exit_frame_yes_button = customtkinter.CTkButton(self, text="Yes", command=exit)
        exit_frame_yes_button.grid(row=2, column=2, padx=(20, 10), pady=(10, 20))

        exit_frame_no_button = customtkinter.CTkButton(
            self, text="No", command=lambda: controller.display_frame("home_frame")
        )
        exit_frame_no_button.grid(row=2, column=3, padx=(10, 20), pady=(10, 20))
