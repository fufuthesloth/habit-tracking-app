import json
from typing import Dict


class Config:
    def __init__(self):
        """Initializes config from file
        """
        try:
            with open("./database/config.json", "r") as config_file:
                self.config = json.load(config_file)
                if (
                    (self.config["appearance_mode"] not in ("Dark", "Light"))
                    or (self.config["color_theme"] not in ("blue", "green"))
                    or (self.config["initial_opening"] not in ("True", "False"))
                ):
                    raise ValueError
        except (FileNotFoundError, KeyError, ValueError):
            self.config = {"appearance_mode": "Dark", "color_theme": "blue", "initial_opening": "True"}

    def __getattr__(self, name: str) -> Dict[str, str]:
        """Returns given attribute
        :param name: str
        :return: Dict[str, str]
        """
        return self.config

    @staticmethod
    def save_new_config(appearance_mode: str, color_theme: str) -> None:
        """Saves new config to file
        :param appearance_mode: str
        :param color_theme: str
        :return: None
        """
        config = {"appearance_mode": appearance_mode, "color_theme": color_theme, "initial_opening": "False"}
        with open("./database/config.json", "w") as config_file:
            json.dump(config, config_file, indent=2)



