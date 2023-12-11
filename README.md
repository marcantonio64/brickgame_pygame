# Brick Game with [pygame](https://www.pygame.org/)

## Overview
An exercise project for GUIs using tools from the [**Python3**](https://www.python.org/)
library [**pygame**](https://www.pygame.org/).
The goal is to make a client with some simple games: snake, breakout,
asteroids, and tetris.

The aspect is of a 20x10 grid of `Block` objects, which are used
as pixels for the construction of each game.

> A `Block` is built as a `Sprite` to a `Surface` object as an outer
empty square containing a smaller filled square.

A manual with the rules and controls of each game can be found on
`...\brickgame_pygame\docs\game_manuals.md`. Instructions for adding more games can
be seen on `...\brickgame_pygame\docs\user_guide.md`.

## Installation
In the command line, after setting up your directory, download the project with:

```shell
git clone https://github.com/marcantonio64/brickgame_pygame.git
python setup.py install
```

Then run the game package with:

```shell
python -m brickgame_pygame
```

If you want to play a specific game directly, simply add `.games.` and
the name of the game, for example:

```shell
python -m brickgame_pygame.games.tetris
```

## Inspirations
Gustavo Barbieri's pygame tutorial: [Introduction to Game Development using PyGame](https://old.gustavobarbieri.com.br/jogos/jogo/doc/).

## Metadata
Author: marcantonio64

Contact: mafigueiredo08@gmail.com

Date: 11-Nov-2023

License: MIT

Python: v3.6+