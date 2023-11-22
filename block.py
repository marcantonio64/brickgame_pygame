""" Establishing the structure, appearance, and behavior of unit cells. """

import pygame
from .constants import *

__all__ = ["Block", "BlinkingBlock", "Bomb"]


class Block(pygame.sprite.Sprite):
    """ Unitary cell, colored black when active. """

    def __init__(self, i, j, color=LINE_COLOR, direction=""):
        """
        Constructor for :class:`Block` instances.

        Set instance variables, access the active ``surface``,
        and draw squares on it.

        Parameters
        ----------
        i : int
            Horizontal position on the grid.
        j : int
            Vertical position on the grid.
        color : str, optional
            Color value. Defaults to ``LINE_VALUE`` (std. black).
        direction : str, optional
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        self.displacement = (0, 0)
        """        
        A 2D-vector of integers.

        Represents the real displacement a :class:`Block` will suffer in
        the next update. It depends on the current game's resolution.
        """
        self.coords = (i, j)
        self._color = color
        self._direction = direction

        # Initialize the `Sprite`.
        super().__init__()
        # Create an `image` surface and draw on it.
        self.image = pygame.Surface((BLOCK_SIDE, BLOCK_SIDE))
        self.image.fill(BACK_COLOR)
        self.draw(self.image)
        # Extract its `rect` container.
        self.rect = self.image.get_rect()
        # Place it according to i and j.
        self.set_position(i, j)
        self.set_direction(self._direction)
    
    def update(self, t=0, speed=0):
        """
        Update the inner :class:`Block` mechanics.

        Parameters
        ----------
        t : int, optional
            A timer. Defaults to 0.
        speed : int, optional
            Number of moves per second. Defaults to 0.
        """

        # The `Block` moves only when a direction and a positive speed
        # are specified.
        if self._direction and speed > 0:
            if t % int(FPS/speed) == 0:  # `speed` actions per second.
                # Move in place by `displacement`.
                self.rect.move_ip(self.displacement)
                # Adjust the coordinates.
                i, j = self.coords
                a, b = self.displacement
                a /= DIST_BLOCKS
                b /= DIST_BLOCKS
                self.coords = (i+int(a), j+int(b))
    
    def draw(self, surface):
        """
        Draw squares at ``surface``.

        Parameters
        ----------
        surface : pygame.Surface
            Environment to draw on.
        """

        # Outer square
        side = PIXEL_SIDE*10
        square = pygame.Rect(0, 0, side, side)
        pygame.draw.rect(surface, self._color, square, PIXEL_SIDE)

        # Inner square
        dist = 2*PIXEL_SIDE
        side = 6*PIXEL_SIDE
        square = pygame.Rect(dist, dist, side, side)
        pygame.draw.rect(surface, self._color, square)

        # Update ``surface``.
        surface.blit(surface, (0, 0))
    
    def set_position(self, i, j):
        """
        Move :class:`Block` to the specified position.

        Parameters
        ----------
        i : int
            New horizontal position on the grid.
        j : int
            New vertical position on the grid.
        """

        # Convert grid coordinates into positional pixels
        self.coords = (i, j)
        x = int(BORDER_WIDTH + i*DIST_BLOCKS)
        y = int(BORDER_WIDTH + j*DIST_BLOCKS)
        self.rect.topleft = (x, y)  # Placement.
    
    def set_direction(self, direction):
        """
        Update the ``displacement`` attribute to move the :class:`Block`
        according to the ``direction`` parameter.

        Parameters
        ----------
        direction : str
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        if direction:
            self._direction = direction
            i, j = CONVERT[direction]
            x = i*DIST_BLOCKS
            y = j*DIST_BLOCKS
            self.displacement = (x, y)


class BlinkingBlock(Block):
    """ Just a :class:`Block` sprite which ``image`` attribute blinks. """
    
    def __init__(self, i, j):
        """
        Constructor for :class:`BlinkingBlock` instances.

        Draw a normal `_image` and a `_blank`, over which `image` will
        alternate over time (twice per second).

        Parameters
        ----------
        i : int
            Horizontal position on the grid.
        j : int
            Vertical position on the grid.
        """

        super().__init__(i, j)
        # Store the active `image` into `_image`.
        self._image = self.image
        # Draw a shaded `blank` image.
        self._blank = Block(i, j, color=SHADE_COLOR).image
    
    def update(self, t=0, **kwargs):
        """
        Update the inner :class:`BlinkingBlock` mechanics.

        Since the method `pygame.sprite.Group.draw()` 'blits' the
        sprites' `.image` attribute to the surface, we need to
        alternate what is drawn to `self.image`.

        Parameters
        ----------
        t : int, optional
            A timer. Defaults to 0.
        """

        if t > 0:
            if t % FPS == 0:
                self.image = self._image  # Active.
            elif t % FPS == int(FPS/2):
                self.image = self._blank  # Not active.


