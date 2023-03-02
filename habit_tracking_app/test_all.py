import os
import sys
import unittest


def run():
    os.chdir(os.path.dirname(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(os.getcwd())
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    run()
