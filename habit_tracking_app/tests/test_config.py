import unittest
from unittest.mock import patch, mock_open

from habit_tracking_app.frames.functions.config import Config


class TestConfig(unittest.TestCase):

    @patch("json.load", return_value={"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "False"})
    @patch("builtins.open", new_callable=mock_open())
    def test_successfull_config_init(self, mocked_open, mocked_json):
        control_config = {"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "False"}
        test_config = Config().config

        mocked_open.assert_called_once_with("./database/config.json", "r")
        mocked_json.assert_called_once_with(mocked_open.return_value.__enter__.return_value)
        self.assertEqual(test_config, control_config, "Failed to read the config from file")
        self.assertIsInstance(test_config, dict, "Config is not a dictionary")

    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open(), return_value=FileNotFoundError)
    def test_FileNotFoundError_config_init(self, mocked_open, mocked_json):
        control_config = {"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "True"}
        test_config = Config().config

        mocked_open.assert_called_once_with("./database/config.json", "r")
        mocked_json.assert_called_once_with(mocked_open.return_value.__enter__.return_value)
        self.assertRaises(FileNotFoundError)
        self.assertEqual(test_config, control_config, "Failed to set default values")
        self.assertIsInstance(test_config, dict, "Config is not a dictionary")

    @patch("json.load", return_value={"appearance_mode": "NotExistingValue"})
    @patch("builtins.open", new_callable=mock_open())
    def test_KeyError_config_init(self, mocked_open, mocked_json):
        control_config = {"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "True"}
        test_config = Config().config

        mocked_open.assert_called_once_with("./database/config.json", "r")
        mocked_json.assert_called_once_with(mocked_open.return_value.__enter__.return_value)
        self.assertRaises(KeyError)
        self.assertEqual(test_config, control_config, "Failed to set default values")
        self.assertIsInstance(test_config, dict, "Config is not a dictionary")

    @patch("json.load", return_value={"NotExistingKey": "Dark"})
    @patch("builtins.open", new_callable=mock_open())
    def test_ValueError_config_init(self, mocked_open, mocked_json):
        control_config = {"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "True"}
        test_config = Config().config

        mocked_open.assert_called_once_with("./database/config.json", "r")
        mocked_json.assert_called_once_with(mocked_open.return_value.__enter__.return_value)
        self.assertRaises(ValueError)
        self.assertEqual(test_config, control_config, "Failed to set default values")
        self.assertIsInstance(test_config, dict, "Config is not a dictionary")

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open())
    def test_save_new_config(self, mocked_open, mocked_json):
        appearance_mode = "Dark"
        color_theme = "blue"
        Config.save_new_config(appearance_mode, color_theme)
        control_config = {"appearance_mode": appearance_mode, "color_theme": color_theme, "initial_opening": "False"}

        mocked_open.assert_called_once_with("./database/config.json", "w")
        mocked_json.assert_called_once_with(control_config, mocked_open.return_value.__enter__.return_value, indent=2)


if __name__ == '__main__':
    unittest.main()
