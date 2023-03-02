import unittest
from unittest.mock import patch, MagicMock, call

from customtkinter import CTk, CTkFrame

from habit_tracking_app.main import App


class TestApp(unittest.TestCase):

    @patch("habit_tracking_app.main.App.container_init")
    def test_app_init(self, mocked_container):
        app = App()
        mocked_container.side_effect = CTkFrame(app)
        child_widgets = app.winfo_children()

        self.assertIsInstance(app, CTk, "App window is not CTk")
        self.assertEqual(len(child_widgets), 1, "App window child widgets count is incorrect")
        mocked_container.assert_called_once()

    @patch("habit_tracking_app.main.Exit")
    @patch("habit_tracking_app.main.ResetData")
    @patch("habit_tracking_app.main.Analytics")
    @patch("habit_tracking_app.main.MarkAsCompleted")
    @patch("habit_tracking_app.main.DeleteHabit")
    @patch("habit_tracking_app.main.EditHabit")
    @patch("habit_tracking_app.main.AddNewHabit")
    @patch("habit_tracking_app.main.Habits")
    @patch("habit_tracking_app.main.Home")
    @patch("habit_tracking_app.main.Settings")
    @patch("habit_tracking_app.main.Menu")
    @patch("habit_tracking_app.main.App.display_frame")
    def test_container_init(self, mocked_display, mocked_menu, mocked_settings, mocked_home, mocked_habits,
                            mocked_addnewhabit, mocked_edithabit, mocked_deletehabit, mocked_markascompleted,
                            mocked_analytics, mocked_resetdata, mocked_exit):
        app = App()

        self.assertIsInstance(app.container, CTkFrame, "Container is not CTkFrame")
        mocked_menu.assert_called_once_with(app.container, app)
        mocked_settings.assert_called_once_with(app.container, app)
        mocked_home.assert_called_once_with(app.container)
        mocked_habits.assert_called_once_with(app.container, app)
        mocked_addnewhabit.assert_called_once_with(app.container, app)
        mocked_edithabit.assert_called_once_with(app.container, app)
        mocked_deletehabit.assert_called_once_with(app.container, app)
        mocked_markascompleted.assert_called_once_with(app.container, app)
        mocked_analytics.assert_called_once_with(app.container)
        mocked_resetdata.assert_called_once_with(app.container, app)
        mocked_exit.assert_called_once_with(app.container, app)
        mocked_display.assert_called_once_with("home_frame")

    @patch("habit_tracking_app.main.Home")
    @patch("habit_tracking_app.main.App.container_init")
    def test_display_frame(self, mocked_container, mocked_home):
        app = App()
        app.frames = {"home_frame": mocked_home}
        app.display_frame("home_frame")

        app.frames["home_frame"].tkraise.assert_called_once()

    @patch("habit_tracking_app.main.App.container_init")
    def test_reintialize_container(self, mocked_container):
        app = App()
        app.container = MagicMock()
        app.reinitialize_container("home_frame")
        calls = [call(), call("home_frame")]

        app.container.destroy.assert_called_once()
        self.assertEqual(mocked_container.call_count, 2, "Container_init was not called right amount of times")
        mocked_container.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
