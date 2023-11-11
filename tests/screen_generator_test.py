""" Testing `screen_generator.py` elements. """

import pygame
from ..constants import FPS
from ..client import BaseClient
from ..block import *
from ..screen_generator import *


class BackgroundClient(BaseClient):
    """ A client with a background. """

    def __init__(self):
        # GUI initialization.
        super().__init__()
        pygame.display.set_caption("Background test")

        # Draw a background.
        Background()


class Client(BackgroundClient):
    """ Testing the victory and defeat messages. """

    def loop(self, t):
        """ Shift through the screens. """

        if t % (20*FPS) == 5*FPS:
            DefeatScreen()
        elif t % (20*FPS) == 10*FPS:
            VictoryScreen()
        elif t % (20*FPS) == 0:
            Background()


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