class Bomb:
    """
    Used to destroy blocks from a target upon collision.

    Made with a group of :class:`Block` and :class:`BlinkingBlock`
    objects in an *X* shape, akin to a sea mine.
    """

    _bombs = []  # List of active `Bomb`s, shared within the objects.

    def __init__(self, i, j, group=None):
        """
        Constructor for :class:`Bomb` instances.

        Instantiate the required :class:`Block` and :class:`BlinkingBlock`
        objects and organize them according to ``group``.

        Parameters
        ----------
        i : int
            Horizontal position of the top left corner.
        j : int
            Vertical position of the top left corner.
        group : pygame.sprite.Group, optional
            A `Group` object to collect :class:`Bomb`'s elements.
            Defaults to ``None``.
        """

        # `Bomb` construction:
        if group is not None:
            bomb = [BlinkingBlock(i, j),    # 4 outer corners.
                    BlinkingBlock(i, j+3),
                    BlinkingBlock(i+3, j),
                    BlinkingBlock(i+3, j+3),
                    Block(i+1, j+1),        # 4 core `Block`s.
                    Block(i+1, j+2),
                    Block(i+2, j+1),
                    Block(i+2, j+2),
                    Block(i, j+1, color=SHADE_COLOR),  # Fill spaces.
                    Block(i, j+2, color=SHADE_COLOR),
                    Block(i+3, j+1, color=SHADE_COLOR),
                    Block(i+3, j+2, color=SHADE_COLOR),
                    Block(i+1, j, color=SHADE_COLOR),
                    Block(i+2, j, color=SHADE_COLOR),
                    Block(i+1, j+3, color=SHADE_COLOR),
                    Block(i+2, j+3, color=SHADE_COLOR),
                    ]
            # Add `bomb`'s components to `group` for drawing.
            group.add(*bomb)
            # Add ``bomb`` to `Bomb._bombs` for iteration.
            Bomb._bombs.append(bomb)
    
    def move(self, direction):
        """
        Handle :class:`Bomb` movement.

        Parameters
        ----------
        direction : str
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        a, b = CONVERT[direction]
        for bomb in Bomb._bombs[::-1]:
            # Move each component using `.set_position()`.
            for block in bomb:
                i, j = block.coords
                block.set_position(i+a, j+b)
            
            # Delete a `Bomb` when it exits the grid.
            _, k = bomb[0].coords
            if (direction == "up" and k < 0  # At the top.
                    or direction == "down" and k >= 17):  # At the bottom.
                for block in bomb:
                    # Erase the drawings.
                    block.kill()
                # Remove references.
                Bomb._bombs.remove(bomb)
    
    def check_explosion(self, target_group):
        """
        Manage collision detection.

        Parameters
        ----------
        target_group : pygame.sprite.Group
            A `Group` object indicating objects to be destroyed.

        Returns
        -------
        bool
            Whether any explosion happened.
        """

        _erase = False
        # Iterate through `Bomb._bombs` reversely, keeping track of the
        # indexes for deletions.
        for index, bomb in list(enumerate(Bomb._bombs))[::-1]:
            i, j = bomb[0].coords
            erase = False
            # Detect explosion.
            for block in target_group:
                a, b = block.coords
                if (i <= a <= i+3) and (j <= b <= j+3):
                    # Stop if any component of `target` reaches `Bomb`.
                    erase = True
                    _erase = True
            if erase:  # If any explosion happened.
                self.explode(target_group, index=index)
        return _erase

    def explode(self, target_group, index=-1):
        """
        Destroy `target` and the indexed `Bomb`.

        Parameters
        ----------.
        target_group : pygame.sprite.Group
            A `Group` object indicating objects to be destroyed.
        nindex : int, optional
            The index of an exploding `Bomb` in `bombs`. Defaults to -1.
        """

        bomb = Bomb._bombs[index]
        i, j = bomb[0].coords
        # Destroy `target`.
        for target in target_group:
            a, b = target.coords
            # Blast range of 2 `Blocks` from the `Bomb`'s edges.
            if (i-2 <= a <= i+5) and (j-2 <= b <= j+5):
                target.kill()  # Erase the drawings.
        # Destroy `bomb`.
        for block in bomb:
            block.kill()  # Erase the drawings.
        del Bomb._bombs[index]  # Remove references.
