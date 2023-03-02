import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.home_page import Home


class TestHome(unittest.TestCase):

    @patch("habit_tracking_app.frames.home_page.DatabaseOperations")
    def test_add_new_habit_page_init(self, mocked_database):
        home_frame = Home(None)
        child_widgets = home_frame.winfo_children()
        self.assertIsInstance(home_frame, CTkFrame, "Home frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 3, "Home page child widgets count is incorrect")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.auto_update.assert_called_once()
        mocked_database.return_value.__enter__.return_value.list_of_ids.assert_called_once()
        mocked_database.return_value.__enter__.return_value.max_current_streak.assert_called_once()


if __name__ == '__main__':
    unittest.main()
