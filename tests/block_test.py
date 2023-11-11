""" Testing `block.py` elements. """

import pygame
from ..constants import BACK_COLOR, FPS
from ..client import BaseClient
from ..block import *


class Client(BaseClient):
    """
    A functioning client with some tests for `Block` and its derivatives.

    Test targets:

    1. `Block` display
    2. `BlinkingBlock` display and behavior
    3. `Bomb` display and its methods
    4. `set_position()` for `Block` and `BlinkingBlock`
    """

    def __init__(self):
        """ Initializing the tested objects and their containers. """

        # GUI initialization.
        super().__init__()
        pygame.display.set_caption("Block test")

        # Draw a background.
        self.back = self.screen.copy()
        self.back.fill(BACK_COLOR)

        # Create groups and add sprites to them.
        self.entities = {
            1: pygame.sprite.RenderPlain(),
            2: pygame.sprite.RenderPlain(BlinkingBlock(5, 5)),
            3: pygame.sprite.RenderPlain(),
            4: pygame.sprite.RenderPlain(),
        }

        # First test's target: static `Block`s.
        self.coords = [(3, 3), (3, 2)]
        self.blocks = []  # Holds references.
        for (i, j) in self.coords:
            block = Block(i, j, direction="down")
            block.add(self.entities[1])
            self.blocks.append(block)

        # Second test's target: static `BlinkingBlock` already added to
        # `entities`.
        #co = [(7,7),(7,6),(7,5),(7,8),(4,12)]
        #for (i, j) in co:
        #    self.entities[2].add(BlinkingBlock(i, j))

        # Third test's target: `Bomb`.
        self.bomb = Bomb(5, 10, group=self.entities[3])

        # Fourth test's target: `set_position()` method for `Block` and
        # `BlinkingBlock`
        self.b1 = Block(0, 0)
        self.b2 = BlinkingBlock(9, 19)
        self.entities[4].add(self.b1, self.b2)

    def loop(self, t):
        """ List of scheduled events. """

        # Clean the screen.
        self.screen.fill(BACK_COLOR)

        if t > 5*FPS:  # After 5 seconds, do...

            # Test movement for `Snake`: move down two `Block`s.
            i, j = self.coords[0]
            # Draw a third `Block` below and store its data.
            block = Block(i, j+1)
            block.add(self.entities[1])
            self.coords.insert(0, (i, j+1))
            self.blocks.insert(0, block)
            # Delete the first `Block`'s drawing and data, creating an
            # illusion of movement.
            self.blocks[-1].kill()
            self.blocks.pop()
            self.coords.pop()

            # Test `BlinkingBlock`'s blinking: by visual checking
            # and tracking its `image` attribute for 5 seconds.
            if t <= 10*FPS:
                print(
                    [blink.image == blink._image
                     for blink in self.entities[2]
                     ]
                )

            # Test `Bomb`'s methods.
            # Change for `"down"` to test the `Bomb`'s behavior when it
            # reaches the bottom of the grid. Quote all occurrences of
            # `2` to test for the top instead.
            self.bomb.move("up")
            self.bomb.check_explosion(target_group=self.entities[2])

            # Test `.set_position()`
            i, j = self.b1.coords
            self.b1.set_position(i+1, j+1)
            if t % (2*FPS) == 0:
                i, j = self.b2.coords
                self.b2.set_position(i-1, j-1)

        # Update sprites' mechanics.
        for entity in self.entities.values():
            for block in entity:
                block.update(t=t, speed=1)

        # Draw the objects to the screen.
        for entity in self.entities.values():
            entity.draw(self.screen)


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
