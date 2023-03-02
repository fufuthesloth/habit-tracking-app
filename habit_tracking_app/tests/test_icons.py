import unittest
from unittest.mock import patch, call, MagicMock

from PIL import Image
from customtkinter import CTkImage

from habit_tracking_app.frames.functions.icons import load_icon


class TestIcons(unittest.TestCase):

    @patch("habit_tracking_app.frames.functions.icons.Image")
    def test_successfully_load_icon(self, mocked_icons):
        mocked_icons.open.return_value = MagicMock(spec=Image.Image)
        icon_name = "home"
        icon = load_icon(icon_name)
        calls = (call(f"./icons/{icon_name}_light_mode.png"), call(f"./icons/{icon_name}_dark_mode.png"))

        self.assertIsInstance(icon, CTkImage, "Icon is not CTkImage")
        self.assertEqual(mocked_icons.open.call_count, 2, "Image.open was not called right amount of time")
        mocked_icons.open.assert_has_calls(calls)
        self.assertEqual(icon.cget("size"), (25, 25), "Incorrect size of the icon")

    def test_failed_load_icon(self):
        icon = load_icon("invalid_name")
        none_type = type(None)

        self.assertIsInstance(icon, none_type, "Icon is not None")
        self.assertRaises(FileNotFoundError)


if __name__ == '__main__':
    unittest.main()
