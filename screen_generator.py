"""
This module contains classes used to create the following screens:

* background
* victory screen
* defeat screen
* high_scores
* game previews

All screens constructed and drawn at runtime as `pygame.Surface`
objects, and must be instantiated to be shown.

Except for `high_scores`, each of the screens is made of an arrangement
of dark `Block`s on top of a 20x10 grid of lighter `Block`s.
"""

import json
import pygame
from abc import ABC, abstractmethod
from .constants import *
from .client import high_scores_dir
from .block import Block

__all__ = ["Background",
           "VictoryScreen",
           "DefeatScreen",
           "GamePreview",
           "show_high_scores",
           ]


class BaseScreen(ABC):
    """ Abstract class with a general constructor for drawing the screens. """

    def __init__(self):
        """ Access the current active `pygame.Surface` and draw to it. """

        # Initialize the `Group` to update and draw the `Block` sprites.
        self.render = pygame.sprite.RenderPlain()
        
        # Access the current active `Surface` and draw in it.
        screen = pygame.display.get_surface()
        self.draw(screen)
    
    @abstractmethod
    def draw(self, surface):
        """
        Positioning the `Block` objects in a 20x10 grid.

        Parameters
        ----------
        surface : pygame.Surface
            Where to draw.
        """

        pass


class Background(BaseScreen):
    """ A 20x10 grid of `Block` sprites colored ``SHADE_COLOR``. """

    def draw(self, surface):
        """
        Positioning the `Block` objects in a 20x10 grid.

        Parameters
        ----------
        surface : pygame.Surface
            Where to draw.
        """

        surface.fill(BACK_COLOR)
        
        # Border
        border = pygame.Rect(0, 0, *RES)
        pygame.draw.rect(surface,
                         LINE_COLOR,
                         border,
                         BORDER_WIDTH,
                         )
        
        # Grid
        for i in range(10):
            for j in range(20):
                Block(i, j, color=SHADE_COLOR).add(self.render)
        
        self.render.draw(surface)


class VictoryScreen(BaseScreen):
    """ A *You Win* message. """
    
    def __init__(self):
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
        
        sketch = { 1: (0,    2,       5,          9),
                   2: (0,    2,       5,          9),
                   3: (0, 1, 2,       5,    7,    9),
                   4: (      2,       5, 6, 7, 8, 9),
                   5: (0, 1, 2,       5, 6,    8, 9),
                   
                   7: (0, 1, 2,          6, 7, 8   ),
                   8: (0,    2,             7      ),
                   9: (0,    2,             7      ),
                  10: (0, 1, 2,          6, 7, 8   ),
                  
                  12: (0,    2,       5, 6,       9),
                  13: (0,    2,       5, 6, 7,    9),
                  14: (0,    2,       5,    7, 8, 9),
                  15: (0, 1, 2,       5,       8, 9)}

        for j in sketch.keys():
            for i in sketch[j]:
                Block(i, j).add(self.render)
        
        self.render.draw(surface)


class DefeatScreen(BaseScreen):
    """ A *Game Over* message. """
    
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

        sketch = {0: (   1, 2, 3, 4,       7, 8, 9),
                  1: (0,                   7,    9),
                  2: (0,    2, 3, 4,       7,    9),
                  3: (0,          4,       7, 8, 9),
                  4: (   1, 2, 3                  ),          
                  5: (                     7,    9),
                  6: (   1, 2, 3,          7,    9),
                  7: (0,          4,       7,    9),
                  8: (0, 1, 2, 3, 4,          8   ),  
                  9: (0,          4               ),          
                 10: (                     7, 8, 9),
                 11: (0,          4,       7      ),    
                 12: (0, 1,    3, 4,       7, 8, 9),
                 13: (0,    2,    4,       7      ),    
                 14: (                     7, 8, 9),
                 15: (   1, 2, 3                  ),            
                 16: (   1,                7, 8   ),  
                 17: (   1, 2, 3,          7,    9),
                 18: (   1,                7, 8   ),  
                 19: (   1, 2, 3,          7,    9)}

        for j in sketch.keys():
            for i in sketch[j]:
                Block(i, j).add(self.render)
        
        self.render.draw(surface)


