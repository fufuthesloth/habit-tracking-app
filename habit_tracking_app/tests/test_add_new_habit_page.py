from datetime import date
import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.add_new_habit_page import AddNewHabit


class TestAddNewHabit(unittest.TestCase):

    def test_add_new_habit_page_init(self):
        add_new_habit_frame = AddNewHabit(None, None)
        child_widgets = add_new_habit_frame.winfo_children()

        self.assertIsInstance(add_new_habit_frame, CTkFrame, "Add new habit frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 8, "Add new habits frame child widgets count is incorrect")

    @patch("habit_tracking_app.frames.add_new_habit_page.DatabaseOperations")
    @patch("main.App")
    def test_create_new_habit(self, mocked_controller, mocked_database):
        add_new_habit_frame = AddNewHabit(None, mocked_controller)
        add_new_habit_frame.create_new_habit()
        title = add_new_habit_frame.new_habit_title_entry.get()
        period = add_new_habit_frame.new_habit_period_optionmenu.get()
        start_date = add_new_habit_frame.new_habit_start_date_date_entry.get()

        self.assertEqual(title, "", "Title is incorrect")
        self.assertEqual(period, "daily", "Period is incorrect")
        self.assertEqual(start_date, date.today().strftime('%Y-%m-%d'), "Start date is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.insert_new_habit.assert_called_once_with(
            title, period, start_date)
        mocked_controller.reinitialize_container.assert_called_once_with("habits_frame")


if __name__ == '__main__':
    unittest.main()
