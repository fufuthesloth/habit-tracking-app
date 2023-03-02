import unittest
from unittest.mock import patch, call

from customtkinter import CTkFrame

from habit_tracking_app.frames.settings_page import Settings


class TestSettings(unittest.TestCase):

    @patch("habit_tracking_app.frames.settings_page.Config")
    def test_settings_page_init(self, mocked_config):
        mocked_config.return_value.config = {"appearance_mode": "Dark", "color_theme": "blue",
                                             "initial_opening": "False"}
        settings_frame = Settings(None, None)
        child_widgets = settings_frame.winfo_children()

        self.assertIsInstance(settings_frame, CTkFrame, "Settings frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 5, "Settings frame child widgets count is incorrect")

    @patch("habit_tracking_app.frames.settings_page.DatabaseOperations")
    @patch("habit_tracking_app.frames.settings_page.customtkinter")
    @patch("habit_tracking_app.frames.settings_page.Config")
    def test_load_config_with_initial_opening_true(self, mocked_config, mocked_gui, mocked_database):
        mocked_config.return_value.config = {"appearance_mode": "Dark", "color_theme": "blue",
                                             "initial_opening": "True"}
        Settings(None, None)
        mocked_gui.set_appearance_mode.assert_called_once_with("Dark")
        mocked_gui.set_default_color_theme.assert_called_once_with("blue")
        calls = [call(value='Dark'), call(value='blue')]

        mocked_gui.StringVar.assert_has_calls(calls)
        self.assertEqual(mocked_gui.StringVar.call_count, 2, "StringVar was not called right amount of times")
        mocked_database.assert_called_once()
        mocked_database.return_value.__enter__.return_value.create_table.assert_called_once()
        mocked_database.return_value.__enter__.return_value.insert_predefined_habits.assert_called_once()
        mocked_config.save_new_config.assert_called_once_with("Dark", "blue")

    @patch("habit_tracking_app.frames.settings_page.DatabaseOperations")
    @patch("habit_tracking_app.frames.settings_page.customtkinter")
    @patch("habit_tracking_app.frames.settings_page.Config")
    def test_load_config_with_initial_opening_false(self, mocked_config, mocked_gui, mocked_database):
        mocked_config.return_value.config = {"appearance_mode": "Dark", "color_theme": "blue",
                                             "initial_opening": "False"}
        Settings(None, None)
        mocked_gui.set_appearance_mode.assert_called_once_with("Dark")
        mocked_gui.set_default_color_theme.assert_called_once_with("blue")
        calls = [call(value='Dark'), call(value='blue')]

        mocked_gui.StringVar.assert_has_calls(calls)
        self.assertEqual(mocked_gui.StringVar.call_count, 2, "StringVar was not called right amount of times")
        mocked_database.assert_not_called()

    @patch("habit_tracking_app.frames.settings_page.customtkinter")
    @patch("habit_tracking_app.frames.settings_page.Config")
    def test_change_appearance_mode(self, mocked_config, mocked_gui):
        mocked_config.return_value.config = {"appearance_mode": "Dark", "color_theme": "blue",
                                             "initial_opening": "False"}
        settings_frame = Settings(None, None)
        settings_frame.change_appearance_mode("Light")

        mocked_gui.set_appearance_mode.assert_called_with("Light")
        mocked_config.save_new_config.assert_called_once_with("Light", settings_frame.color_theme_optionmenu.get())

    @patch("habit_tracking_app.frames.settings_page.Config")
    @patch("main.App")
    def test_change_color_theme(self, mocked_controller, mocked_config):
        mocked_config.return_value.config = {"appearance_mode": "Dark", "color_theme": "blue",
                                             "initial_opening": "False"}
        settings_frame = Settings(None, mocked_controller)
        settings_frame.change_color_theme("green")

        mocked_config.save_new_config.assert_called_once_with(settings_frame.appearance_mode_optionmenu.get(), "green")
        mocked_controller.reinitialize_container.assert_called_once_with("settings_frame")


if __name__ == '__main__':
    unittest.main()
