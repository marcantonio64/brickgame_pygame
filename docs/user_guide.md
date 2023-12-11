# Project User Guide

Instructions on how to expand the project.

## Adding more games/updating

New game modules should be in `...\brickgame_pygame\games`. 
The general rules for consistency are:

### Import statements
The general game structure is defined at 
`...\brickgame_pygame\games\game_engine.py`.

For each new game, the standard imports are:

```python
import pygame
from pygame.locals import *
from ..constants import *
from ..client import BaseClient
from ..block import Block, BlinkingBlock
from .game_engine import Game
```

You may also import the `random` built-in module, or any of 
your preference.
  
### Class structure
The class containing the new game should implement `Game` and 
be imported into `...\brickgame_pygame\__main__.py`.
The class may follow this template:

```python
class NewGame(Game):
    """
    Implements `Game` with a new game.

    Attributes
    ----------
    on : bool
        Whether any game is active.
    entities : dict
        Containers for the objects to be drawn (name:group).
    ...
    """
    
    ...
    entities  = {"first_entity": [],
                 "second_entity": [],
                 ...
                }
    ...
    
    def __init__(self):
        """ Initialize instance attributes and instantiate game objects. """

        super().__init__()
        
        # Spawn the entities.
        self.first_entity = self.First()
        self.second_entity = self.Second()
        ...
    
    def reset(self):  # Add this if you define extra class variables, like speed
        """ Remove all elements from the screen and start again. """

        # NewGame.newvar1 = ...
        # NewGame.newvar2 = ...
        ...
        super().reset()
    
    def handle_events(self, key, state):
        """
        Set the keybindings.

        Parameters
        ----------
        key : int
            A key id.
        state : int
            ``KEYDOWN`` or ``KEYUP``.
        """

        super().handle_events(key, state)
        
        if state == KEYDOWN:  # Key pressed.
            # if key == ...:
            #     ...
            ...
        if state == KEYUP:  # Key released.
            # if key == ...:
            #     ...
            ...
    
    def manage(self):
        """ Game logic implementation. """
        
        if self.running and not self.paused:
            # List of events.
            ...
        
        super().manage()  # Manage endgame.
    
    def update_score(self):
        """ Scoring mechanics. """
        
        ...
        super().update_score()
    
    def check_victory(self):
        """
        Victory occurs when ...

        Returns
        -------
        bool
            Whether the game has been beaten.
        """
        
        if ...:  # Victory condition.
            return True
        else:
            return False
    
    def check_defeat(self):
        """
        Defeat happens if ...

        Returns
        -------
        bool
            Whether the game was lost.
        """
        
        if ...:  # Defeat condition.
            return True
        else:
            return False
    
    ...  # Rest of the methods.
    
    class FirstEntity:
        """ docstring """
        
        def __init__(self):
            ...
        
        ... # Rest of the methods.
        
    class SecondEntity:
        """ docstring """
        
        def __init__(self):
            ...
          
        ...  # Rest of the methods.
```
  
### Playing/Testing
To run the game/check for errors, you will need to create an
instance of `Client`, for which you can follow this template:

```python
class Client(BaseClient):
    """ A client for :class:`NewGame`. """

    def __init__(self):
        """ Initializing the GUI and the game. """

        super().__init__()
        pygame.display.set_caption("NewGame Game")
        self.game = NewGame()

    def loop(self, t):
        """
        List of scheduled events.

        Parameters
        ----------
        t : int
            A timer.
        """

        # Update `Block`'s mechanics.
        self.game.update_entities(t=t)

        # Implement the game mechanics and check for endgame.
        self.game.manage(t)

        # Draw the game objects to the screen.
        self.game.draw_entities()

    def handle_events(self, key, state):
        """
        Deal with user input.

        Parameters
        ----------
        key : int
            A key id.
        state : int
            `KEYDOWN` or `KEYUP`.
        """

        self.game.handle_events(key, state)
```

After which you can set up the `if __name__ == '__main__'`
statement:

```python
def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
```

### Updates in `...\brickgame_pygame\__main__.py`
Some changes need to be made in order to properly load the game 
when running the full package:
* Import the game into `...\brickgame_pygame\__main__.py` with 
  `from newgame import NewGame`;
* Update the file `...\brickgame_tkinter\high-scores.json` by 
  changing the `Brickgame.__init__()` constructor, adding 
  `"NewGame": 0,` in `json.dumps()` at the `try` statement (around
  line 36).
  Before:
  ```python
  # Create the .json file, if it doesn't already exist.
  try: 
      with open(high_scores_dir, "x") as file:
          json.dump({
              "Snake": 0,
              "Breakout": 0,
              "Asteroids": 0,
              "Tetris": 0,
          }, file)
      print("File `high-scores.json` successfully created at",
            package_dir)
  except Exception as e:
      print(e)
  ```
  After:
  ```python
  # Create the .json file, if it doesn't already exist.
  try: 
      with open(high_scores_dir, "x") as file:
          json.dump({
              "Snake": 0,
              "Breakout": 0,
              "Asteroids": 0,
              "Tetris": 0,
              "NewGame": 0,
          }, file)
      print("File `high-scores.json` successfully created at",
            package_dir)
  except Exception as e:
      print(e)
  ```
* Update the `Brickgame.Selector.__init__()` constructor by 
  adding `n: NewGame(),` to `self.select` (around line 114)
  (`n` is the new number of games).
  
  Before:
  ```python
  self.select = {1: Snake(),
                 2: Breakout(),
                 3: Asteroids(),
                 4: Tetris(),
                }
  ```
  After:
  ```python
  self.select = {1: Snake(),
                 2: Breakout(),
                 3: Asteroids(),
                 4: Tetris(),
                 5: NewGame(),
                 }
  ```
  
### Updates in `...\brickgame_tkinter\screen_generator.py`
The image previews for each game are built and drawn when running 
the game using the `screen_generator.py` module. To create the 
previews for the new game, you will need to add three new nested 
classes in `screen_generator.GamePreview` with this format:
```python
class GamePreview:
    """ Organizes the game preview screens. """
    
    ...
    
    class NewGame1(BaseScreen):
        """ First preview for NewGame. """
        
        def __init__(self) -> None:
            Background()
            super().__init__()
        
        def draw(self, surface):
            """
            Positioning the `Block` objects in a 20x10 grid.

            Parameters
            ----------
            surface : pygame.Surface
                Where to draw.
            """

            sketch = { ... }
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)

    class NewGame2(BaseScreen):
        """ Second preview for NewGame. """
        ...

    class NewGame3(BaseScreen):
        """ Second preview for NewGame. """
        ...
```

An example for `sketch`:

```python
    sketch = { 0: (                            ),
               1: (                            ),
               2: (                            ),
               3: (         3, 4, 5,           ),
               4: (            4,              ),
               5: (                            ),
               6: (                            ),
               7: (                            ),
               8: (                            ),
               9: (                            ),
              10: (0,                          ),
              11: (0,                          ),
              12: (0, 1, 2,          6, 7,     ),
              13: (0, 1, 2, 3,    5, 6, 7, 8, 9),
              14: (                            ),
              15: (         3, 4, 5,           ),
              16: (         3,       6,        ),
              17: (         3,       6,        ),
              18: (         3,       6,        ),
              19: (         3, 4, 5,           )}
```

> Remember to add the next unused letter of the alphabet for identification.