import pygame

from page_keys import PageKey

# Program state variables
running: bool = True
STARTUP_PAGE: PageKey = PageKey.DEBUG_PAGE
FPS = 60
tick_count: int = 0

_events_last_updated_tick: int = 0
_events: list[pygame.Event] = []
def get_events() -> list[pygame.Event]:
    """
    Returns the current pygame events, drawing from the _events buffer if called more
    than once in the same tick
    """
    global _events_last_updated_tick
    global _events
    if(_events_last_updated_tick != tick_count):
        _events = pygame.event.get()
        _events_last_updated_tick = tick_count
    return _events

def key_is_down(key: int) -> bool:
    """
    Returns whether a key is currently pressed
    
    :rtype: list[int]
    """
    for event in get_events():
        if event.type == pygame.KEYDOWN and event.key == key:
            return True
    return False

# Window & root variables and helpers
ROOT_SIZE: tuple[int, int] = (300, 200)
ROOT_WIDTH, ROOT_HEIGHT = ROOT_SIZE
window_scale: int = 2

def window_size() -> tuple[int, int]:
    """
    The current window size, based on the current root size and window scale.
    
    :return: Current window size
    :rtype: tuple[float, float]
    """
    return tuple([n * window_scale for n in ROOT_SIZE]) # type: ignore

def window_width() -> int:
    """
    The current window width
    
    :return: The current window width
    :rtype: int
    """
    return window_size()[0]

def window_height() -> int:
    """
    The current window height
    
    :return: The current window height
    :rtype: int
    """
    return window_size()[1]

