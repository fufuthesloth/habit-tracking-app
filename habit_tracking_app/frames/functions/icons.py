from typing import Union

from customtkinter import CTkImage
from PIL import Image


def load_icon(icon_name: str) -> Union[CTkImage, None]:
    """Loads icons and resizes them. If fails, returns nothing
    :param icon_name: str
    :return: Union[CTkImage, None]
    """
    try:
        return CTkImage(
            light_image=Image.open(f"./icons/{icon_name}_light_mode.png"),
            dark_image=Image.open(f"./icons/{icon_name}_dark_mode.png"),
            size=(25, 25),
        )
    except FileNotFoundError:
        return None
