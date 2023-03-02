import unittest

from habit_tracking_app.frames.functions.habit import Habit


class TestHabit(unittest.TestCase):

    def test_habit_init(self):
        habit = Habit(1, "brushing teeth", "daily", "2023-01-16 08:00:00", "2023-01-16", "2023-01-17",
                      "2023-01-16 08:01:00", 0, 0, 0, 0)

        self.assertIsInstance(habit, Habit)

    def test_return_astuple(self):
        habit = Habit(1, "brushing teeth", "daily", "2023-01-16 08:00:00", "2023-01-16", "2023-01-17",
                      "2023-01-16 08:01:00", 0, 0, 0, 0)

        self.assertEqual(habit.as_tuple(), (1, "brushing teeth", "daily", "2023-01-16 08:00:00", "2023-01-16",
                                            "2023-01-17", "2023-01-16 08:01:00", 0, 0, 0, 0))


if __name__ == '__main__':
    unittest.main()
