from datetime import date, datetime, timedelta
import sqlite3
import unittest
from unittest.mock import patch

from habit_tracking_app.frames.functions.database import DatabaseOperations
from habit_tracking_app.frames.functions.habit import Habit


@patch("habit_tracking_app.frames.functions.database.sqlite3.connect")
class TestDatabaseOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()

        with open("./database/table.sql", "r") as script:
            self.cursor.executescript(script.read())
        self.connection.commit()

        with open("./database/predefined_habits.sql", "r") as script:
            self.cursor.executescript(script.read())
        self.connection.commit()

    def tearDown(self) -> None:
        self.connection.close()

    def test_database_operations_init(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()

        mocked_connect.assert_called_once_with("./database/database.db")
        self.assertIsInstance(dbo.connection, sqlite3.Connection, "Connection type is incorrect")
        self.assertIsInstance(dbo.cursor, sqlite3.Cursor, "Cursor type is incorrect")

    def test_create_table(self, mocked_connect):
        self.cursor.execute("DROP TABLE habits")   # Drop table created in setUp
        self.connection.commit()

        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.create_table()

        table = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'").fetchone()

        self.assertIsNotNone(table, "Failed to create table habits")

    def test_insert_predefined_habits(self, mocked_connect):
        self.cursor.execute("DELETE FROM habits")   # Delete predefined habits inserted in setUp
        self.connection.commit()

        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.insert_predefined_habits()

        count = self.cursor.execute("SELECT count(*) FROM habits").fetchone()[0]

        self.assertGreater(count, 0, "Failed to insert predefined habits")

    def test_list_of_ids(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.list_of_ids()

        self.assertEqual(result, [(1,), (2,), (3,), (4,), (5,)], "Result of list of ids is incorrect")

    def test_auto_update(self, mocked_connect):
        self.cursor.execute("DELETE FROM habits")  # Delete predefined habits inserted in setUp
        self.connection.commit()
        self.cursor.execute(
            f"INSERT INTO habits (id, title, period, created_date, start_date, due_date) VALUES (6, 'test title', "
            f"'daily', '2023-02-23 12:02:30', '2023-02-23', '2023-02-24')")  # Insert test habit to test auto update
        self.connection.commit()

        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.auto_update()

        delta = (date.today() - datetime.strptime('2023-02-23', "%Y-%m-%d").date()).days
        result = self.cursor.execute("SELECT * FROM habits WHERE id='6' ORDER BY entry_no DESC LIMIT 1").fetchone()
        test_result = ((delta + 1), 6, 'test title', 'daily', '2023-02-23 12:02:30', date.today().strftime("%Y-%m-%d"),
                       (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"), None, 0, 0, delta, delta)

        self.assertEqual(result, test_result, "Result of auto update is incorrect")

    def test_max_current_streak(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.max_current_streak()

        self.assertEqual(result, 9, "Result of max current streak is incorrect")

    def test_return_habits_data(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_habits_data()

        self.assertEqual(len(result), 5, "Result of return habits data is incorrect")

    def test_list_of_habits(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.list_of_habits()
        test_result = ['1 brushing teeth', '2 no caffeine', '3 study python', '4 go to gym', '5 go to therapy']

        self.assertEqual(result, test_result, "Result of list of habits is incorrect")

    def test_next_free_id(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.next_free_id()

        self.assertEqual(result, 6, "Result of next free id is incorrect")

    def test_insert_new_habit(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.insert_new_habit("test habit", "daily", "2023-02-24")
        result = self.cursor.execute("SELECT * FROM habits WHERE title='test habit'").fetchone()
        test_result = (135, 6, 'test habit', 'daily', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '2023-02-24',
                       '2023-02-25', None, 0, 0, 0, 0)

        self.assertEqual(result, test_result, "Result of insert new habit is incorrect")

    def test_update_habit(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.update_habit("4", "workout", "daily", "2023-02-24")
        result = self.cursor.execute("SELECT * FROM habits WHERE id='4' ORDER BY entry_no DESC LIMIT 1").fetchone()
        test_result = (133, 4, 'workout', 'daily', '2023-01-17 10:00:00', '2023-02-24', '2023-02-25', None, 0, 3, 2, 2)

        self.assertEqual(result, test_result, "Result of update habit is incorrect")

    def test_delete_habit(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.delete_habit("3")
        result = self.cursor.execute("SELECT count(*) FROM habits WHERE id='3'").fetchone()[0]

        self.assertEqual(result, 0, "Result of delete habit is incorrect")

    def test_mark_as_completed(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.mark_as_completed("1")

        result = self.cursor.execute(
            "SELECT completed_timestamp FROM habits WHERE id='1' ORDER BY entry_no DESC LIMIT 1").fetchone()[0]

        self.assertEqual(result, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "Result of mark as completed is incorrect")

    def test_return_daily_habits(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_daily_habits()

        self.assertEqual(len(result), 3, "Result of return daily habits is incorrect")

    def test_return_weekly_habits(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_weekly_habits()

        self.assertEqual(len(result), 2, "Result of return weekly habits is incorrect")

    def test_return_currently_longest_break(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_currently_longest_break()
        test_result = [Habit(id_=4, title='go to gym', period='weekly', created_date='2023-01-17 10:00:00',
                             start_date='2023-02-21', due_date='2023-02-28', completed_timestamp=None, streak=0,
                             max_streak=3, break_=2, max_break=2)]

        self.assertEqual(result, test_result, "Result of return currently longest break is incorrect")

    def test_return_max_break(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_max_break()
        test_result = [Habit(id_=3, title='study python', period='daily', created_date='2023-01-16 12:00:00',
                             start_date='2023-02-24', due_date='2023-02-25', completed_timestamp='2023-02-24 21:01:00',
                             streak=3, max_streak=21, break_=0, max_break=10)]

        self.assertEqual(result, test_result, "Result of return max break is incorrect")

    def test_return_currently_longest_streak(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_currently_longest_streak()
        test_result = [Habit(id_=2, title='no caffeine', period='daily', created_date='2023-01-16 10:00:00',
                             start_date='2023-02-24', due_date='2023-02-25', completed_timestamp='2023-02-24 21:34:00',
                             streak=9, max_streak=10, break_=0, max_break=5)]

        self.assertEqual(result, test_result, "Result of return currently longest streak is incorrect")

    def test_return_max_streak(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_max_streak()
        test_result = [Habit(id_=1, title='brushing teeth', period='daily', created_date='2023-01-16 08:00:00',
                             start_date='2023-02-24', due_date='2023-02-25', completed_timestamp='2023-02-24 09:01:00',
                             streak=4, max_streak=32, break_=0, max_break=3)]

        self.assertEqual(result, test_result, "Result of return max streak is incorrect")

    def test_return_longest_tracked_habit(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_longest_tracked_habit()
        test_result = [Habit(id_=1, title='brushing teeth', period='daily', created_date='2023-01-16 08:00:00',
                             start_date='2023-02-24', due_date='2023-02-25', completed_timestamp='2023-02-24 09:01:00',
                             streak=4, max_streak=32, break_=0, max_break=3)]

        self.assertEqual(result, test_result, "Result of return longest tracked habit is incorrect")

    def test_return_shortest_tracked_habit(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.return_shortest_tracked_habit()
        test_result = [Habit(id_=5, title='go to therapy', period='weekly', created_date='2023-01-17 12:00:00',
                             start_date='2023-02-21', due_date='2023-02-28', completed_timestamp=None, streak=5,
                             max_streak=5, break_=0, max_break=0)]

        self.assertEqual(result, test_result, "Result of return shortest tracked habit is incorrect")

    def test_display_history(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.display_history("1")

        self.assertEqual(len(result), 40, "Result of display history is incorrect")

    def test_display_habit_information(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.display_habit_information("1")
        test_result = (1, 'brushing teeth', 'daily', '2023-01-16 08:00:00', '2023-02-24', '2023-02-25',
                       '2023-02-24 09:01:00', 4, 32, 0, 3)

        self.assertEqual(result[0].as_tuple(), test_result, "Result of display habit information is incorrect")

    def test_display_max_streak(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        result = dbo.display_max_streak("1")
        test_result = (1, 'brushing teeth', 'daily', '2023-01-16 08:00:00', '2023-02-24', '2023-02-25',
                       '2023-02-24 09:01:00', 4, 32, 0, 3)

        self.assertEqual(result[0].as_tuple(), test_result, "Result of display max streak is incorrect")

    def test_reset_data(self, mocked_connect):
        mocked_connect.return_value = self.connection
        dbo = DatabaseOperations()
        dbo.reset_data()

        count = self.cursor.execute("SELECT count(*) FROM habits").fetchone()[0]

        self.assertEqual(count, 0, "Failed to reset data")


if __name__ == '__main__':
    unittest.main()
