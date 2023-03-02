import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.delete_habit_page import DeleteHabit


class TestDeleteHabit(unittest.TestCase):

    @patch("habit_tracking_app.frames.delete_habit_page.DatabaseOperations")
    def test_delete_habit_page_init(self, mocked_database):
        delete_habit_frame = DeleteHabit(None, None)
        child_widgets = delete_habit_frame.winfo_children()

        self.assertIsInstance(delete_habit_frame, CTkFrame, "Delete habit frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 4, "Delete habit frame child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.list_of_habits.assert_called_once()

    @patch("habit_tracking_app.frames.delete_habit_page.DatabaseOperations")
    @patch("main.App")
    def test_delete_habit(self, mocked_controller, mocked_database):
        delete_habit_frame = DeleteHabit(None, mocked_controller)
        delete_habit_frame.delete_habit()

        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        mocked_database.return_value.__enter__.return_value.delete_habit.assert_called_once_with(
            delete_habit_frame.delete_habit_optionmenu.get()[0]
        )
        mocked_controller.reinitialize_container.assert_called_once_with("habits_frame")


if __name__ == '__main__':
    unittest.main()
