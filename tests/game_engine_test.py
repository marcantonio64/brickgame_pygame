""" Testing `game_engine.py` elements. """

import random
import pygame
from ..constants import FPS
from ..client import BaseClient
from ..block import *
from ..games.game_engine import *


class NewGame(Game):
    entities = {"block": pygame.sprite.RenderPlain(),
                "food":  pygame.sprite.RenderPlain(),
                "bomb":  pygame.sprite.RenderPlain()}

    def __init__(self):
        super().__init__()

        # Spawning a `Block` at (3, 3) that moves down.
        Block(3, 3, direction="down").add(self.entities["block"])

        # Spawning a `BlinkingBlock` at a random position.
        i = random.randint(0, 9)
        j = random.randint(0, 19)
        BlinkingBlock(i, j).add(self.entities["food"])

        # Spawning a `Bomb` at (5, 10).
        Bomb(5, 10, group=self.entities["bomb"])

    def handle_events(self, key, state):
        super().handle_events(key, state)

    def manage(self):
        super().manage()

    def update_score(self):
        super().update_score()

    def check_victory(self):
        super().check_victory()

    def check_defeat(self):
        super().check_defeat()


class Client(BaseClient):
    """ A functioning client with some tests for `Game`. """

    def __init__(self):
        """ Initializing the tested objects and their containers. """

        super().__init__()
        pygame.display.set_caption("Game test")

        # Initialize the game.
        self.game = NewGame()

    def loop(self, t):
        """ List of scheduled events. """

        # Update `Block`'s mechanics.
        self.game.update_entities(t=t)

        # Implement the game mechanics and check for endgame.
        self.game.manage()

        # Draw the game objects to the screen.
        self.game.draw_entities()

        # Tests for `game`'s methods.
        if t == FPS*10:    # 10 seconds mark.
            self.game.toggle_defeat()
        elif t == 15*FPS:  # 15 seconds mark.
            self.game.toggle_victory()
        elif t == 20*FPS:  # 20 seconds mark.
            self.game.reset()

    def handle_events(self, key, state):
        """ Deal with user input. """
        self.game.handle_events(key, state)


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
