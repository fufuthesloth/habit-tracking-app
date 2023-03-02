from __future__ import annotations
from typing import TYPE_CHECKING

import customtkinter

from habit_tracking_app.frames.functions.icons import load_icon

if TYPE_CHECKING:
    from habit_tracking_app.main import App


class Menu(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame, controller: App):
        """Initializes navigation menu
        :param root: customtkinter.CTkFrame
        :param controller: App
        """
        super().__init__(root, corner_radius=0)
        self.controller = controller

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(6, weight=1)

        menu_frame_label = customtkinter.CTkLabel(
            self, text="Habit tracker", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        menu_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_page_button = self.add_menu_button("Home", load_icon("home"), "home_frame")
        self.home_page_button.grid(row=1, column=0, padx=(0, 1), sticky="ew")

        self.habits_page_button = self.add_menu_button("Habits", load_icon("habits"), "habits_frame")
        self.habits_page_button.grid(row=2, column=0, padx=(0, 1), sticky="ew")

        self.analytics_page_button = self.add_menu_button("Analytics", load_icon("analytics"), "analytics_frame")
        self.analytics_page_button.grid(row=3, column=0, padx=(0, 1), sticky="ew")

        self.settings_page_button = self.add_menu_button("Settings", load_icon("settings"), "settings_frame")
        self.settings_page_button.grid(row=4, column=0, padx=(0, 1), sticky="ew")

        self.exit_page_button = self.add_menu_button("Exit", load_icon("exit"), "exit_frame")
        self.exit_page_button.grid(row=5, column=0, padx=(0, 1), sticky="ew")

    def add_menu_button(
            self, button_name: str, icon_name: customtkinter.CTkImage, frame_name: str
    ) -> customtkinter.CTkButton:
        """Takes the name, image object and function to trigger on click, and creates CTkButton
        :param button_name: str
        :param icon_name: CTkImage
        :param frame_name: str
        :return: CTkButton
        """
        return customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=button_name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("grey70", "grey30"),
            image=icon_name,
            anchor="w",
            command=lambda: self.change_frame(frame_name)
        )

    def change_frame(self, frame_name: str) -> None:
        """Highlights the button and calls the function assigned to it
        :param frame_name: str
        :return: None
        """
        self.home_page_button.configure(fg_color=("gray75", "gray25") if frame_name == "home_frame" else "transparent")
        self.habits_page_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "habits_frame" else "transparent"
        )
        self.analytics_page_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "analytics_frame" else "transparent"
        )
        self.settings_page_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "settings_frame" else "transparent"
        )
        self.exit_page_button.configure(fg_color=("gray75", "gray25") if frame_name == "exit_frame" else "transparent")
        self.controller.display_frame(frame_name)
