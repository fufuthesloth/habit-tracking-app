import unittest

from customtkinter import CTkFrame

from habit_tracking_app.frames.exit_page import Exit


class TestExit(unittest.TestCase):

    def test_exit_page_init(self):
        exit_frame = Exit(None, None)
        child_widgets = exit_frame.winfo_children()

        self.assertIsInstance(exit_frame, CTkFrame, "Exit frame is not CTkFrame")
        self.assertEqual(len(child_widgets), 3, "The child widget count is incorrect")


if __name__ == '__main__':
    unittest.main()
