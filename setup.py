from io import open
from setuptools import setup, find_packages

setup(
    name='habit-tracking-app',
    version='0.0.4',
    url='https://github.com/fufuthesloth/habit-tracking-app/',
    license='Unlicense',
    author='Krzysztof Szczypkowski',
    author_email='krzysztof.szczypkowski@o2.pl',
    description='Habit tracking application',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['habit tracking', 'gui', 'executable'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['customtkinter >= 5.1.2', 'tkcalendar >= 1.6.1', 'Pillow >= 9.4.0'],
    python_requires='>=3.10',
    classifiers=[
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points={
        'console_scripts': [
            'habit-tracking-app=habit_tracking_app.main:run',
            'habit-tracking-app-tests=habit_tracking_app.test_all:run'
        ],
    },
)
