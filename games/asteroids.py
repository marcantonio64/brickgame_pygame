""" This module contains an implementation of an Asteroids game. """

import random
import pygame
from pygame.locals import *
from ..constants import *
from ..client import BaseClient
from ..block import Block, Bomb
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Asteroids"]

USE_BOMBS = True


class Asteroids(Game):
    """
    Implements `Game` with an Asteroids game.

    Attributes
    ----------
    shooter_speed : int
        Number of bullets per second.
    entities : dict
        Containers for the objects to be drawn (name:group).
    """

    shooter_speed = 10
    entities = {"asteroids": pygame.sprite.RenderPlain(),
                "bullet":    pygame.sprite.RenderPlain(),
                "shooter":   pygame.sprite.RenderPlain(),
                "bomb":      pygame.sprite.RenderPlain()}
    
    def __init__(self):

        super().__init__()
        self.asteroids_speed = 2  # Falling speed.
        self.speed = self.asteroids_speed
        self.game_ticks = 0  # Internal timer for the game.

        # Spawn the entities.
        self.shooter = self.Shooter()  # Also spawns the bullets.
        # Initialize `self.bomb` with a dummy `Bomb` outside the grid.
        self.bomb = Bomb(-5, -5)

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
                # Set `Shooter`'s movement.
                if key == K_LEFT:
                    self.Shooter.direction = "left"
                elif key == K_RIGHT:
                    self.Shooter.direction = "right"

            if state == KEYUP:  # Key released.
                if key == K_LEFT:
                    self.Shooter.direction = ""
                elif key == K_RIGHT:
                    self.Shooter.direction = ""
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            # Separate from the :class:`Client`'s timer to allow for proper
            # scaling of difficulty.
            self.game_ticks += 1

            # Manage multiple simultaneous hits and scoring.
            collisions = self.check_hit()
            self.update_score(len(collisions))

            # Set the events with an action rate of `asteroids_speed`
            # `Block`s per second.
            if t % int(FPS/self.asteroids_speed) == 0:
                self.move_asteroids(self.game_ticks)
                self.bomb.move("up")
                self.bomb.check_explosion(
                    target_group=Asteroids.entities["asteroids"]
                )

            # Set the events with an action rate of `shooter_speed`
            # `Block`s per second.
            if t % int(FPS/self.shooter_speed) == 0:
                # The `Bullet`'s movement is handled by its `update`
                # method.
                self.shooter.shoot()
                self.shooter.move()
                self.try_spawn_bomb(self.game_ticks)
        
        super().manage()  # Manage endgame.

    def check_hit(self):
        """
        Bullets disappear and destroy asteroids on collision.

        Returns
        -------
        dict
            A mapping with all the collisions.
        """

        asteroids = self.entities["asteroids"]
        bullet = self.entities["bullet"]
        # A collision happens if the sprites overlap.
        collisions = pygame.sprite.groupcollide(
            asteroids,
            bullet,
            dokilla=True,  # Destroy asteroids.
            dokillb=True,  # Destroy bullet.
        )
        return collisions

    def update_score(self, blocks_hit):
        """ Scoring mechanics. """

        self.score += 5*blocks_hit
        super().update_score()

    def try_spawn_bomb(self, t):
        """
        Handle the `Bomb`'s spawn over time according to its spawn rate.

        Parameters
        ----------
        t : int
            The timer.
        """

        # The chance of a `Bomb` spawning increases from 0.1% up to
        # 0.15% after 3 minutes.
        spawn_rate = 1/3000
        if t <= 180*FPS and t % 60*FPS == 0:
            spawn_rate += 1/6000
        (spawning,) = random.choices(
            (USE_BOMBS, False),  # No spawns if `USE_BOMBS` is False.
            (spawn_rate, 1-spawn_rate),
        )
        # It shall spawn at the bottom of the grid with a random
        # horizontal coordinate.
        if spawning:
            i = random.randint(0, 6)
            self.bomb = Bomb(i, 19, group=self.entities["bomb"])
    
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
        Defeat condition.

        Occurs when an ``aster`` `Block` reaches either the ``shooter``
        or the lower border of the grid.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        asteroids = self.entities["asteroids"]
        shooter = self.entities["shooter"]
        # Check for collisions with the `shooter`.
        collision = pygame.sprite.groupcollide(asteroids, shooter, 0, 0)
        # Track the asteroids' height.
        distance = max([1] + [asteroid.coords[1] for asteroid in asteroids])
        
        if collision:
            return True
        elif distance >= 20:  # Hitting the bottom.
            return True
        else:
            return False

    def move_asteroids(self, t):
        """
        Organizes the asteroids to be destroyed.

        Manages the spawning and the drawing of the asteroid `Block`s,
        as well as their movement.

        Parameters
        ----------
        t : int
            The timer.
        """

        for asteroid in Asteroids.entities["asteroids"]:
            i, j = asteroid.coords
            asteroid.set_position(i, j + 1)

        # Spawn rate starts at 0.3 per tick, increasing linearly up to
        # 0.45 per tick after 3 minutes. (0.5+ is unbeatable.)
        if t < 180 * FPS:
            r = 0.3 + t * 0.15 / (180 * FPS)
        else:
            r = 0.45
        choices = random.choices((1, 0), (r, 1 - r), k=10)
        for i, choice in enumerate(choices):
            if choice:
                Asteroids.entities["asteroids"].add(Block(i, 0))

    class Bullet(Block):
        """ A `Block` sprite that moves up. """

        def __init__(self, i, j):
            super().__init__(i, j, direction="up")
            Asteroids.entities["bullet"].add(self)
        
        def update(self, speed, **kwargs):
            """
            Adapt the `Block.update` method for `Bullet`.

            Parameters
            ----------
            speed : int
                A placeholder for the standard parameters, meant
                to be overridden with ``FPS``.
            """

            # The bullet disappears if it hits the top border.
            if self.coords[1] < 0:
                self.kill()
            # And moves at the update rate speed.
            super().update(speed=FPS, **kwargs)
            
    class Shooter(Block):
        """
        Manages the player-controlled shooter.

        A `Block` sprite moving horizontally at the bottom of the grid
        that can shoot `Bullet`s.

        Attributes
        ----------
        direction : str
            Where to move: ``"left"`` or ``"right"``.
        """

        direction = ""
        
        def __init__(self):
            """ Set `Shooter`'s initial position """

            super().__init__(4, 19)
            Asteroids.entities["shooter"].add(self)
        
        def move(self):
            """ Avoid the shooter from leaving the grid. """

            i, j = self.coords
            a, _ = CONVERT[Asteroids.Shooter.direction]
            if 0 <= i+a < 10:
                self.set_position(i+a, j)
        
        def shoot(self):
            """ Spawn the `Bullet` from the `Shooter`. """

            Asteroids.Bullet(*self.coords)
        
        def update(self, speed, **kwargs):
            """
            Adapt the `Block.update` method for `Shooter`.

            Parameters
            ----------
            speed : int
                A placeholder for the standard parameters, meant
                to be overridden with ``Asteroids.shooter_speed``.
            """

            super().update(speed=Asteroids.shooter_speed, **kwargs)


class Client(BaseClient):
    """ A client for :class:`Asteroids`. """

    def __init__(self):
        """ Initializing the GUI and the game. """

        super().__init__()
        pygame.display.set_caption("Asteroids Game")

        self.game = Asteroids()

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
