import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.analytics_page import Analytics


class TestAnalytics(unittest.TestCase):

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_analytics_init(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        mocked_display.return_value = CTkFrame(analytics_frame)
        frame_child_widgets = analytics_frame.winfo_children()
        tabview_child_widgets = analytics_frame.analytics_tabview.winfo_children()
        general_tabview_child_widgets = \
            analytics_frame.analytics_tabview.tab("General analytics functions").winfo_children()
        habit_specific_tabview_child_widgets = \
            analytics_frame.analytics_tabview.tab("Habit specific analytics functions").winfo_children()

        self.assertIsInstance(analytics_frame, CTkFrame, "Display frame is not CTkFrame")
        self.assertEqual(len(frame_child_widgets), 2, "Analytics frame child widgets count is incorrect")
        self.assertEqual(len(tabview_child_widgets), 2, "Analytics tabview child widgets count is incorrect")
        self.assertEqual(len(general_tabview_child_widgets), 2,
                         "General analytics tabview child widgets count is incorrect")
        self.assertEqual(len(habit_specific_tabview_child_widgets), 3,
                         "Habit specific analytics tabview child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.list_of_habits.assert_called_once()
        mocked_display.assert_called_once_with(analytics_frame)

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_all_habits(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display all habits")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_habits_data

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_all_daily_habits(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display all daily habits")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_daily_habits

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_all_weekly_habits(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display all weekly habits")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_weekly_habits

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_currently_longest_break(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display habit(s) with currently the longest break")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_currently_longest_break

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_longest_max_break(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display habit(s) with the longest max break")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_max_break

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_currently_longest_streak(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display habit(s) with currently the longest streak")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_currently_longest_streak

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_longest_max_streak(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display habit(s) with the longest max streak")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_max_streak

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_longest_tracked_habit(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display the longest tracked habit")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_longest_tracked_habit

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_shortest_tracked_habit(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("General analytics functions")
        analytics_frame.general_functions_optionmenu.set("Display the shortest tracked habit")
        analytics_frame.select_analytics_function()
        database_query = mocked_database.return_value.__enter__.return_value.return_shortest_tracked_habit

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once()

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_history_of_habit(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("Habit specific analytics functions")
        analytics_frame.habit_specific_functions_optionmenu.set("Display history of habit")
        analytics_frame.select_analytics_function()
        habit = analytics_frame.select_habit_optionmenu.get()[0]
        database_query = mocked_database.return_value.__enter__.return_value.display_history

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once_with(habit)

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_habit_information(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("Habit specific analytics functions")
        analytics_frame.habit_specific_functions_optionmenu.set("Display habit information")
        analytics_frame.select_analytics_function()
        habit = analytics_frame.select_habit_optionmenu.get()[0]
        database_query = mocked_database.return_value.__enter__.return_value.display_habit_information

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once_with(habit)

    @patch("habit_tracking_app.frames.analytics_page.DisplayData")
    @patch("habit_tracking_app.frames.analytics_page.DatabaseOperations")
    def test_select_analytics_function_habit_max_streak(self, mocked_database, mocked_display):
        analytics_frame = Analytics(None)
        analytics_frame.analytics_tabview.set("Habit specific analytics functions")
        analytics_frame.habit_specific_functions_optionmenu.set("Display the max streak")
        analytics_frame.select_analytics_function()
        habit = analytics_frame.select_habit_optionmenu.get()[0]
        database_query = mocked_database.return_value.__enter__.return_value.display_max_streak

        mocked_display.return_value.destroy.assert_called_once()
        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        self.assertEqual(mocked_display.call_count, 2, "DisplayData was not called right amount of times")
        mocked_display.assert_called_with(analytics_frame, database_query.return_value)
        database_query.assert_called_once_with(habit)


if __name__ == '__main__':
    unittest.main()
