from datetime import date, datetime, timedelta
import sqlite3
from typing import cast, List, Tuple, Union

from habit_tracking_app.frames.functions.habit import Habit


class DatabaseOperations:
    def __init__(self):
        self.connection = sqlite3.connect("./database/database.db")
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def create_table(self) -> None:
        """Creates table in database if not exists
        :return: None
        """
        with open("./database/table.sql", "r") as script:
            self.cursor.executescript(script.read())
        self.connection.commit()

    def insert_predefined_habits(self) -> None:
        """Inserts predefined habits into table habits
        :return: None
        """
        with open("./database/predefined_habits.sql", "r") as script:
            self.cursor.executescript(script.read())
        self.connection.commit()

    def list_of_ids(self) -> List[Tuple[int]]:
        """Returns list of tuples with all distinct ids in the table habits
        :return: List[Tuple[int]]
        """
        self.cursor.execute("SELECT DISTINCT(id) FROM habits")
        return self.cursor.fetchall()

    def auto_update(self) -> None:
        """Automaticaly updates ovedue habits
        :return: None
        """
        for id_ in self.list_of_ids():
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
                id_
            )
            habit = Habit(*self.cursor.fetchone())
            habit.start_date = datetime.strptime(cast(str, habit.start_date), "%Y-%m-%d").date()
            habit.due_date = datetime.strptime(cast(str, habit.due_date), "%Y-%m-%d").date()
            habit.completed_timestamp = (
                None if habit.completed_timestamp is None
                else datetime.strptime(cast(str, habit.completed_timestamp), "%Y-%m-%d %H:%M:%S").date()
            )
            while habit.due_date <= date.today():
                if habit.completed_timestamp is None:
                    habit.break_ += 1
                    habit.streak = 0
                    if habit.break_ > habit.max_break:
                        habit.max_break = habit.break_
                else:
                    habit.break_ = 0
                    habit.streak += 1
                    if habit.streak > habit.max_streak:
                        habit.max_streak = habit.streak
                if habit.period == "daily":
                    habit.start_date += timedelta(days=1)
                    habit.due_date += timedelta(days=1)
                else:
                    habit.start_date += timedelta(days=7)
                    habit.due_date += timedelta(days=7)
                habit.completed_timestamp = None
                self.cursor.execute(
                    f"INSERT INTO habits (id, title, period, created_date, start_date, due_date, completed_timestamp, "
                    f"streak, max_streak, break, max_break) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (habit.as_tuple())
                )
                self.connection.commit()

    def max_current_streak(self) -> int:
        """Returns max streak
        :return: int
        """
        current_streaks = []
        for id_ in self.list_of_ids():
            self.cursor.execute("SELECT streak FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            current_streaks.append(self.cursor.fetchone()[0])
        return max(current_streaks) if len(current_streaks) > 0 else 0

    def return_habits_data(self) -> List[Habit]:
        """Returns list with data of all currently tracked habits
        :return: List[Habit]
        """
        habits_list = []
        for id_ in self.list_of_ids():
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
                id_
            )
            habits_list.append(Habit(*self.cursor.fetchone()))
        return habits_list

    def list_of_habits(self) -> List[str]:
        """Returns a list of ids and titles of all habits
        :return: List[str]
        """
        habits_id_titles = []
        for id_ in self.list_of_ids():
            self.cursor.execute("SELECT id, title FROM habits WHERE id = ? ", id_)
            title = self.cursor.fetchone()
            habits_id_titles.append(f"{title[0]} {title[1]}")
        return habits_id_titles if len(habits_id_titles) > 0 else ["You have no habits!"]

    def next_free_id(self) -> int:
        """Checks what is currently the highest id number and returns number one higher
        :return: int
        """
        self.cursor.execute("SELECT MAX(id) FROM habits")
        id_ = self.cursor.fetchone()[0]
        return 1 if id_ is None else (id_ + 1)

    def insert_new_habit(self, title: str, period: str, start_date: str) -> None:
        """Inserts new habit into table habits
        :param title: str
        :param period: str
        :param start_date: str
        :return: None
        """
        id_ = self.next_free_id()
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        due_date = start_date + timedelta(days=1) if period == "daily" else start_date + timedelta(days=7)
        self.cursor.execute(
            "INSERT INTO habits (id, title, period, created_date, start_date, due_date) VALUES (?, ?, ?, ?, ?, ?)",
            (id_, title, period, created_date, start_date, due_date)
        )
        self.connection.commit()

    def update_habit(self, id_: str, new_title: str, new_period: str, new_starting_date: str) -> None:
        """Updates given habit with new title, period and starting date
        :param id_: str
        :param new_title: str
        :param new_period: str
        :param new_starting_date: str
        :return: None
        """
        self.cursor.execute("SELECT entry_no FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
        entry_no = self.cursor.fetchone()
        if entry_no is not None:
            start_date = datetime.strptime(new_starting_date, "%Y-%m-%d").date()
            due_date = start_date + timedelta(days=1) if new_period == "daily" else start_date + timedelta(days=7)
            self.cursor.execute(
                f"UPDATE habits SET title = ?, period = ?, start_date = ?, due_date = ?, completed_timestamp = ? "
                f"WHERE entry_no = ?",
                (new_title, new_period, start_date, due_date, None, entry_no[0])
            )
            self.connection.commit()

    def delete_habit(self, id_: str) -> None:
        """Deletes given habit from table habits
        :param id_: str
        :return: None
        """
        self.cursor.execute("DELETE FROM habits WHERE id = ?", id_)
        self.connection.commit()

    def mark_as_completed(self, id_: str) -> None:
        """Updates completed_timestamp for given habit
        :param id_: str
        :return: None
        """
        self.cursor.execute("SELECT entry_no FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)

        entry_no = self.cursor.fetchone()
        if entry_no is not None:
            self.cursor.execute(
                "UPDATE habits SET completed_timestamp = ? WHERE entry_no = ?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), entry_no[0])
            )
            self.connection.commit()

    def return_daily_habits(self) -> List[Habit]:
        """Returns list with data of all currently tracked daily habits
        :return: List[Habit]
        """
        daily_habits_list = []
        for id_ in self.list_of_ids():
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
                id_
            )
            habit = Habit(*self.cursor.fetchone())
            if (habit.period == 'daily') and (habit is not None):
                daily_habits_list.append(habit)
        return daily_habits_list

    def return_weekly_habits(self) -> List[Habit]:
        """Returns list with data of all currently tracked weekly habits
        :return: List[Habit]
        """
        weekly_habits_list = []
        for id_ in self.list_of_ids():
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
                id_
            )
            habit = Habit(*self.cursor.fetchone())
            if (habit.period == 'weekly') and (habit is not None):
                weekly_habits_list.append(habit)
        return weekly_habits_list

    def return_currently_longest_break(self) -> List[Habit]:
        """Returns list with data of habits with currently the longest break
        :return: List[Habit]
        """
        current_breaks = []
        list_of_ids = self.list_of_ids()
        for id_ in list_of_ids:
            self.cursor.execute("SELECT break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            current_breaks.append(self.cursor.fetchone()[0])
        max_current_break = max(current_breaks) if len(current_breaks) > 0 else 0
        currently_longest_break_list = []
        for id_ in list_of_ids:
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE break = ? AND entry_no = (SELECT entry_no FROM habits "
                f"WHERE id = ? ORDER BY entry_no DESC LIMIT 1)",
                (max_current_break, id_[0])
            )
            habit = self.cursor.fetchone()
            if habit is not None:
                currently_longest_break_list.append(Habit(*habit))
        return currently_longest_break_list

    def return_max_break(self) -> List[Habit]:
        """Returns list with data of habits with the longest max_break
        :return: List[Habit]
        """
        max_breaks = []
        list_of_ids = self.list_of_ids()
        for id_ in list_of_ids:
            self.cursor.execute("SELECT max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            max_breaks.append(self.cursor.fetchone()[0])
        max_break = max(max_breaks) if len(max_breaks) > 0 else 0
        max_break_list = []
        for id_ in list_of_ids:
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE max_break = ? AND entry_no = (SELECT entry_no "
                f"FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1)",
                (max_break, id_[0])
            )
            habit = self.cursor.fetchone()
            if habit is not None:
                max_break_list.append(Habit(*habit))
        return max_break_list

    def return_currently_longest_streak(self) -> List[Habit]:
        """Returns list with data of habits with currently the longest streak
        :return: List[Habit]
        """
        max_current_streak = self.max_current_streak()
        currently_longest_streak_list = []
        for id_ in self.list_of_ids():
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE streak = ? AND entry_no = (SELECT entry_no "
                f"FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1)",
                (max_current_streak, id_[0])
            )
            habit = self.cursor.fetchone()
            if habit is not None:
                currently_longest_streak_list.append(Habit(*habit))
        return currently_longest_streak_list

    def return_max_streak(self) -> List[Habit]:
        """Returns list with data of habits with the longest max_streak
        :return: List[Habit]
        """
        current_max_streaks = []
        list_of_ids = self.list_of_ids()
        for id_ in list_of_ids:
            self.cursor.execute("SELECT max_streak FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            current_max_streaks.append(self.cursor.fetchone()[0])
        max_streak = max(current_max_streaks) if len(current_max_streaks) > 0 else 0
        max_streak_list = []
        for id_ in list_of_ids:
            self.cursor.execute(
                f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
                f"max_streak, break, max_break FROM habits WHERE max_streak = ? AND entry_no = (SELECT entry_no "
                f"FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1)",
                (max_streak, id_[0])
            )
            habit = self.cursor.fetchone()
            if habit is not None:
                max_streak_list.append(Habit(*habit))
        return max_streak_list

    def return_longest_tracked_habit(self) -> List[Habit]:
        """Returns list with data of the longest tracked habit
        :return: List[Habit]
        """
        created_dates = []
        list_of_ids = self.list_of_ids()
        for id_ in list_of_ids:
            self.cursor.execute("SELECT created_date FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            created_dates.append(datetime.strptime(self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S"))
        oldest_date = min(created_dates) if len(created_dates) != 0 else 0
        self.cursor.execute(
            f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
            f"max_streak, break, max_break FROM habits WHERE created_date = ? ORDER BY entry_no DESC LIMIT 1",
            (oldest_date,))
        habit = self.cursor.fetchone()
        if habit is not None:
            habit = [Habit(*habit)]
        return habit

    def return_shortest_tracked_habit(self) -> List[Habit]:
        """Returns list with data of the shortest tracked habit
        :return: List[Habit]
        """
        created_dates = []
        list_of_ids = self.list_of_ids()
        for id_ in list_of_ids:
            self.cursor.execute("SELECT created_date FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1", id_)
            created_dates.append(datetime.strptime(self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S"))
        youngest_date = max(created_dates) if len(created_dates) > 0 else 0
        self.cursor.execute(
            f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
            f"max_streak, break, max_break FROM habits WHERE created_date = ? ORDER BY entry_no DESC LIMIT 1",
            (youngest_date,))
        habit = self.cursor.fetchone()
        if habit is not None:
            habit = [Habit(*habit)]
        return habit

    def display_history(self, id_: str) -> List[Habit]:
        """Returns historical data about given habits
        :param id_: str
        :return: List[Habit]
        """
        self.cursor.execute(
            f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
            f"max_streak, break, max_break FROM habits WHERE id = ?",
            id_
        )
        history = []
        for entry in self.cursor.fetchall():
            history.append(Habit(*entry))
        return history

    def display_habit_information(self, id_: str) -> Union[List[Habit], None]:
        """Returns data for a given habit
        :param id_: str
        :return: Union[List[Habit], None]
        """
        self.cursor.execute(
            f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
            f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
            id_
        )
        habit_information = self.cursor.fetchone()
        return None if habit_information is None else [Habit(*habit_information)]

    def display_max_streak(self, id_: str) -> Union[List[Habit], None]:
        """Returns max_streak for given habit
        :param id_: str
        :return: Union[List[Habit], None]
        """
        self.cursor.execute(
            f"SELECT id, title, period, created_date, start_date, due_date, completed_timestamp, streak, "
            f"max_streak, break, max_break FROM habits WHERE id = ? ORDER BY entry_no DESC LIMIT 1",
            id_
        )
        max_streak = self.cursor.fetchone()
        return None if max_streak is None else [Habit(*max_streak)]

    def reset_data(self) -> None:
        """Deletes all data from table habits
        :return: None
        """
        self.cursor.execute("DELETE FROM habits")
        self.connection.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
