import pygame

from pygame import Surface
from page import Page
from page_keys import PageKey
import ui
from lesson import Lesson, lessons
import state

class SelectionPage(Page):
    PAGE_KEY = PageKey.SELECTION_PAGE # type: ignore

    def __init__(self, selected_lesson_index: int = 0):
        self._selected_lesson_index = selected_lesson_index
        self._selected_lesson = lessons[selected_lesson_index]
        super().__init__()

    def construct(self):

        selection_btn_width = 75
        lesson_selection_button = ui.Button(pygame.Rect(state.ROOT_WIDTH/2 - selection_btn_width /2,
                                                        state.ROOT_HEIGHT - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                                        selection_btn_width, ui.DEFAULT_BUTTON_HEIGHT), 
                                            text = lessons[self._selected_lesson_index].title, 
                                            id = 'lesson_selection_button')

        back_button = ui.Button(pygame.Rect(lesson_selection_button.hitbox.left - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                            state.ROOT_HEIGHT - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                            ui.DEFAULT_BUTTON_HEIGHT, ui.DEFAULT_BUTTON_HEIGHT), "<", 
                                            id = 'back_button')
        foward_button = ui.Button(pygame.Rect(lesson_selection_button.hitbox.right + ui.DEFAULT_BUTTON_HEIGHT, 
                                              state.ROOT_HEIGHT - ui.DEFAULT_BUTTON_HEIGHT*2, 
                                            ui.DEFAULT_BUTTON_HEIGHT, ui.DEFAULT_BUTTON_HEIGHT), ">", 
                                            id = 'foward_button')
        
        self.ui_elements += [lesson_selection_button, back_button, foward_button]

    def render(self, root: Surface):

        # Render lesson thumbnail
        lesson_thumbnail = ui.load_texture(f"lesson_thumbnails\\{self._selected_lesson.id}")
        root.blit(lesson_thumbnail)

        self.render_all_elements(root)

    def _update_page(self):
        if self.get_element('back_button').released(): # type: ignore
            self._select_lesson(self._selected_lesson_index - 1)
        if self.get_element('foward_button').released(): # type: ignore
            self._select_lesson(self._selected_lesson_index + 1)
        if self.get_element('lesson_selection_button').released(): # type: ignore
            state.navigate_to(PageKey.LESSON_PAGE, self._selected_lesson)

    def _select_lesson(self, lesson_index: int):
        """
        Selects the lesson with the given lesson index.

        :type lesson_index: int
        """

        # Constrain lesson index to [0-(num lessons)]
        if lesson_index >= len(lessons):
            lesson_index = 0
        elif lesson_index < 0:
            lesson_index = len(lessons) - 1

        self._selected_lesson_index = lesson_index
        self._selected_lesson = lessons[lesson_index]
        self.get_element('lesson_selection_button').text = self._selected_lesson.title # type: ignore