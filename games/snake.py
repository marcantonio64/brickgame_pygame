""" This module contains an implementation of a Snake game. """

import random
import pygame
from pygame.locals import *
from ..constants import *
from ..client import BaseClient
from ..block import Block, BlinkingBlock
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Snake"]


class Snake(Game):
    """
    Implements `Game` with a snake game.

    Attributes
    ----------
    direction : str
        Where the snake should turn to.
    growing : bool
        Whether the snake should grow one block after eating.
    entities : dict
        Containers for the objects to be drawn (name:group).
    """

    direction = "down"
    growing = False
    entities = {"body": pygame.sprite.RenderPlain(),
                "food": pygame.sprite.RenderPlain(),
                }
    
    def __init__(self):
        """ Initialize instance attributes and instantiate game objects. """

        super().__init__()
        self.speed = 10
        self.key_enabled = False
        """ Allows only one directional movement at a time. """

        # Spawn the entities.
        self.snake = self.Body()
        self.food = self.Food()

    def reset(self):
        """ Remove all elements from the screen and start again. """

        Snake.direction = "down"
        Snake.growing = False
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

        if self.running:
            if state == KEYDOWN:  # Key pressed.
                if key == K_SPACE:
                    self.speed *= 2
                # Lock direction changes after the first until the next iteration.
                elif self.key_enabled:
                    self.key_enabled = False
                    # Direction changes, making sure the snake's head won't enter itself.
                    if key == K_UP and self.direction != "down":
                        Snake.direction = "up"
                    elif key == K_DOWN and self.direction != "up":
                        Snake.direction = "down"
                    elif key == K_LEFT and self.direction != "right":
                        Snake.direction = "left"
                    elif key == K_RIGHT and self.direction != "left":
                        Snake.direction = "right"

            if state == KEYUP:  # Key released.
                if key == K_SPACE:
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
            self.check_eat()
            # Set the action rate at `speed` blocks per second.
            if t % int(FPS/self.speed) == 0:
                self.update_score()
                self.snake.move()
                self.key_enabled = True
        
        super().manage()  # Manage endgame.
    
    def check_eat(self):
        """ The snake grows if it reaches the food. """

        if self.snake.head.coords == self.food.coords:
            Snake.growing = True
            self.food.respawn()
            # Avoid the food spawning inside the snake.
            while self.food.coords in self.snake.coords:
                self.food.respawn()
    
    def update_score(self):
        """ Scoring mechanics. """

        n = len(self.snake.segments)
        if self.growing:
            if 3 < n <= 25:
                self.score += 15
            elif 25 < n <= 50:
                self.score += 45
            elif 50 < n <= 100:
                self.score += 100
            elif 100 < n < 200:
                self.score += 250
        super().update_score()
    
    def check_victory(self):
        """
        Victory occurs when the snake's size becomes the whole grid.

        Returns
        -------
        bool
            Whether the game has been beaten.
        """

        n = len(self.snake.segments)
        if n == 200:
            return True
        else:
            return False
    
    def check_defeat(self):
        """
        Defeat happens if the snake's head hits its body or the borders.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        i, j = self.snake.head.coords
        if ((0 <= i < 10) and
                (0 <= j < 20) and
                (i, j) not in self.snake.coords[1:]):
            return False
        else:
            return True
    
    class Body:
        """ Organizes the snake's drawing, movement, and growth. """
        
        def __init__(self):
            # Set the snake's initial position.
            self.segments = [Block(4, 5), Block(4, 4), Block(4, 3)]
            self.coords = [segment.coords for segment in self.segments]

            # Add its `Block`s to the container for drawing.
            Snake.entities["body"].add(*self.segments)

            # Identify the head and the tail.
            self.head = self.segments[0]
            self.tail = self.segments[-1]
        
        def move(self):
            """ Handle the snake's movement and growth mechanics. """
            
            # Movement is achieved by creating a new `Block` sprite in
            # the head's next position, ...
            i, j = CONVERT[Snake.direction]
            a, b = self.head.coords
            self.head = Block(i+a, j+b)
            self.segments.insert(0, self.head)
            Snake.entities["body"].add(self.head)
            # ... keeping the tail in the same place if the head doesn't
            # hit the food, ...
            if Snake.growing:
                Snake.growing = False
            else:
                # ... or deleting it (references and drawing) otherwise.
                self.segments.pop()
                self.tail.kill()
                self.tail = self.segments[-1]

            # Update the list of coordinates.
            self.coords = [segment.coords
                           for segment in self.segments]
    
    class Food(BlinkingBlock):
        """ Organizes the food's spawn randomly. """
        
        def __init__(self):
            """ Generate random coordinates to spawn a `BlinkingBlock` at. """

            i = random.randint(0, 9)
            j = random.randint(0, 19)
            super().__init__(i, j)
            # Add the instance to the container for drawing.
            Snake.entities["food"].add(self)
        
        def respawn(self):
            """ Generate new random coordinates to move the `BlinkingBlock` to. """

            i = random.randint(0, 9)
            j = random.randint(0, 19)
            self.set_position(i, j)


class Client(BaseClient):
    """ A client for :class:`Snake`. """

    def __init__(self):
        """ Initializing the GUI and the game. """

        super().__init__()
        pygame.display.set_caption("Snake Game")

        self.game = Snake()

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
