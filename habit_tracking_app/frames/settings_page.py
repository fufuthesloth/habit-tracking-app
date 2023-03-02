from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.config import Config
from habit_tracking_app.frames.functions.database import DatabaseOperations

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class Settings(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes settings frame
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure((0, 4), weight=1)
        self.grid_columnconfigure((0, 1, 4, 5), weight=1)

        self.load_config()

        appearance_mode_label = customtkinter.CTkLabel(self, text="Select appearance mode:", anchor="e")
        appearance_mode_label.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self,
            values=["Dark", "Light"],
            command=self.change_appearance_mode,
            variable=self.appearance_mode_initial_value,
        )
        self.appearance_mode_optionmenu.grid(row=1, column=3, padx=(10, 20), pady=(20, 10))

        color_theme_label = customtkinter.CTkLabel(self, text="Select color theme:", anchor="e")
        color_theme_label.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.color_theme_optionmenu = customtkinter.CTkOptionMenu(
            self,
            values=["blue", "green"],
            command=self.change_color_theme,
            variable=self.color_theme_initial_value,
        )
        self.color_theme_optionmenu.grid(row=2, column=3, padx=(10, 20), pady=(10, 10))

        reset_data_button = customtkinter.CTkButton(
            self, text="Reset all habits", command=lambda: self.controller.display_frame("reset_data_frame")
        )
        reset_data_button.grid(row=3, column=2, columnspan=2, padx=(20, 20), pady=(10, 20))

    def load_config(self) -> None:
        """Loads config of the app
        :return: None
        """
        config = Config().config
        customtkinter.set_appearance_mode(config["appearance_mode"])
        customtkinter.set_default_color_theme(config["color_theme"])
        self.appearance_mode_initial_value = customtkinter.StringVar(value=config["appearance_mode"])
        self.color_theme_initial_value = customtkinter.StringVar(value=config["color_theme"])
        if config["initial_opening"] == "True":
            with DatabaseOperations() as dbo:
                dbo.create_table()
                dbo.insert_predefined_habits()
            Config.save_new_config(config["appearance_mode"], config["color_theme"])

    def change_appearance_mode(self, new_appearance_mode: str) -> None:
        """Changes appearance mode
        :param new_appearance_mode: str
        :return: None
        """
        customtkinter.set_appearance_mode(new_appearance_mode)
        Config.save_new_config(new_appearance_mode, self.color_theme_optionmenu.get())

    def change_color_theme(self, new_color_theme: str) -> None:
        """Changes color theme and reinitializes the frame
        :param new_color_theme: str
        :return: None
        """
        Config.save_new_config(self.appearance_mode_optionmenu.get(), new_color_theme)
        self.controller.reinitialize_container("settings_frame")
