from abc import ABCMeta, abstractmethod, abstractproperty
import pygame

from page_keys import PageKey
import ui
import state

class Page:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.ui_elements: list[ui.UIElement] = []
        self.construct()

    @property
    def PAGE_KEY(self) -> PageKey:
        raise NotImplementedError
    
    @abstractmethod
    def construct(self):
        """
        Initializes the page's UI elements (and any other components, if applicable).
        """
        raise NotImplementedError
    
    @abstractmethod
    def render(self, root: pygame.Surface):
        """
        Renders the page to the given root surface
        
        :param root: Root surface to render to
        :type root: pygame.Surface
        """
        raise NotImplementedError
    
    def update(self):
        """
        Updates the page and any contained UI elements (should be called once per tick).
        """
        self._update_ui_elements()
        self._update_page()
    
    def _update_ui_elements(self):
        """
        Updates all contained UI elements
        
        :param self: Description
        """
        for ui_element in self.ui_elements:
            ui_element.update()

    @abstractmethod
    def _update_page(self):
        """
        Updates any non-ui page components
        """
        raise NotImplementedError
    
    def render_all_elements(self, root: pygame.Surface):
        """
        Renders all contained ui elements to the given root surface.
        
        :type root: pygame.Surface
        """
        for ui_element in self.ui_elements:
            ui_element.render(root)
    
    def get_element(self, id: str) -> ui.UIElement:
        """
        Gets the contained ui element matching given id.
        
        :param id: The ui element's id
        :type id: str
        :return: The matching ui element
        :rtype: UIElement
        """
        for ui_element in self.ui_elements:
            if ui_element.id == id:
                return ui_element
        raise IndexError(f"No element found in {self.PAGE_KEY.name} with id \'{id}\'")