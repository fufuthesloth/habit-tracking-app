import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.habits_page import Habits


class TestHabits(unittest.TestCase):

    @patch("habit_tracking_app.frames.functions.habit.Habit")
    @patch("habit_tracking_app.frames.habits_page.DisplayData")
    @patch("habit_tracking_app.frames.habits_page.DatabaseOperations")
    def test_habits_page_init(self, mocked_database, mocked_display, mocked_habit):
        data = mocked_database.return_value.__enter__.return_value.return_habits_data.return_value = mocked_habit
        habits_frame = Habits(None, None)
        mocked_display.return_value = CTkFrame(habits_frame)
        child_widgets = habits_frame.winfo_children()

        self.assertIsInstance(habits_frame, CTkFrame, "Habits frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 5, "Edit habit frame child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.return_habits_data.assert_called_once()
        mocked_display.assert_called_once_with(habits_frame, data)


if __name__ == '__main__':
    unittest.main()
