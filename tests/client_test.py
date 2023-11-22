""" Testing some `client.py` elements. """

import sys
import pygame
from ..constants import *
from ..client import *


class Client1(BaseClient):
    """ A (theoretically) functioning client: plain. """

    pass


class Client2(BaseClient):
    """ A (theoretically) functioning client: title and background. """

    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Title test")
        self.screen.fill(SHADE_COLOR)


class Client3(Client2):
    """ A (theoretically) functioning client: drawing squares. """

    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
        self.j = 1
        self.draw_square(0, 0)

    def draw_square(self, i, j):
        """ Draw a `LINE_COLOR` square on `self.screen`. """

        # Create a small surface to draw on.
        self.image = pygame.Surface((BLOCK_SIDE, BLOCK_SIDE))
        self.image.fill(BACK_COLOR)
        # Extract its `.rect` container.
        self.rect = self.image.get_rect()
        # Place it according to `i` and `j`.
        self.rect.topleft = (
            BORDER_WIDTH + i*DIST_BLOCKS,
            BORDER_WIDTH + j*DIST_BLOCKS
        )
        # Draw an empty square in this smaller surface.
        pygame.draw.rect(
            self.image,
            LINE_COLOR,
            pygame.Rect(0, 0, BLOCK_SIDE, BLOCK_SIDE),
            PIXEL_SIDE,
        )
        # Update (blit) the drawing to the smaller surface.
        self.image.blit(self.image, (0, 0))
        # Update (blit) the smaller surface to the original.
        self.screen.blit(self.image, self.rect)

    def loop(self, t):
        """ List of scheduled events. """

        if t % FPS == 0:  # Every second, do...
            # Create another square below the previous ones.
            self.draw_square(0, self.j)
            self.j += 1


class Client4(Client3):
    """ Moving a square. """

    def loop(self, t):
        """ List of scheduled events. """

        if t % FPS == 0:  # Every second, do...
            # Clean the screen.
            self.screen.fill(BACK_COLOR)
            # Create another square below the previous ones.
            self.draw_square(0, self.j)
            self.j += 1


def main(args):
    """ Output-generating commands. """

    if len(args) != 2:
        print("Please provide one argument to specify the class, for example:")
        print("python -m brickgame_pygame.tests.client_test 1")
    else:
        if args[1] == "1":  # Creating the window and keeping it open.
            client = Client1()
            client.start()
        elif args[1] == "2":  # Changing title and background.
            client = Client2()
            client.start()
        elif args[1] == "3":  # Filling a line with squares.
            client = Client3()
            client.start()
        elif args[1] == "4":  # Moving a square.
            client = Client4()
            client.start()
        else:
            print("Client", args[1], " was not implemented yet.", sep="")


if __name__ == '__main__':
    main(sys.argv)
