from setuptools import setup

setup(
    name='pytwitch',
    version='1.0.0',
    author='troyev',
    description='Бибилотека для легкой работы с API Twitch',
    packages=['mylibrary'],
    install_requires=[
        'numpy',
        'matplotlib',
        'requests',
        'pytz'
    ],
)
