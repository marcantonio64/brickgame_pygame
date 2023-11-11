""" This module contains a base class with general game mechanics. """

import json
import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from ..client import high_scores_dir
from ..screen_generator import Background, VictoryScreen, DefeatScreen

__all__ = ["Game"]


class Game(ABC):
    """
    Engine for pixel games in a 10x20 grid.

    Attributes
    ----------
    entities : dict
        Container for all `Block` objects and derivatives.
    """

    # Class variables, shared with instances and nested classes.
    entities = None
    
    def __init__(self):
        """ Set instance variables and load background. """

        self.score = 0
        self.highest_score = 0
        self.speed = 1  # Unit cells per second.
        self.paused = False
        self.running = True
        """ Whether this game is active. """
        self.name = self.__class__.__name__
        # Access the current surface.
        self.screen = pygame.display.get_surface()

        # Draw the background.
        Background()
    
    def reset(self):
        """ Removes all elements from the screen and start again. """

        self.running = True
        # Clean the groups.
        for entity in self.entities.values():
            entity.empty()
        # Start again.
        self.__init__()
    
    @abstractmethod
    def handle_events(self, key, state):
        """
        Deal with user input during a game.

        Parameters
        ----------
        key : int
            A key id.
        state : int
            ``KEYDOWN`` or ``KEYUP``.
        """
        
        # Setting *P* for pause/unpause and *Return* for reset
        if state == KEYDOWN:
            if key == K_p:
                self.paused = not self.paused
                if self.paused:
                    print("Game paused")
                else:
                    print("Game unpaused")
            elif key == K_RETURN:
                self.reset()
            ...
    
    @abstractmethod
    def manage(self, *args):
        """ Game logic implementation. """

        if self.running and not self.paused:
            if self.check_victory():
                self.toggle_victory()
                print("Congratulations!")
                print("Your score on", self.name, ":", self.score)
            if self.check_defeat():
                self.toggle_defeat()
                print("Better luck next time...")
                print("Your score on", self.name, ":", self.score)
    
    @abstractmethod
    def update_score(self, *args):
        """ Communicate with the `high-scores.json` file. """

        # Read the highest score for the current game.
        try:
            with open(high_scores_dir, "r") as file:
                high_scores = json.load(file)
                self.highest_score = high_scores[self.name]
        except Exception as e:
            print(e)
            print("Failed to read 'high-scores.json'.")
            pass  # This interrupts the scoring system without stopping the game.
        
        # Update the highest score to the .json file.
        if self.score > self.highest_score:
            if self.score >= 10**8:
                self.score = 10**8 - 1  # Max value
            else:
                self.highest_score = self.score
            try:
                with open(high_scores_dir, "w") as file:
                    high_scores[self.name] = self.highest_score
                    json.dump(high_scores, file)
            except Exception as e:
                print(e)
                # print("Failed to update 'high-scores.json'.")
    
    @abstractmethod
    def check_victory(self):
        return False
    
    @abstractmethod
    def check_defeat(self):
        return False
    
    def toggle_victory(self):
        """ Removes all elements from the screen and show victory_screen. """

        self.running = False
        # Clean the groups.
        for entity in self.entities.values():
            entity.empty()
        # Show the victory message.
        VictoryScreen()
    
    def toggle_defeat(self):
        """ Removes all elements from the screen and show defeat_screen. """

        self.running = False
        # Clean the groups.
        for entity in self.entities.values():
            entity.empty()
        # Show the defeat message.
        DefeatScreen()
    
    def update_entities(self, **kwargs):
        """ Update `Block`'s mechanics. """

        if not self.paused:
            for entity in self.entities.values():
                entity.update(speed=self.speed, **kwargs)
    
    def draw_entities(self):
        """ Draw all the sprites to the screen. """

        if self.running:
            # Draw the background (clear previous drawings).
            Background()
            # Draw the current objects to the screen.
            for entity in self.entities.values():
                entity.draw(self.screen)
