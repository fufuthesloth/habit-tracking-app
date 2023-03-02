import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.mark_as_completed_page import MarkAsCompleted


class TestMarkAsCompleted(unittest.TestCase):

    @patch("habit_tracking_app.frames.mark_as_completed_page.DatabaseOperations")
    def test_mark_as_completed_page_init(self, mocked_database):
        mark_as_completed = MarkAsCompleted(None, None)
        child_widgets = mark_as_completed.winfo_children()

        self.assertIsInstance(mark_as_completed, CTkFrame, "Mark as completed frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 4, "Mark as completed frame child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.list_of_habits.assert_called_once()

    @patch("habit_tracking_app.frames.mark_as_completed_page.DatabaseOperations")
    @patch("main.App")
    def test_mark_as_completed(self, mocked_controller, mocked_database):
        mark_as_completed = MarkAsCompleted(None, mocked_controller)
        mark_as_completed.mark_as_completed()

        self.assertEqual(mocked_database.call_count, 2, "DatabaseOperations was not called right amount of times")
        mocked_database.return_value.__enter__.return_value.mark_as_completed.assert_called_once_with(
            mark_as_completed.mark_as_completed_optionmenu.get()[0]
        )
        mocked_controller.reinitialize_container.assert_called_once_with("habits_frame")


if __name__ == '__main__':
    unittest.main()
