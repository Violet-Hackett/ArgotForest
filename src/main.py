# External libraries
import pygame
import sys

# Internal libraries
import state
from pages.supported_pages import get_page
from lesson import load_lessons

# Window setup
pygame.init()
fpsClock = pygame.time.Clock()
root = pygame.display.set_mode(state.window_size())
pygame.display.set_caption('Argot Forest')

# Program state setup
load_lessons()
state.current_page = get_page(state.STARTUP_PAGE)()

def quit():
    """
    Quits the program
    """
    state.running = False
    pygame.quit()
    sys.exit()

while(state.running):

    # Check for quit events
    for event in state.get_events():
        if event.type == pygame.QUIT:
            quit()
    if state.key_is_down(pygame.K_ESCAPE):
        quit()
    
    state.current_page.update()

    # Render
    raw_frame = pygame.Surface(state.ROOT_SIZE)
    state.current_page.render(raw_frame)
    pygame.transform.scale_by(raw_frame, state.window_scale, root)

    # Update program state
    pygame.display.update()
    fpsClock.tick(state.FPS)
    state.tick_count += 1

quit()