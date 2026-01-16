from pygame import Surface
from page import Page
from page_keys import PageKey

class DebugPage(Page):
    PAGE_KEY = PageKey.DEBUG_PAGE # type: ignore

    def render(self, root: Surface):
        root.fill((30, 30, 30))