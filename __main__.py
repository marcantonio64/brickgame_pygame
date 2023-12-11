""" Entry point for the execution of the main package. """

import json
import pygame
from pygame.locals import *
from .constants import *
from .client import BaseClient
from .screen_generator import Background, GamePreview, show_high_scores
from .client import package_dir, high_scores_dir
from .games import game_manuals
from .games.snake import Snake
from .games.breakout import Breakout
from .games.asteroids import Asteroids
from .games.tetris import Tetris


class Brickgame(BaseClient):
    """
    Manages all the console and game mechanics and their interactions.

    Attributes
    ----------
    environment : str
        The active environment for user input.
    game : Type[Game]
        The current game being played.
    """

    environment = "selector"
    game = None
    
    def __init__(self):
        """ Initializing the GUI. """

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
        
        super().__init__()
        pygame.display.set_caption("Game Selection")

        # Render the environments.
        self.selector = self.Selector()

        # Draw the background.
        Background()

    def loop(self, t):
        """
        List of scheduled events.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.environment == "selector":
            self.selector.animate_screen(t)
        elif self.environment == "game":
            # Implement the game mechanics and check for endgame.
            self.game.manage(t)
            # Update sprites' mechanics.
            self.game.update_entities(t=t)
            # Show the game's current state.
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

        if state in (KEYDOWN, KEYUP):
            if self.environment == "selector":
                # Shift to `selector` keybindings.
                self.selector.handle_events(key, state)
            elif self.environment == "game":
                # Leave the `game` instance if *Backspace* is pressed.
                if (key, state) == (K_BACKSPACE, KEYDOWN):
                    Brickgame.environment = "selector"
                    pygame.display.set_caption("Game Selection")
                else:
                    # Shift to `game` keybindings otherwise.
                    self.game.handle_events(key, state)
    
    class Selector:
        """ Mechanics for game selection, previews, and high scores. """

        def __init__(self):

            # Instantiate all the game classes.
            # (Their loops start only when selected.)
            self.select = {1: Snake(),
                           2: Breakout(),
                           3: Asteroids(),
                           4: Tetris(),
                           }
            self.number_of_games = len(self.select)
            self.stage_id = 1  # Show `Snake` first.
            self.name = self.select[self.stage_id].__class__.__name__
        
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

            if state == KEYDOWN:  # Key press.
                if key == K_RETURN:
                    # Entering a game.
                    if self.stage_id <= self.number_of_games:
                        Brickgame.environment = "game"
                        Brickgame.game = self.select[self.stage_id]
                        self.name = Brickgame.game.__class__.__name__
                        # Update the window title and inform of the
                        # game change.
                        pygame.display.set_caption(self.name)
                        print("Now playing:", self.name)
                        # This avoids the need for pressing *Return*
                        # twice after endgames.
                        if not Brickgame.game.running:
                            Brickgame.game.reset()
                        #if self.name == "Tetris":
                        #    Brickgame.game.piece.preview()
                # Choosing a game.
                elif key == K_LEFT:
                    if self.stage_id > 1:
                        if self.stage_id > self.number_of_games:
                            pygame.display.set_caption("Game Selection")
                        self.stage_id -= 1
                    else:
                        self.stage_id = self.number_of_games+1
                        show_high_scores()
                elif key == K_RIGHT:
                    if self.stage_id <= self.number_of_games:
                        self.stage_id += 1
                        if self.stage_id > self.number_of_games:
                            show_high_scores()
                    else:
                        self.stage_id = 1
                        pygame.display.set_caption("Game Selection")
        
        def animate_screen(self, t):
            """
            Toggle game previews.

            Iterates through each game's previews, with 3 frames per
            second. The previews were built using pixel images, in the
            :mod:`_screen_generator`_ module.

            Parameters
            ----------
            t : int
                Main timer.
            """

            if t % FPS == 0:  # 0.000s
                if self.stage_id == 1:
                    GamePreview.Snake1()
                elif self.stage_id == 2:
                    GamePreview.Breakout1()
                elif self.stage_id == 3:
                    GamePreview.Asteroids1()
                elif self.stage_id == 4:
                    GamePreview.Tetris1()
            elif t % FPS == int(FPS/3):  # 0.333s
                if self.stage_id == 1:
                    GamePreview.Snake2()
                elif self.stage_id == 2:
                    GamePreview.Breakout2()
                elif self.stage_id == 3:
                    GamePreview.Asteroids2()
                elif self.stage_id == 4:
                    GamePreview.Tetris2()
            elif t % FPS == int(2*FPS/3):  # 0.666s
                if self.stage_id == 1:
                    GamePreview.Snake3()
                elif self.stage_id == 2:
                    GamePreview.Breakout3()
                elif self.stage_id == 3:
                    GamePreview.Asteroids3()
                elif self.stage_id == 4:
                    GamePreview.Tetris3()


def main():
    """ Output-generating commands. """

    print("Check `", game_manuals, "` for instructions.", sep="")
    brickgame = Brickgame()
    brickgame.start()


if __name__ == '__main__':
    main()
