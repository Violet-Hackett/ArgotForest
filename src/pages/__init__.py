from typing import Type

from pages.debug_page import DebugPage
from pages.selection_page import SelectionPage
from pages.lesson_page import LessonPage
import state

# Initialize the state's supported page list
state.SUPPORTED_PAGES = [
    DebugPage,
    SelectionPage,
    LessonPage
]