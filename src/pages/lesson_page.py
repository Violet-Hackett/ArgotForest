import pygame
import state

from pygame import Surface
from page import Page
from page_keys import PageKey
import ui
from lesson import Lesson, lessons

JOURNAL_WIDTH = state.ROOT_WIDTH / 3
class LessonPage(Page):
    PAGE_KEY = PageKey.LESSON_PAGE # type: ignore

    def __init__(self, lesson: Lesson):
        self.lesson = lesson
        super().__init__()

    def construct(self):
        exit_button = ui.Button(pygame.Rect(JOURNAL_WIDTH + ui.DEFAULT_BUTTON_HEIGHT, ui.DEFAULT_BUTTON_HEIGHT,
                                            ui.DEFAULT_BUTTON_HEIGHT, ui.DEFAULT_BUTTON_HEIGHT), 
                                            text = "x", id = 'exit_button')
        enter_button = ui.Button(pygame.Rect(state.ROOT_WIDTH - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                             state.ROOT_HEIGHT - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                             ui.DEFAULT_BUTTON_HEIGHT, ui.DEFAULT_BUTTON_HEIGHT), 
                                             text = ">", id = 'enter_button')

        self.ui_elements += [exit_button, enter_button]

    def render(self, root: Surface):
        root.blit(ui.load_texture(f'lesson_thumbnails\\{self.lesson.id}'), (JOURNAL_WIDTH, 0))
        self.render_all_elements(root)

    def _update_page(self):
        if self.get_element('exit_button').released(): # type: ignore
            state.navigate_to(PageKey.SELECTION_PAGE, lessons.index(self.lesson))
        if self.get_element('enter_button').released(): # type: ignore
            print("Enter pressed")