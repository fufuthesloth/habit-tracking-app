import customtkinter

from habit_tracking_app.frames.functions.database import DatabaseOperations
from habit_tracking_app.frames.functions.display_data_frame import DisplayData


class Analytics(customtkinter.CTkFrame):
    def __init__(self, root: customtkinter.CTkFrame):
        """Initializes analytics frame
        :param root: customtkinter.CTkFrame
        """
        super().__init__(root, corner_radius=0, fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.analytics_tabview = customtkinter.CTkTabview(self, height=1)
        self.analytics_tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 10))

        general_tab = self.analytics_tabview.add("General analytics functions")
        general_tab.grid_columnconfigure((0, 3), weight=1)

        specific_tab = self.analytics_tabview.add("Habit specific analytics functions")
        specific_tab.grid_columnconfigure((0, 4), weight=1)

        self.general_functions_optionmenu = customtkinter.CTkOptionMenu(
            general_tab,
            values=[
                "Display all habits",
                "Display all daily habits",
                "Display all weekly habits",
                "Display habit(s) with currently the longest break",
                "Display habit(s) with the longest max break",
                "Display habit(s) with currently the longest streak",
                "Display habit(s) with the longest max streak",
                "Display the longest tracked habit",
                "Display the shortest tracked habit"]
        )
        self.general_functions_optionmenu.grid(row=0, column=1, padx=(20, 10), pady=(20, 0))

        general_functions_submit_button = customtkinter.CTkButton(
            general_tab, text="Submit", command=self.select_analytics_function
        )
        general_functions_submit_button.grid(row=0, column=2, padx=(10, 20), pady=(20, 0))

        self.habit_specific_functions_optionmenu = customtkinter.CTkOptionMenu(
            specific_tab,
            values=[
                "Display history of habit",
                "Display habit information",
                "Display the max streak"]
        )
        self.habit_specific_functions_optionmenu.grid(row=0, column=1, padx=(20, 10), pady=(20, 0))

        with DatabaseOperations() as dbo:
            list_of_habits = dbo.list_of_habits()

        self.select_habit_optionmenu = customtkinter.CTkOptionMenu(specific_tab, values=list_of_habits)
        self.select_habit_optionmenu.grid(row=0, column=2, padx=(10, 10), pady=(20, 0))

        specific_functions_submit_button = customtkinter.CTkButton(
            specific_tab, text="Submit", command=self.select_analytics_function
        )
        specific_functions_submit_button.grid(row=0, column=3, padx=(10, 20), pady=(20, 0))

        self.frame = DisplayData(self)

    def select_analytics_function(self) -> None:
        """Destroys currently displayed frame and displays new frame with data for a given function
        :return: None
        """
        self.frame.destroy()
        with DatabaseOperations() as dbo:
            if self.analytics_tabview.get() == "General analytics functions":
                match self.general_functions_optionmenu.get():
                    case "Display all habits":
                        self.frame = DisplayData(self, dbo.return_habits_data())
                    case "Display all daily habits":
                        self.frame = DisplayData(self, dbo.return_daily_habits())
                    case "Display all weekly habits":
                        self.frame = DisplayData(self, dbo.return_weekly_habits())
                    case "Display habit(s) with currently the longest break":
                        self.frame = DisplayData(self, dbo.return_currently_longest_break())
                    case "Display habit(s) with the longest max break":
                        self.frame = DisplayData(self, dbo.return_max_break())
                    case "Display habit(s) with currently the longest streak":
                        self.frame = DisplayData(self, dbo.return_currently_longest_streak())
                    case "Display habit(s) with the longest max streak":
                        self.frame = DisplayData(self, dbo.return_max_streak())
                    case "Display the longest tracked habit":
                        self.frame = DisplayData(self, dbo.return_longest_tracked_habit())
                    case "Display the shortest tracked habit":
                        self.frame = DisplayData(self, dbo.return_shortest_tracked_habit())
            else:
                habit = self.select_habit_optionmenu.get()[0]
                match self.habit_specific_functions_optionmenu.get():
                    case "Display history of habit":
                        self.frame = DisplayData(self, dbo.display_history(habit))
                    case "Display habit information":
                        self.frame = DisplayData(self, dbo.display_habit_information(habit))
                    case "Display the max streak":
                        self.frame = DisplayData(self, dbo.display_max_streak(habit))
