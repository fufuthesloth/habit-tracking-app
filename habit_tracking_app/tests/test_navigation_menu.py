import unittest
from unittest.mock import patch, call, MagicMock

from customtkinter import CTkFrame, CTkButton

from habit_tracking_app.frames.navigation_menu import Menu


class TestMenu(unittest.TestCase):

    @patch("habit_tracking_app.frames.navigation_menu.load_icon", return_value=None)
    def test_navigation_menu_frame_init(self, mocked_icons):
        menu_frame = Menu(None, None)
        child_widgets = menu_frame.winfo_children()
        calls = [call("home"), call("habits"), call("analytics"), call("settings"), call("exit")]

        self.assertIsInstance(menu_frame, CTkFrame, "Navigation menu frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 6, "Navigation menu frame child widgets count is incorrect")
        self.assertEqual(mocked_icons.call_count, 5, "load_icon was not called right amount of time")
        mocked_icons.assert_has_calls(calls)

    @patch("habit_tracking_app.frames.navigation_menu.Menu.add_menu_button", return_value=MagicMock(spec=CTkButton))
    @patch("habit_tracking_app.frames.navigation_menu.load_icon")
    def test_add_menu_button(self, mocked_icons, mocked_button):
        Menu(None, None)
        calls = [call("Home", mocked_icons.return_value, "home_frame"),
                 call("Habits", mocked_icons.return_value, "habits_frame"),
                 call("Analytics", mocked_icons.return_value, "analytics_frame"),
                 call("Settings", mocked_icons.return_value, "settings_frame"),
                 call("Exit", mocked_icons.return_value, "exit_frame")]

        self.assertIsInstance(mocked_button.return_value, CTkButton, "Menu button is not CTkButton")
        self.assertEqual(mocked_button.call_count, 5, "add_menu_button was not called right amount of time")
        mocked_button.assert_has_calls(calls)

    @patch("main.App")
    def test_change_frame(self, mocked_controller):
        menu_frame = Menu(None, mocked_controller)
        menu_frame.change_frame("home_frame")

        self.assertEqual(menu_frame.home_page_button.cget("fg_color"), ("gray75", "gray25"),
                         "Home button foreground color is incorrect")
        self.assertEqual(menu_frame.habits_page_button.cget("fg_color"), "transparent",
                         "Habits button foreground color is incorrect")
        self.assertEqual(menu_frame.analytics_page_button.cget("fg_color"), "transparent",
                         "Analytics button foreground color is incorrect")
        self.assertEqual(menu_frame.settings_page_button.cget("fg_color"), "transparent",
                         "Settings button foreground color is incorrect")
        self.assertEqual(menu_frame.exit_page_button.cget("fg_color"), "transparent",
                         "Exit button foreground color is incorrect")
        mocked_controller.display_frame.assert_called_once_with("home_frame")


if __name__ == '__main__':
    unittest.main()
