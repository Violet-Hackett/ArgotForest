from page import Page
from page_keys import PageKey

from pages.debug_page import DebugPage
from pages.selection_page import SelectionPage
import state

SUPPORTED_PAGES: list[type[Page]] = [
    DebugPage,
    SelectionPage
]

def get_page(page_key: PageKey) -> type[Page]:
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