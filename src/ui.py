import pygame
from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum

import state

class UIElement:

    def __init__(self, id: str|None = None):
        self.id = id

    @abstractmethod
    def render(self, root: pygame.Surface):
        """
        Renders the UI Element onto the given root surface.
        
        :type root: pygame.Surface
        """
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        """
        Updates the UI Element (should be called once per tick).
        """
        raise NotImplementedError
    
class ButtonState(Enum):
    IDLE = 0
    HOVERED = 1
    PRESSED = 2

class Button(UIElement):
    def __init__(self, hitbox: pygame.Rect, id: str|None = None):
        super().__init__(id)
        self.hitbox = hitbox
        self.state: ButtonState = ButtonState.IDLE
        self._previous_state: ButtonState = ButtonState.IDLE

    def render(self, root: pygame.Surface):

        debug_color = pygame.Color(255, 50, 50)
        if self.state == ButtonState.HOVERED:
            debug_color = pygame.Color(50, 50, 255)
        elif self.state == ButtonState.PRESSED:
            debug_color = pygame.Color(50, 255, 50)

        pygame.draw.rect(root, debug_color, self.hitbox)

    def update(self):

        self._previous_state = self.state
        
        if self.hitbox.collidepoint(*state.root_mouse_position()):
            if any(pygame.mouse.get_pressed()):
                self.state = ButtonState.PRESSED
            else:
                self.state = ButtonState.HOVERED
        else:
            self.state = ButtonState.IDLE

    def released(self) -> bool:
        """
        Whether the button is currently being released on the current tick
        
        :param self: Description
        :return: Description
        :rtype: bool
        """
        return self.state != ButtonState.PRESSED and self._previous_state == ButtonState.PRESSED