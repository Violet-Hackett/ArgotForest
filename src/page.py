from abc import ABCMeta, abstractmethod, abstractproperty
import pygame

from page_keys import PageKey

class Page:
    __metaclass__ = ABCMeta

    @property
    def PAGE_KEY(self) -> PageKey:
        raise NotImplementedError
    
    @abstractmethod
    def render(self, root: pygame.Surface):
        """
        Renders the page to the given root surface
        
        :param root: Root surface to render to
        :type root: pygame.Surface
        """
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        """
        Updates the page
        """
        raise NotImplementedError