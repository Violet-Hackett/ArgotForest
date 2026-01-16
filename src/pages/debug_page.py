import pygame

from pygame import Surface
from page import Page
from page_keys import PageKey
import ui

class DebugPage(Page):
    PAGE_KEY = PageKey.DEBUG_PAGE # type: ignore

    def __init__(self):
        super().__init__()

    def construct(self):
        test_button = ui.Button(pygame.Rect(50, 50, 35, 16), text = "Test", id = 'test_button')
        self.ui_elements.append(test_button)

    def render(self, root: Surface):
        root.fill((30, 30, 30))

        self.get_element('test_button').render(root)

    def _update_page(self):
        if self.get_element('test_button').released(): # type: ignore
            print("Test button released")