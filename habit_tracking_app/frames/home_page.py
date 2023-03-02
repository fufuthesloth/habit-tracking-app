import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations


class Home(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame):
        """Initializes home frame
        :param root: customtkinter.CTkFrame
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        home_frame_welcome_label = customtkinter.CTkLabel(
            self, text="Welcome in the Habit tracking app", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        home_frame_welcome_label.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 10))

        with DatabaseOperations() as dbo:
            dbo.auto_update()
            habits_amount = len(dbo.list_of_ids())
            max_current_streak = dbo.max_current_streak()

        home_frame_tracking_label = customtkinter.CTkLabel(
            self,
            text=f'You are currently tracking {habits_amount} {"habit" if habits_amount == 1 else "habits"}'
            f' and your current highest streak is {max_current_streak} days.'
        )
        home_frame_tracking_label.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))

        home_frame_icons_label = customtkinter.CTkLabel(
            self, text="All icons provided by https://icons8.com", anchor="e"
        )
        home_frame_icons_label.grid(row=4, column=1, padx=(20, 20), pady=(20, 20))