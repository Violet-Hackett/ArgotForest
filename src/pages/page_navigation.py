import state
from pages.supported_pages import PageKey, get_page

def navigate_to(page_key: PageKey, *page_args):
        """
        Navigate to a new page with the corresponding page key

        :type page_key: PageKey
        """
        state.current_page = get_page(page_key)(*page_args)