import pygame
import sys
from pathlib import Path

from page_keys import PageKey

# Program state variables
running: bool = True
STARTUP_PAGE: PageKey = PageKey.SELECTION_PAGE
FPS = 60
tick_count: int = 0
current_page = None
TARGET_LANGUAGE_NAME: str = "Russian"
TARGET_LANGUAGE = None

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

# Page navigation
SUPPORTED_PAGES: list[type] = []

def get_page(page_key: PageKey) -> type:
    """
    Finds and returns the page type of the assosiated page key
    
    :param page_key: The assosiated page key
    :type page_key: PageKey
    :return: The assosiated page type
    :rtype: type[Page]
    """
    for _page in SUPPORTED_PAGES:
        if _page.PAGE_KEY == page_key:
            return _page
    raise IndexError(f"No page found with page key \'{page_key}\'")

def navigate_to(page_key: PageKey, *page_args):
        """
        Navigate to a new page with the corresponding page key

        :type page_key: PageKey
        """
        global current_page
        current_page = get_page(page_key)(*page_args)

# Filepaths
def get_base_path() -> Path:
    """
    Gets the absolute file path to the ArgotForest folder
    
    :rtype: Path
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

ARGOT_JUNGLE_FP = get_base_path()
BIN_FP = f"{ARGOT_JUNGLE_FP}\\bin"
FONTS_FP = f"{BIN_FP}\\fonts"
LANGUAGES_FP = f"{BIN_FP}\\languages"
LESSONS_FP = f"{BIN_FP}\\lessons"
TEXTURES_FP = f"{BIN_FP}\\textures"

# Window & root variables and helpers
ROOT_SIZE: tuple[int, int] = (700, 450)
ROOT_WIDTH, ROOT_HEIGHT = ROOT_SIZE
window_scale: float = 1.5

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

def root_mouse_position() -> tuple[int, int]:
    """
    Calculates the relative mouse position mapped onto the root surface.
    
    :rtype: tuple[int, int]
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return (int(mouse_x / window_scale), int(mouse_y / window_scale))