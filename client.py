""" Establishing the basic structure of the client. """

import os
import pygame
from pygame.locals import *
from abc import ABC
from .constants import *

package_dir = os.path.abspath(
    os.path.dirname(__file__)
)
""" Directory of the main package. """
high_scores_dir = os.path.join(
    package_dir,
    "high-scores.json"
)
""" Directory of `high-scores.json`. """

__all__ = ["BaseClient", "package_dir", "high_scores_dir"]


class BaseClient(ABC):
    """ General GUI and loop configs. """

    def __init__(self):
        """ Initialize a GUI and create a `pygame.Surface` object. """

        self._run = True
        # Initialize the window.
        pygame.init()
        self.screen = pygame.display.set_mode(RES)  # Surface object.
        self.screen.fill(BACK_COLOR)
        pygame.mouse.set_visible(0)   # Hiding the cursor.

    def _loop(self):
        """ A hidden method avoids interference. """

        # Start the timer.
        t = 0
        clock = pygame.time.Clock()
        while self._run:
            t += 1
            # Set the frame rate.
            clock.tick(FPS)
            # Read user input.
            self._handle_events()
            # Extra schedules.
            self.loop(t)
            # Update the screen.
            pygame.display.flip()

    def _handle_events(self):
        """ Set up the structure for input events. """

        # Open a queue of events.
        for event in pygame.event.get():
            state = event.type
            # Key press and release.
            if state in (KEYDOWN, KEYUP):
                key = event.key
            # Window exit conditions.
            if state == QUIT:  # Closing directly.
                self._run = False
            elif state == KEYDOWN:
                if key == K_ESCAPE:  # Pressing ESC.
                    self._run = False
            # If a key is pressed or released, switch to the standard.
            if state in (KEYDOWN, KEYUP):
                self.handle_events(key, state)

    def start(self):
        """ Allow for more definition before starting the main loop. """

        self._loop()

    def loop(self, t):
        """ Schedule loop events. """

        pass

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

        pass
