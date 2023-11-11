""" This module contains an implementation of a Breakout-like game. """

import pygame
from pygame.locals import *
from ..constants import *
from ..client import BaseClient
from ..block import Block
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Breakout"]


class Breakout(Game):
    """
    Implements `Game` with a game of 'breakout'.

    Attributes
    ----------
    number : int
        Amount of remaining `Block`s.
    start_speed : int
        Storing the starting value for ``speed``.
    entities : dict
        Containers for the objects to be drawn (name:group).
    """

    _total = 0
    number = 0
    start_speed = 20
    entities = {"target": pygame.sprite.RenderPlain(),
                "ball":   pygame.sprite.RenderPlain(),
                "paddle": pygame.sprite.RenderPlain(),
                }
    
    def __init__(self):
        """ Initialize instance attributes and instantiate game objects. """

        super().__init__()
        self.level = 1  # Starting stage.
        self.speed = Breakout.start_speed  # Internal speed for `ball`.

        # Spawn the entities.
        self.target = self.Target(self.level)
        self.ball = self.Ball(4, 18)
        self.paddle = self.Paddle(self.ball)
    
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

        if self.running:
            if state == KEYDOWN:  # Key pressed.
                # Set `Paddle`'s movement.
                if key == K_LEFT:
                    self.Paddle.direction = "left"
                elif key == K_RIGHT:
                    self.Paddle.direction = "right"
                elif key == K_SPACE:
                    self.speed *= 2

            if state == KEYUP:  # Key released.
                if key == K_LEFT:
                    self.Paddle.direction = ""
                elif key == K_RIGHT:
                    self.Paddle.direction = ""
                elif key == K_SPACE:
                    self.speed /= 2
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            # Set the action rate at `speed` blocks per second.
            if t % int(FPS/self.speed) == 0:
                # Check if the `ball` hit `target`.
                self.target.check_hit(self.ball)
                self.update_score()

                # Check if there still are `Block`s left in `target`.
                # If not, call the next stage.
                self.manage_levels()

                self.ball.check_border_reflect()
                
                # Deal with immediate collision after hitting a border.
                self.target.check_hit(self.ball)
                self.update_score()
                self.manage_levels()

                # `paddle` dragging `ball`.
                self.paddle.check_paddle_drag()
                self.paddle.check_paddle_reflect()

                # Avoid the `ball` from leaving the screen by the
                # lateral borders.
                self.ball.check_border_reflect()

                # Make the `paddle` move.
                self.paddle.move(self.speed)
        
        super().manage()  # Manage endgame.
    
    def update_score(self):
        """ Scoring mechanics. """

        n = len(Breakout.entities["target"].sprites())  # `target`'s `Block`s left.
        for _ in range(Breakout.number, n, -1):
            if self.level == 1:
                self.score += 15
            elif self.level == 2:
                self.score += 20
            elif self.level == 3:
                self.score += 30
        Breakout.number = n  # Update the number of `target`'s `Block`s.
        super().update_score()
    
    def manage_levels(self):
        """ Turns to the next stage upon clearing the current one. """

        if not Breakout.entities["target"]:
            # Toggle the next stage.
            print("Stage", self.level, "cleared")
            self.level += 1
            # Add score bonus from phase completion.
            self.score += 3000 + 3000*(self.level - 1)
            # Construct the next `target`.
            self.target = self.Target(self.level)
            # Respawn the `ball`.
            Breakout.entities["ball"].empty()
            self.ball = self.Ball(4, 18)
            # Respawn the `paddle`.
            Breakout.entities["paddle"].empty()
            self.paddle = self.Paddle(self.ball)
    
    def check_victory(self):
        """
        Victory occurs when all 3 stages are cleared.

        Returns
        -------
        bool
            Whether the game has been beaten.
        """

        if self.level == 4:
            return True
        else:
            return False
    
    def check_defeat(self):
        """
        Defeat happens if the ``ball`` falls from the bottom border.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        if self.ball.coords[1] > 19:
            return True
        else:
            return False
    
    class Target:
        """
        Manages the `Block`s to be destroyed.

        Organizes the drawing and breaking of the target `Block`s at
        the top of the grid.
        """
        
        def __init__(self, level):
            """
            Build the target's structure.

            Parameters
            ----------
            level : int
                Current stage.
            """

            # Clean the `target`'s drawing and references.
            Breakout.entities["target"].empty()

            if level == 1:
                sketch = {0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          1: (0,                         9),
                          2: (0,                         9),
                          3: (0,       3, 4, 5, 6,       9),
                          4: (0,       3, 4, 5, 6,       9),
                          5: (0,       3, 4, 5, 6,       9),
                          6: (0,       3, 4, 5, 6,       9),
                          7: (0,                         9),
                          8: (0,                         9),
                          9: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}

                self.block = {}
                for j in sketch.keys():
                    for i in sketch[j]:
                        self.block[(i, j)] = Block(i, j)
                        self.block[(i, j)].add(Breakout.entities["target"])

            elif level == 2:
                sketch = {0: (0, 1,                   8, 9),
                          1: (0, 1, 2,             7, 8, 9),
                          2: (   1, 2, 3,       6, 7, 8   ),
                          3: (      2, 3, 4, 5, 6, 7      ),
                          4: (   1, 2, 3,       6, 7, 8   ),
                          5: (0, 1, 2,             7, 8, 9),
                          6: (0, 1,                   8, 9)}
                self.block = {}
                for j in sketch.keys():
                    for i in sketch[j]:
                        self.block[(i, j)] = Block(i, j)
                        self.block[(i, j)].add(Breakout.entities["target"])

            elif level == 3:
                sketch = {0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          1: (0,          4, 5,          9),
                          2: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          3: (0,          4, 5,          9),
                          4: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          5: (0,          4, 5,          9),
                          6: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}
                self.block = {}
                for j in sketch.keys():
                    for i in sketch[j]:
                        self.block[(i, j)] = Block(i, j)
                        self.block[(i, j)].add(Breakout.entities["target"])

            Breakout._total = len(self.block)
            Breakout.number = Breakout._total

            # Model for more stages
            #
            # sketch = {0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           1: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           2: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           3: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           4: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           5: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            #           6: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}
        
        def check_hit(self, ball):
            """
            Collision mechanics between ``ball`` and ``target``.

            Parameters
            ----------
            ball : Breakout.Ball
                The ``Ball`` instance.
            """

            a, b = ball.velocity
            i, j = ball.coords
            
            # When the `ball` hits a corner...
            if ((i+a, j) in self.block.keys()
                    and (i, j+b) in self.block.keys()):
                # ... reverse both directions, ...
                ball.velocity = [-a, -b]
                # ... destroy both `Block`s that make the corner, ...
                self.block[(i+a, j)].kill()
                self.block[(i, j+b)].kill()
                del self.block[(i+a, j)]
                del self.block[(i, j+b)]
                # ... including the vertex, if it exists.
                if (i+a, j+b) in self.block.keys():
                    self.block[(i+a, j+b)].kill()
                    del self.block[(i+a, j+b)]
            
            # When the `ball` hits the `target`'s `Block`s horizontally only...
            elif ((i+a, j) in self.block.keys()
                  and (i, j+b) not in self.block.keys()):
                # ... reverse only its first coordinate, ...
                ball.velocity = [-a, b]
                # and destroy only the `Block` it hit.
                self.block[(i+a, j)].kill()
                del self.block[(i+a, j)]
            
            # When the `ball` hits the `target`'s `Block`s vertically only...
            elif ((i+a, j) not in self.block.keys()
                    and (i, j+b) in self.block.keys()):
                # ... reverse only its second coordinate, ...
                ball.velocity = [a, -b]
                # and destroy only the `Block` it hit.
                self.block[(i, j+b)].kill()
                del self.block[(i, j+b)]
            
            # When the `ball` hits the `target`'s `Block`s at exactly a vertex...
            elif (i+a, j+b) in self.block.keys():
                # ... reverse both directions, ...
                ball.velocity = [-a, -b]
                # ... and destroy the `Block` at said vertex.
                self.block[(i+a, j+b)].kill()
                del self.block[(i+a, j+b)]

            # Adjust from positional coordinates to the appropriate
            # number of pixels.
            ball.displacement = [x*DIST_BLOCKS for x in ball.velocity]
    
    class Paddle:
        """
        Manages the player-controlled paddle.

        Organizes the drawing, movement, dragging, and reflection off
        of the paddle.

        Attributes
        ----------
        direction : str
            Where to move: ``"left"`` or ``"right"``.
        dragging : bool
            Whether the paddle is currently dragging the ``ball``.
        """

        direction = ""
        dragging = False
        
        def __init__(self, ball):
            """
            Build the paddle (dragging the ``ball`` at start).

            Parameters
            ----------
            ball : Breakout.Ball
                The ``Ball`` instance.
            """

            self.ball = ball
            
            # Set the `paddle`'s initial position.
            self.blocks = [Block(3, 19), Block(4, 19), Block(5, 19)]
            self._size = len(self.blocks) - 1

            # Add the `ball` to the `paddle` initially to allow for a
            # launching choice.
            self.blocks.append(self.ball)

            # Track coordinates and add to the corresponding `Group`
            # for drawing.
            self.coords = [block.coords for block in self.blocks]
            Breakout.entities["paddle"].add(*self.blocks)
        
        def move(self, speed):
            """
            Movement mechanics for the paddle, and ``ball``'s launch.

            Parameters
            ----------
            speed : float
                Current ``ball``'s speed in `Block`s per second.
            """

            # Take a reference at the leftmost horizontal coordinate of
            # the `paddle`.
            i_0 = self.coords[0][0]
            a, _ = CONVERT[self.direction]  # Only horizontal matters.
            for block in self.blocks:
                i, j = block.coords
                # Ensures the `paddle` will remain within the screen.
                if 0 <= i_0+a < 10-self._size:
                    block.set_position(i+a, j)

            # Update the `paddle`'s coordinates.
            self.coords = [block.coords for block in self.blocks]

            # Launch mechanics at the start of the stage (the `ball` is
            # released from the `paddle` if *Space* is pressed).
            if speed > Breakout.start_speed:
                if (len(self.coords) == 4  # Stage start conditions.
                        and Breakout.number == Breakout._total):
                    Breakout.entities["paddle"].remove(self.ball)
                    self.blocks.pop()
                    self.coords.pop()
                    # Update `ball` data.
                    self.ball._direction = "NE"
                    self.ball.velocity = [1, -1]  # First direction.
        
        def check_paddle_drag(self):
            """ Manages ``ball`` drag and release. """

            i, j = self.ball.coords
            _, b = self.ball.velocity
            # Allow for dragging the `ball` when it hits the `paddle`
            # from the top.
            if (i, j+b) in self.coords[:self._size]:
                # The `ball` will become part of the `paddle` for exactly
                # one iteration.
                self.ball.displacement = [0, 0]  # Won't move on its own.
                Breakout.Paddle.dragging = not self.dragging
                if self.dragging:
                    self.blocks.append(self.ball)
                    Breakout.entities["paddle"].add(self.ball)
                else:
                    self.blocks.pop()
                    self.coords.pop()
                    Breakout.entities["paddle"].remove(self.ball)
            else:
                # Since we only changed `ball.displacement`,
                # `ball.velocity` still stores its previous value.
                self.ball.displacement = [x*DIST_BLOCKS
                                          for x in self.ball.velocity
                                          ]
        
        def check_paddle_reflect(self):
            """ Hypothesis for when the ``ball`` reflects from the ``paddle``. """

            if not self.dragging:
                a, b = self.ball.velocity
                i, j = self.ball.coords
                # Reflection occurs if the `ball` hits the `paddle`
                # from above or at a vertex.
                if ((i, j+b) in self.coords[:self._size]
                        or (i+a, j+b) in self.coords[:self._size]):
                    # Reverse the vertical coordinate.
                    self.ball.velocity[1] = -1
                    # Depending on where the ball hits the `paddle`,
                    # horizontal reflection may or may not happen.
                    if ((i, j+b) == self.coords[0]
                            or (i+a, j+b) == self.coords[0]):
                        # The ball moves left if it hit the left corner
                        # of the `paddle`.
                        self.ball.velocity[0] = -1
                    elif ((i, j+b) == self.coords[self._size-1]
                          or (i+a, j+b) == self.coords[self._size-1]):
                        # The `ball` moves right if it hit the right corner
                        # of the `paddle`.
                        self.ball.velocity[0] = 1
                # Adjust from positional coordinates to the appropriate
                # number of pixels.
                self.ball.displacement = [x*DIST_BLOCKS
                                          for x in self.ball.velocity
                                          ]
    
    class Ball(Block):
        """
        Deals with ball's spawning and border reflection.

        All other interactions have already been taken care of.
        """

        def __init__(self, i, j):
            self.velocity = [0, 0]
            super().__init__(i, j)

            # Add `self` (a `Sprite`) to a `Group` for drawing.
            Breakout.entities["ball"].add(self)
        
        def check_border_reflect(self):
            """ Hypothesis for when the ``ball`` reflects from the border. """

            a, b = self.velocity
            i, j = self.coords
            # Reverse the horizontal coordinate if the `ball` hits a
            # vertical border.
            if (i == 0 and a == -1) or (i == 9 and a == 1):
                self.velocity[0] = -a
            # Reverse the vertical coordinate if the `ball` hits a
            # horizontal border.
            if j == 0 and b == -1:
                self.velocity[1] = 1
            
            # Adjust from positional coordinates to the appropriate
            # number of pixels.
            if not Breakout.Paddle.dragging:
                self.displacement = [x*DIST_BLOCKS
                                     for x in self.velocity
                                     ]


class Client(BaseClient):
    """ A client for :class:`Breakout`. """

    def __init__(self):
        """ Initializing the GUI and the game. """

        super().__init__()
        pygame.display.set_caption("Breakout Game")

        self.game = Breakout()

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


def main():
    """ Output-generating commands. """

    print("Check `", game_manuals, "` for instructions.", sep="")
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
