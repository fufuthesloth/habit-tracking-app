import os

import customtkinter

from habit_tracking_app.frames import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Habit tracker")
        self.geometry(f"{1280}x{640}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", lambda: self.display_frame("exit_frame"))

        self.container_init()

    def container_init(self, frame_name: str = "home_frame") -> None:
        """Initializes container frame, navigation menu and all pages. Calls function to display given frame
        :param frame_name: str
        :return: None
        """
        self.container = customtkinter.CTkFrame(self, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        Menu(self.container, self)

        self.frames = {
            "settings_frame": Settings(self.container, self),
            "home_frame": Home(self.container),
            "habits_frame": Habits(self.container, self),
            "add_new_habit_frame": AddNewHabit(self.container, self),
            "edit_habit_frame": EditHabit(self.container, self),
            "delete_habit_frame": DeleteHabit(self.container, self),
            "mark_as_completed_frame": MarkAsCompleted(self.container, self),
            "analytics_frame": Analytics(self.container),
            "reset_data_frame": ResetData(self.container, self),
            "exit_frame": Exit(self.container, self)
        }

        for frame in self.frames.keys():
            self.frames[frame].grid(row=0, column=1, sticky="nsew")
        self.display_frame(frame_name)

    def display_frame(self, frame_name: str) -> None:
        """Displays given frame
        :param frame_name: str
        :return: None
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def reinitialize_container(self, frame_name: str) -> None:
        """Reinitializes container
        :param frame_name: str
        :return: None
        """
        self.container.destroy()
        self.container_init(frame_name)


def run():
    os.chdir(os.path.dirname(__file__))
    app = App()
    app.mainloop()


if __name__ == '__main__':
    run()
