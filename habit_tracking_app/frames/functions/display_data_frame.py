from typing import List, Union

import customtkinter

from habit_tracking_app.frames.functions.habit import Habit


class DisplayData(customtkinter.CTkScrollableFrame):
    def __init__(self, root: customtkinter.CTkFrame, data: Union[List[Habit], None] = None):
        """Initializes analytics display frame
        :param root: customtkinter.CTkFrame
        :param data: Union[List[Habit], List[None]]
        """
        super().__init__(root, fg_color=("#F9F9FA", "#3B3B3B"))

        self.grid(row=1, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        self.place_labels_on_frame()
        self.place_data_on_frame(data)

    def place_labels_on_frame(self) -> None:
        """Places labels on frame
        :return: None
        """
        labels = [
            "ID:",
            "Title:",
            "Period:",
            "Created_date:",
            "Start_date:",
            "Due_date:",
            "Completed:",
            "Streak:",
            "Max_streak:",
            "Break:",
            "Max_break:"
        ]
        for column_no, label in enumerate(labels):
            label_widget = customtkinter.CTkLabel(
                self, text=label, font=customtkinter.CTkFont(weight="bold"), anchor="w"
            )
            label_widget.grid(row=0, column=column_no, sticky="nsew")

    def place_data_on_frame(self, data: Union[List[Habit], None]) -> None:
        """Places given data on the frame
        :param data: Union[List[Habit], List[None]]
        :return: None
        """
        if data is not None:
            row_no = 1
            for habit in data:
                for column_no, variable in enumerate(habit.as_tuple()):
                    label = customtkinter.CTkLabel(self, text=variable, anchor="w")
                    label.grid(row=row_no, column=column_no, sticky="nsew")
                row_no += 1
