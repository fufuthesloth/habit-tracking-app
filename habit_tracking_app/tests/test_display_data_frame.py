import unittest

from customtkinter import CTkScrollableFrame

from habit_tracking_app.frames.functions.display_data_frame import DisplayData
from habit_tracking_app.frames.functions.habit import Habit


class TestDisplayData(unittest.TestCase):

    def test_display_data_init(self):
        display_frame = DisplayData(None)

        self.assertIsInstance(display_frame, CTkScrollableFrame, "Display frame is not CTkScrollableFrame")

    def test_place_labels_on_frame(self):
        child_widgets = DisplayData(None).winfo_children()

        self.assertEqual(len(child_widgets), 11, "Display frame child widgets count is incorrect")

    def test_place_data_on_frame(self):
        test_data = [Habit(1, "brushing teeth", "daily", "2023-01-16 08:00:00", "2023-01-16", "2023-01-17",
                     "2023-01-16 08:01:00", 0, 0, 0, 0)]
        child_widgets = DisplayData(None, test_data).winfo_children()

        self.assertEqual(len(child_widgets), 22, "Data was not printed successfully on display frame")


if __name__ == '__main__':
    unittest.main()
