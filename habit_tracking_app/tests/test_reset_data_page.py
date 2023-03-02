import unittest
from unittest.mock import patch

from customtkinter import CTkFrame

from habit_tracking_app.frames.reset_data_page import ResetData


class TestResetData(unittest.TestCase):

    def test_reset_data_page_init(self):
        reset_data_frame = ResetData(None, None)
        child_widgets = reset_data_frame.winfo_children()

        self.assertIsInstance(reset_data_frame, CTkFrame, "Reset data frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 3, "Reset data frame child widgets count is incorrect")

    @patch("habit_tracking_app.frames.reset_data_page.DatabaseOperations")
    @patch("main.App")
    def test_reset_data(self, mocked_controller, mocked_database):
        reset_data_frame = ResetData(None, mocked_controller)
        reset_data_frame.reset_data()

        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.reset_data.assert_called_once()
        mocked_controller.reinitialize_container.assert_called_once_with("settings_frame")


if __name__ == '__main__':
    unittest.main()
