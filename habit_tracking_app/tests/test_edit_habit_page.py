import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.edit_habit_page import EditHabit


class TestEditHabit(unittest.TestCase):

    @patch("habit_tracking_app.frames.edit_habit_page.DatabaseOperations")
    def test_edit_habit_page_init(self, mocked_database):
        edit_habit_frame = EditHabit(None, None)
        child_widgets = edit_habit_frame.winfo_children()

        self.assertIsInstance(edit_habit_frame, CTkFrame, "Edit habit frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 10, "Edit habit frame child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.list_of_habits.assert_called_once()

    @patch("habit_tracking_app.frames.edit_habit_page.DatabaseOperations")
    @patch("main.App")
    def test_edit_habit(self, mocked_controller, mocked_database):
        edit_habit_frame = EditHabit(None, mocked_controller)
        edit_habit_frame.edit_habit()
        id_ = edit_habit_frame.habit_to_edit_combobox.get()[0]
        new_title = edit_habit_frame.new_habit_title_entry.get()
        new_period = edit_habit_frame.new_habit_period_optionmenu.get()
        new_starting_date = edit_habit_frame.new_habit_start_date_date_entry.get()

        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        mocked_database.return_value.__enter__.return_value.update_habit.assert_called_once_with(
            id_, new_title, new_period, new_starting_date)
        mocked_controller.reinitialize_container.assert_called_once_with("habits_frame")


if __name__ == '__main__':
    unittest.main()
