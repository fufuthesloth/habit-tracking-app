from dataclasses import astuple, dataclass
from datetime import date
from typing import Union


@dataclass
class Habit:
    id_: int
    title: str
    period: str
    created_date: str
    start_date: Union[str, date]
    due_date: Union[str, date]
    completed_timestamp: Union[str, date, None]
    streak: int
    max_streak: int
    break_: int
    max_break: int

    def as_tuple(self):
        return astuple(self)
