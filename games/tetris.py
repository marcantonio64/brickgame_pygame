""" This module contains an implementation of a Tetris game. """

import random
import pygame
from pygame.locals import *
from ..constants import *
from ..client import BaseClient
from ..block import Block, Bomb
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Tetris"]

USE_BOMBS = False


class Tetris(Game):
    """ Implements `Game` with a Tetris game.

    Attributes
    ----------
    start_speed : int
        Storing the starting value for ``speed``.
    entities : dict
        Containers for the objects to be drawn (name:group).
    """

    start_speed = 1
    entities = {"piece":  pygame.sprite.RenderPlain(),
                "fallen": pygame.sprite.RenderPlain(),
                }
    
    def __init__(self):
        """ Initialize instance attributes and instantiate game objects. """

        super().__init__()
        self.__start = 0
        self.__bomb_at_bottom = False
        self.speed = Tetris.start_speed  # Fall speed (in `Block`s per second).

        # Spawn the entities.
        self.piece = self.Piece()  # Tetrominoes
        self.fallen = self.FallenBlocks()  # Fallen remains

    def _detect_game_on(self):
        """ Prevent the first preview from showing in the main client. """

        if self.__start:
            self.piece.preview()
        self.__start += 1
    
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
                # Set `Piece`'s movement.
                if key == K_UP:
                    self.piece.rotate()
                elif key == K_DOWN:
                    self.Piece.direction = "down"
                elif key == K_LEFT:
                    self.Piece.direction = "left"
                elif key == K_RIGHT:
                    self.Piece.direction = "right"
                elif key == K_SPACE:
                    self.piece.fall_inst()
                    if (self.piece.active_shape == "B"
                            and self.piece.coords[1] < 17):
                        self.piece.move("down")
                    self.try_spawn_next()
                # Set `switch()`.
                elif key == K_RSHIFT:
                    if not self.piece.lock_switch:
                        self.piece.switch()  # Only once for every new `piece`.

            if state == KEYUP:  # Key released.
                if key == K_DOWN:
                    self.Piece.direction = ""
                elif key == K_LEFT:
                    self.Piece.direction = ""
                elif key == K_RIGHT:
                    self.Piece.direction = ""
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            # self._detect_game_on()
            # Set the action rate at `speed` `Block`s per second.
            if t % int(FPS/self.speed) == 0:
                self.piece.move("down")  # Slow fall
                self.try_spawn_next()

            # `speed` scales over time, every 30 seconds.
            if self.speed <= 10:
                if t % (30*FPS) == 0:
                    self.speed *= 10**0.05
            
            # Adjust for movement proportional to the scaling `speed`.
            if t % int(FPS/(7 + 3*self.speed)) == 0:
                # Horizontal movement and downwards acceleration.
                self.piece.move(self.piece.direction)
                self.try_spawn_next()

        super().manage()  # Manage endgame.
    
    def update_score(self, full_lines_number):
        """ Scoring mechanics. """
        
        # More points for more lines at once.
        if full_lines_number == 1:
            self.score += int(2 + self.speed*self.fallen.height)*15
        elif full_lines_number == 2:
            self.score += int(6 + self.speed*self.fallen.height)*15
        elif full_lines_number == 3:
            self.score += int(12 + self.speed*self.fallen.height)*15
        elif full_lines_number == 4:
            self.score += int(20 + self.speed*self.fallen.height)*15
        super().update_score()
    
    def try_spawn_next(self):
        """ `piece`s spawn when they stop falling. """

        if self.piece.height == 0:
            if self.piece.active_shape != "B":  # Normal `piece`
                self.spawn_next()
            else:  # `Bomb` colliding:
                _, j = self.piece.coords
                bomb = self.piece.bomb
                # With the `fallen` structure.
                if bomb.check_explosion(
                    target_group=Tetris.entities["fallen"]
                ):
                    Tetris.entities["piece"].empty()
                    self.spawn_next()
                elif j == 17:
                    if self.__bomb_at_bottom:
                        bomb.explode(
                            target_group=Tetris.entities["fallen"]
                        )
                        Tetris.entities["piece"].empty()
                        self.spawn_next()
                    self.__bomb_at_bottom = not self.__bomb_at_bottom

    def spawn_next(self):

        if self.piece.active_shape != "B":  # Normal `piece`
            # Transfer the `piece`'s `Block`s to the `fallen` structure.
            self.fallen.grow()
            # Account for a proper score according to the lines cleared.
            full_lines_number = self.fallen.remove_full_lines()
            self.update_score(full_lines_number)
        
        # Reset height and spawn a new `Piece` object.
        self.piece.height = 18
        self.piece = self.Piece()
        self.piece.preview()
    
    def check_victory(self):
        """
        The game is endless, except for defeat.

        Returns
        -------
        bool
            Whether the game has been beaten."""

        return False
    
    def check_defeat(self):
        """
        Defeat happens if the `fallen` structure reaches the top of the grid.

        Returns
        -------
        bool
            Whether the game was lost.
        """
        
        if self.fallen.height > 20:
            return True
        else:
            return False
    
    class Piece:
        """
        Organizes the four-tiled-piece's mechanics.

        Attributes
        ----------
        direction : str
            Where to move the piece (``"left"``,``"right"``,  or
            ``"down"`` to accelerate the fall).
        stored_shape : str
            A character representing the next `Tetris.Piece`'s shape.
        bomb : Bomb
            A dummy `Bomb` outside the grid.
        """

        direction = ""
        stored_shape = ""
        bomb = Bomb(-5, -5)

        def __init__(self):
            """ Spawn and preview. """

            self.height = 19
            self.lock_switch = False
            self.blocks = {}
            self.next_id = None
            self.coords = None
            self.piece = None

            # Initialize `self.bomb` with a dummy. Effective `Bomb`s
            # will only appear if `USE_BOMBS` is True.
            self.bomb = Tetris.Piece.bomb
            # `Bomb` spawn rate: 5% at every spawn, if activated.
            r, = random.choices((USE_BOMBS, False), cum_weights=(0.05, 1), k=1)
            if r:  # `Bomb`s are treated as `Piece` objects.
                Tetris.entities["piece"].empty()
                self.bomb = Bomb(3, -1, group=Tetris.entities["piece"])
                self.coords = [3, -1]
                self.piece = self.bomb._bombs[-1]
                # Dummy `self.blocks` to use the `Piece` mechanics.
                self.blocks = {1: (1, self.piece)}
                # Dummy `active_shape`.
                self.active_shape = "B"
                # Spawn a `Bomb` piece.
                self.spawn()
                # `Bomb`s cannot be switched.
                self.lock_switch = True
            
            else:  # 95% of the time, though, a normal piece will spawn.
                # If there is any `Tetris.Piece.stored_shape`, store
                # its value into `self.active_shape`.
                if Tetris.Piece.stored_shape:
                    self.active_shape = Tetris.Piece.stored_shape
                else:
                    # Otherwise, choose the value of `active_shape`
                    # randomly.
                    self.active_shape = random.choice(
                        ("T", "J", "L", "S", "Z", "I", "O")
                    )
                # Store a new shape.
                Tetris.Piece.stored_shape = random.choice(
                    ("T", "J", "L", "S", "Z", "I", "O")
                )
                # Spawn a `Piece` object with the `active_shape`.
                self.spawn()
                # Permit one switch between `active_shape` and
                # `stored_shape`.
                self.lock_switch = False
        
        def spawn(self):
            """ Draw the desired piece on the screen, at top center. """

            self.place(self.active_shape, 4, 0)
            # Identify the next rotated position.
            self.next_id, self.piece = self.blocks[1]
            Tetris.entities["piece"].add(*self.piece)
        
        def preview(self):
            """ Showcase a message with `stored_shape` at the Terminal. """

            if Tetris.Piece.stored_shape == "T":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "    _\n",
                    " _ |_| _\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "J":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _\n",
                    "|_| _  _\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "L":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "       _\n",
                    " _  _ |_|\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "S":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "    _  _\n",
                    " _ |_||_|\n",
                    "|_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "Z":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _\n",
                    "|_||_| _\n",
                    "   |_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "I":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _  _  _\n",
                    "|_||_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "O":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _\n",
                    "|_||_|\n",
                    "|_||_|"
                ])
                print(drawing)
        
        def switch(self):
            """
            Mechanics for switching pieces.

            Change a `piece` with `active_shape` to one with
            `stored_shape` (only once for each new spawn).
            """

            # Clear the current `piece`'s drawing and references.
            Tetris.entities["piece"].empty()

            # Switch shapes and reset the `height`.
            s, a = Tetris.Piece.stored_shape, self.active_shape
            Tetris.Piece.stored_shape, self.active_shape = a, s
            self.height = 19

            self.spawn()
            self.preview()
            
            self.lock_switch = True  # Only once for every new `piece`.
        
        def place(self, shape, i, j):
            """
            Positioning of `Block`s to form each shape and track rotation.

            Parameters
            ----------
            shape : str
                A character representing the desired shape.
            i : int
                Horizontal coordinate reference.
            j : int
                Vertical coordinate reference.
            """

            self.coords = (i, j)
            if shape == "T":
                self.blocks = {
                    1: (2, (Block(i-1, j), Block(i, j), Block(i+1, j), Block(i, j-1))),
                    2: (3, (Block(i-1, j), Block(i, j), Block(i, j-1), Block(i, j+1))),
                    3: (4, (Block(i-1, j), Block(i, j), Block(i+1, j), Block(i, j+1))),
                    4: (1, (Block(i, j-1), Block(i, j), Block(i+1, j), Block(i, j+1)))
                }
            elif shape == "J":
                self.blocks = {
                    1: (2, (Block(i-1, j-1), Block(i-1, j), Block(i, j), Block(i+1, j))),
                    2: (3, (Block(i, j-1), Block(i, j), Block(i, j+1), Block(i-1, j+1))),
                    3: (4, (Block(i-1, j-1), Block(i, j-1), Block(i+1, j-1), Block(i+1, j))),
                    4: (1, (Block(i-1, j-1), Block(i, j-1), Block(i-1, j), Block(i-1, j+1)))
                }
            elif shape == "L":
                self.blocks = {
                    1: (2, (Block(i-1, j), Block(i, j), Block(i+1, j), Block(i+1, j-1))),
                    2: (3, (Block(i-1, j-1), Block(i, j-1), Block(i, j), Block(i, j+1))),
                    3: (4, (Block(i-1, j), Block(i-1, j-1), Block(i, j-1), Block(i+1, j-1))),
                    4: (1, (Block(i-1, j-1), Block(i-1, j), Block(i-1, j+1), Block(i, j+1)))
                }
            elif shape == "S":
                self.blocks = {
                    1: (2, (Block(i-1, j), Block(i, j), Block(i, j-1), Block(i+1, j-1))),
                    2: (1, (Block(i, j+1), Block(i, j), Block(i-1, j), Block(i-1, j-1)))
                }
            elif shape == "Z":
                self.blocks = {
                    1: (2, (Block(i-1, j-1), Block(i, j-1), Block(i, j), Block(i+1, j))),
                    2: (1, (Block(i, j-1), Block(i, j), Block(i-1, j), Block(i-1, j+1)))
                }
            elif shape == "I":
                self.blocks = {
                    1: (2, (Block(i-1, j), Block(i, j), Block(i+1, j), Block(i+2, j))),
                    2: (1, (Block(i, j-1), Block(i, j), Block(i, j+1), Block(i, j+2)))
                }
            elif shape == "O":
                self.blocks = {
                    1: (1, (Block(i, j), Block(i, j+1), Block(i+1, j), Block(i+1, j+1)))
                }
        
        def calculate_dimensions(self):
            """
            Track the boundary dimensions of each `Piece`.

            Returns
            -------
            tuple[int, int, int]
                Horizontal and vertical limits.
            """

            try:
                i_min = min(
                    [block.coords[0] for block in Tetris.entities["piece"]]
                )
                i_max = max(
                    [block.coords[0] for block in Tetris.entities["piece"]]
                )
                j_max = max(
                    [block.coords[1] for block in Tetris.entities["piece"]]
                )
                
                # Calculation of `height`:
                heights = []
                for i in range(i_min, i_max+1):
                    # For each horizontal coordinate, ...
                    piece_col = [block.coords[1]
                                 for block in self.piece
                                 if block.coords[0] == i]
                    # choose the `piece`'s lowest vertical coordinate...
                    j = max([0] + piece_col)
                    # and the fallen structure's highest vertical coordinate.
                    fall_col = [block.coords[1]
                                for block in Tetris.entities["fallen"]
                                if block.coords[0] == i
                                and block.coords[1] > j]
                    # If there's anything below the `piece` in this column, ...
                    if fall_col:
                        # add the distance to the list of heights.
                        heights.append(min(fall_col)-j-1)
                    else:
                        # Otherwise, add the distance to the bottom of
                        # the grid to the list.
                        heights.append(19-j)
                # The `height` attribute is the shortest distance from
                # a `piece` to the fallen structure.
                self.height = min(heights)
                return i_min, i_max, j_max
            # In case any calculation fails, return dummy values.
            except ValueError:
                return 10, 10, 20
        
        def move(self, direction):
            """
            Handle the `piece`'s movement.

            direction : str
            Where to move (``"left"``,``"right"``,  or
            ``"down"`` to accelerate the fall).
            """

            # Get all the necessary dimensions to detect whether
            # movement is possible
            a, b = CONVERT[direction]
            i, j = self.coords
            i_min, i_max, j_max = self.calculate_dimensions()
            
            # First, build a set with the desired new positions for
            # each `Block` in the `piece`.
            X = set(
                [(block.coords[0]+a, block.coords[1]+b)
                 for block in self.piece]
            )
            # Second, build a set with the current positions of the
            # already formed structure.
            Y = set(
                [block.coords
                 for block in Tetris.entities["fallen"]]
            )
            # Movement can happen if these sets don't intersect,
            if (X & Y == set()  # or if a `Bomb` moves `"down"`.
                    or self.active_shape == "B" and direction == "down"):
                # Check also if the movement won't get any `Block`
                # outside screen boundaries.
                if 0 <= i_min+a and i_max+a < 10 and j_max+b < 20:
                    # Update the `self.blocks` dict.
                    self.place(self.active_shape, i+a, j+b)
                    # Make the movement.
                    for block in Tetris.entities["piece"]:
                        i, j = block.coords
                        block.set_position(i+a, j+b)
        
        def rotate(self):
            if len(self.blocks[1][1]) == 4:  # Avoids rotating a `Bomb`.
                # First set: desired new positions of the `piece`'s
                # `Block`s if rotation were to happen.
                X = set([block.coords
                         for block in self.blocks[self.next_id][1]])
                # Second set: current positions of `Block`s in the
                # fallen structure.
                Y = set([block.coords
                         for block in Tetris.entities["fallen"]])
                # Third set: positions outside the borders in the
                # rotation.
                Z = set([(i, j)
                         for (i, j) in X
                         if not (0 <= i < 10 and j < 20)])
                # If the rotated `piece` doesn't collide with the
                # structure and remains inside the grid, then movement
                # occurs.
                if X & Y == set() and Z == set():
                    # Erase the current `piece` from the screen.
                    Tetris.entities["piece"].empty()
                    # Replace it with another with the next rotated state.
                    self.place(self.active_shape, *self.coords)
                    # Update the rotating id and draw the `piece`'s
                    # `Block`s.
                    self.next_id, self.piece = self.blocks[self.next_id]
                    Tetris.entities["piece"].add(*self.piece)
        
        def fall_inst(self):
            """ Instant fall, moving down a piece by its full ``height``. """

            i, j = self.coords
            self.calculate_dimensions()  # Get current `height`.
            # Update `blocks`.
            self.place(self.active_shape, i, j+self.height)

            # Move down by `self.height`.
            for block in Tetris.entities["piece"]:
                a, b = block.coords
                block.set_position(a, b+self.height)
    
    class FallenBlocks:
        """ Structure formed by the fallen piece's `Block`s. """

        def __init__(self):
            self.height = 0  # Not the same as `piece.height`.

        def grow(self):
            """ Making a `Piece` part of the structure. """

            # Transfer the `Block`s from the `"piece"` group to the
            # `"fallen"` group.
            if len(Tetris.entities["piece"]) == 4:  # Exclude `Bomb`.
                for block in Tetris.entities["piece"]:
                    block.add(Tetris.entities["fallen"])
            Tetris.entities["piece"].empty()

            # Update the structure's height.
            h = min(
                [20] + [block.coords[1]
                        for block in Tetris.entities["fallen"]]
            )
            self.height = 20 - h

        def remove_full_lines(self):
            full_lines = []
            # Group all the completed lines (with 10 aligned `Block`s)
            # in `full_lines`.
            for b in range(20):
                line = [block
                        for block in Tetris.entities["fallen"]
                        if block.coords[1] == b]
                if len(line) == 10:
                    full_lines.append((b, line))
            # Remove them from the structure and lower the `Block`s
            # above it.
            for b, line in full_lines:
                Tetris.entities["fallen"].remove(*line)
                for block in Tetris.entities["fallen"]:
                    i, j = block.coords
                    if j < b:
                        block.set_position(i, j+1)
            
            return len(full_lines)  # Used for scoring.


class Client(BaseClient):
    """ A client for :class:`Tetris`. """

    def __init__(self):
        """ Initializing the GUI and the game. """

        super().__init__()
        pygame.display.set_caption("Tetris Game")

        self.game = Tetris()

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
