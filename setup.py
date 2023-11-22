from setuptools import setup, find_packages

setup(
    name="Brick Game with pygame",
    version="1.1",
    packages=find_packages(),
    author="marcantonio64",
    author_email="mafigueiredo08@gmail.com",
    description="An exercise project with GUIs using pygame",
    url="https://github.com/marcantonio64/brickgame_pygame",
    install_requires=[
        'pygame>=2.0.1',
        'python_version >= "3.6.8"',
    ],
)
