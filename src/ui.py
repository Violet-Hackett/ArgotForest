import pygame
from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum

import state

def load_texture(texture_name: str) -> pygame.Surface:
    """
    Loads and returns the png texture by the given texture name within the textures folder.
    
    :param texture_name: The texture name, (eg. 'circle' for textures/circle.png)
    :type texture_name: str
    :rtype: Surface
    """
    return pygame.image.load(f"{state.TEXTURES_FP}\\{texture_name}.png")

pygame.font.init()
DEFAULT_TEXT_SIZE = 16
DEFAULT_FONT = pygame.Font(f"{state.FONTS_FP}\\Tiny5\\Tiny5.ttf", DEFAULT_TEXT_SIZE)
DEFAULT_TEXT_COLOR = pygame.Color(16, 32, 17)
def render_text(text: str, color: pygame.Color = DEFAULT_TEXT_COLOR):
    """
    Renders text and returns the surface.
    
    :type text: str
    :rtype: Surface
    """
    return DEFAULT_FONT.render(text, False, color)

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

DEFAULT_BUTTON_HEIGHT = 20
DEFAULT_BUTTON_COLOR = pygame.Color(145, 182, 146)
HOVERED_BUTTON_COLOR_LIGHTENING = 5.0
PRESSED_BUTTON_COLOR_LIGHTENING = -5.0
class Button(UIElement):
    def __init__(self, hitbox: pygame.Rect, text: str|None = None, base_color: pygame.Color = DEFAULT_BUTTON_COLOR,
                 id: str|None = None):
        super().__init__(id)

        self.hitbox = hitbox
        self.text = text
        self.base_color = base_color

        self._texture: pygame.Surface = self._construct_button_texture()
        self.state: ButtonState = ButtonState.IDLE
        self._previous_state: ButtonState = ButtonState.IDLE

    def render(self, root: pygame.Surface):

        # Recolor button texture to match the button state
        color = self.base_color
        if self.state == ButtonState.HOVERED:
            color = self._hovered_color()
        elif self.state == ButtonState.PRESSED:
            color = self._pressed_color()

        recolored_texture = self._texture.copy()
        recolored_texture.fill(color, special_flags=pygame.BLEND_ADD)

        # Render text
        if self.text != None:
            text_texture = render_text(self.text)
            centered_text_position = [self.hitbox.size[d]/2 - text_texture.size[d]/2 for d in (0, 1)]
            recolored_texture.blit(text_texture, centered_text_position)

        root.blit(recolored_texture, self.hitbox.topleft)

    def _construct_button_texture(self) -> pygame.Surface:
        """
        Constructs and returns the button's texture.
        
        :rtype: Surface
        """
        texture = pygame.Surface(self.hitbox.size, pygame.SRCALPHA)
        
        # Load corner textures
        top_left = load_texture('button\\top_left')
        top_right = load_texture('button\\top_right')
        bottom_left = load_texture('button\\bottom_left')
        bottom_right = load_texture('button\\bottom_right')

        # Load edge & center textures
        top = load_texture('button\\top')
        bottom = load_texture('button\\bottom')
        left = load_texture('button\\left')
        right = load_texture('button\\right')
        center = load_texture('button\\center')
        edge_size = top.height

        # Scale and blit button component textures
        texture.blit(top_left, (0, 0))
        texture.blit(top_right, (texture.width - edge_size, 0))
        texture.blit(bottom_left, (0, texture.height - edge_size))
        texture.blit(bottom_right, (texture.width - edge_size, texture.height - edge_size))

        texture.blit(pygame.transform.scale_by(top, (self.hitbox.width - edge_size*2, 1)), (edge_size, 0))
        texture.blit(pygame.transform.scale_by(bottom, (self.hitbox.width - edge_size*2, 1)), 
                  (edge_size, texture.height - edge_size))
        texture.blit(pygame.transform.scale_by(left, (1, self.hitbox.height - edge_size*2)), (0, edge_size))
        texture.blit(pygame.transform.scale_by(right, (1, self.hitbox.height - edge_size*2)), 
                  (texture.width - edge_size, edge_size))
        
        texture.blit(pygame.transform.scale_by(center, (self.hitbox.width - edge_size*2, 
                                                     self.hitbox.height - edge_size*2)), 
                                                     (edge_size, edge_size))
        
        return texture
    
    def _hovered_color(self) -> pygame.Color:
        """
        Returns a lightened version of the button's base color
        
        :rtype: Color
        """
        h, s, l, a = self.base_color.hsla
        return pygame.Color.from_hsla(h, s, max(0.0, min(100.0, l + HOVERED_BUTTON_COLOR_LIGHTENING)), a)
    
    def _pressed_color(self) -> pygame.Color:
        """
        Returns a darkened version of the button's base color
        
        :rtype: Color
        """
        h, s, l, a = self.base_color.hsla
        return pygame.Color.from_hsla(h, s, max(0.0, min(100.0, l + PRESSED_BUTTON_COLOR_LIGHTENING)), a)

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