class GamePreview:
    """ Organizes the game preview screens. """

    class Snake1(BaseScreen):
        """ First preview for Snake. """
        
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

            sketch = { 0: (                            ),
                       1: (                            ),
                       2: (                            ),
                       3: (      2, 3, 4, 5, 6, 7,     ),
                       4: (                            ),
                       5: (                            ),
                       6: (                            ),
                       7: (                     7,     ),
                       8: (                            ),
                       9: (                            ),
                      10: (                            ),
                      11: (                            ),
                      12: (                            ),
                      13: (                            ),
                      14: (                            ),
                      15: (            4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5, 6,        ),
                      18: (         3,       6,        ),
                      19: (         3,       6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)

    class Snake2(BaseScreen):
        """ Second preview for Snake. """
        
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
            
            sketch = { 0: (                            ),
                       1: (                            ),
                       2: (                            ),
                       3: (         3, 4, 5, 6, 7,     ),
                       4: (                     7,     ),
                       5: (                            ),
                       6: (                            ),
                       7: (                     7,     ),
                       8: (                            ),
                       9: (                            ),
                      10: (                            ),
                      11: (                            ),
                      12: (                            ),
                      13: (                            ),
                      14: (                            ),
                      15: (            4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5, 6,        ),
                      18: (         3,       6,        ),
                      19: (         3,       6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Snake3(BaseScreen):
        """ Third preview for Snake. """
        
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
            
            sketch = { 0: (                            ),
                       1: (                            ),
                       2: (                            ),
                       3: (            4, 5, 6, 7,     ),
                       4: (                     7,     ),
                       5: (                     7,     ),
                       6: (                            ),
                       7: (                     7,     ),
                       8: (                            ),
                       9: (                            ),
                      10: (                            ),
                      11: (                            ),
                      12: (                            ),
                      13: (                            ),
                      14: (                            ),
                      15: (            4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5, 6,        ),
                      18: (         3,       6,        ),
                      19: (         3,       6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
            
    class Breakout1(BaseScreen):
        """ First preview for Breakout. """
        
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
            
            sketch = { 0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                       1: (0,                         9),
                       2: (0,                         9),
                       3: (0,       3, 4, 5, 6,       9),
                       4: (0,       3, 4, 5, 6,       9),
                       5: (0,       3, 4, 5, 6,       9),
                       6: (0,       3, 4, 5, 6,       9),
                       7: (0,                         9),
                       8: (0,                         9),
                       9: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                      10: (                            ),
                      11: (               5,           ),
                      12: (                            ),
                      13: (         3, 4, 5,           ),
                      14: (                            ),
                      15: (         3, 4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5,           ),
                      18: (         3,       6,        ),
                      19: (         3, 4, 5,           )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Breakout2(BaseScreen):
        """ Second preview for Breakout. """
        
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
            
            sketch = { 0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                       1: (0,                         9),
                       2: (0,                         9),
                       3: (0,       3, 4, 5, 6,       9),
                       4: (0,       3, 4, 5, 6,       9),
                       5: (0,       3, 4, 5, 6,       9),
                       6: (0,       3, 4, 5, 6,       9),
                       7: (0,                         9),
                       8: (0,                         9),
                       9: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                      10: (                  6,        ),
                      11: (                            ),
                      12: (                            ),
                      13: (         3, 4, 5,           ),
                      14: (                            ),
                      15: (         3, 4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5,           ),
                      18: (         3,       6,        ),
                      19: (         3, 4, 5,           )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Breakout3(BaseScreen):
        """ Third preview for Breakout. """
        
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
            
            sketch = { 0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                       1: (0,                         9),
                       2: (0,                         9),
                       3: (0,       3, 4, 5, 6,       9),
                       4: (0,       3, 4, 5, 6,       9),
                       5: (0,       3, 4, 5, 6,       9),
                       6: (0,       3, 4, 5, 6,       9),
                       7: (0,                         9),
                       8: (0,                         9),
                       9: (0, 1, 2, 3, 4, 5,       8, 9),
                      10: (                            ),
                      11: (                     7,     ),
                      12: (                            ),
                      13: (            4, 5, 6,        ),
                      14: (                            ),
                      15: (         3, 4, 5,           ),
                      16: (         3,       6,        ),
                      17: (         3, 4, 5,           ),
                      18: (         3,       6,        ),
                      19: (         3, 4, 5,           )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Asteroids1(BaseScreen):
        """ First preview for Asteroids. """
        
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
            
            sketch = { 0: (0, 1, 2, 3,             8, 9),
                       1: (0,    2,    4, 5, 6, 7,    9),
                       2: (0,    2,                   9),
                       3: (0,       3, 4, 5,           ),
                       4: (   1,                       ),
                       5: (            4,              ),
                       6: (                            ),
                       7: (                            ),
                       8: (                            ),
                       9: (                            ),
                      10: (                            ),
                      11: (                            ),
                      12: (            4,              ),
                      13: (            4,              ),
                      14: (                            ),
                      15: (            4, 5, 6,        ),
                      16: (         3,                 ),
                      17: (         3,                 ),
                      18: (         3,                 ),
                      19: (            4, 5, 6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Asteroids2(BaseScreen):
        """ Second preview for Asteroids. """
        
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
            
            sketch = { 0: (0, 1, 2, 3,             8, 9),
                       1: (0,    2,    4, 5, 6, 7,    9),
                       2: (0,    2,                   9),
                       3: (0,       3, 4, 5,           ),
                       4: (   1,       4,              ),
                       5: (                            ),
                       6: (                            ),
                       7: (                            ),
                       8: (                            ),
                       9: (                            ),
                      10: (                            ),
                      11: (            4,              ),
                      12: (                            ),
                      13: (            4,              ),
                      14: (                            ),
                      15: (            4, 5, 6,        ),
                      16: (         3,                 ),
                      17: (         3,                 ),
                      18: (         3,                 ),
                      19: (            4, 5, 6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Asteroids3(BaseScreen):
        """ Third preview for Asteroids. """
        
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
            
            sketch = { 0: (0, 1, 2, 3,             8, 9),
                       1: (0,    2,    4, 5, 6, 7,    9),
                       2: (0,    2,                   9),
                       3: (0,       3,    5,           ),
                       4: (   1,                       ),
                       5: (                            ),
                       6: (                            ),
                       7: (                            ),
                       8: (                            ),
                       9: (                            ),
                      10: (            4,              ),
                      11: (                            ),
                      12: (                            ),
                      13: (            4,              ),
                      14: (                            ),
                      15: (            4, 5, 6,        ),
                      16: (         3,                 ),
                      17: (         3,                 ),
                      18: (         3,                 ),
                      19: (            4, 5, 6,        )}
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Tetris1(BaseScreen):
        """ First preview for Tetris. """
        
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
            
            sketch = { 0: (                            ),
                       1: (         3, 4, 5,           ),
                       2: (            4,              ),
                       3: (                            ),
                       4: (                            ),
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
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Tetris2(BaseScreen):
        """ Second preview for Tetris. """
        
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
            
            sketch = { 0: (                            ),
                       1: (                            ),
                       2: (         3, 4, 5,           ),
                       3: (            4,              ),
                       4: (                            ),
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
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
    class Tetris3(BaseScreen):
        """ Third preview for Tetris. """
        
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
            
            for j in sketch.keys():
                for i in sketch[j]:
                    Block(i, j).add(self.render)
            
            self.render.draw(surface)
    
# Template for more screens.
'''
class Newgamei(BaseScreen):
    """ ith preview for Newgame. """
    
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
        
        sketch = { 0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   1: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   2: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   3: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   4: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   5: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   6: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   7: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   8: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                   9: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  10: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  11: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  12: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  13: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  14: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  15: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  16: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  17: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  18: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                  19: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}

        for j in sketch.keys():
            for i in sketch[j]:
                Block(i, j).add(self.render)

        self.render.draw(surface)
'''

def show_high_scores():
    """ Read, format, and show all entries from `high-scores.json`. """

    # Access the current active surface.
    screen = pygame.display.get_surface()

    # Update the window title.
    pygame.display.set_caption("High scores")

    # Set a background.
    screen.fill(BACK_COLOR)

    # Border
    border = pygame.Rect(0, 0, *RES)
    pygame.draw.rect(surface=screen,
                     color=LINE_COLOR,
                     rect=border,
                     width=BORDER_WIDTH,
                     )
    
    # Set a font.
    font = pygame.font.SysFont(None,
                               size=12*PIXEL_SIDE,
                               )

    # Draw the high scores.
    high_scores = {}
    try:
        # Extract from the .json file.
        with open(high_scores_dir, "r") as file:
            high_scores = json.load(file)
    except Exception as e:
        print(e)
        pass
    # Draw the title on the screen.
    h = DIST_BLOCKS
    text = "{0:^25s}".format("HIGH SCORES")  # Centered on top.
    text_surface = font.render(text,
                               False,
                               LINE_COLOR,
                               BACK_COLOR,
                               )
    screen.blit(text_surface, (DIST_BLOCKS, h))
    
    # Iterate through the high scores.
    for game_name, score in high_scores.items():
        h += 2*DIST_BLOCKS
        # First row: game names.
        text_surface = font.render(game_name,
                                   False,
                                   LINE_COLOR,
                                   BACK_COLOR,
                                   )
        screen.blit(text_surface, (DIST_BLOCKS, h))
        # Second row: game scores.
        text_score = f"{score:07d}"
        text_surface = font.render(text_score,
                                   False,
                                   LINE_COLOR,
                                   BACK_COLOR,
                                   )
        screen.blit(text_surface, (6*DIST_BLOCKS, h))
