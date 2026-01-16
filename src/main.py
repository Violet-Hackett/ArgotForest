# External libraries
import pygame
import sys

# Internal libraries
import state
from pages.supported_pages import get_page

# Window setup
pygame.init()
fpsClock = pygame.time.Clock()
root = pygame.display.set_mode(state.window_size())
pygame.display.set_caption('Argot Forest')

# Program state setup
current_page = get_page(state.STARTUP_PAGE)()

def quit():
    state.running = False
    pygame.quit()
    sys.exit()

while(state.running):

    for event in state.get_events():
        if event.type == pygame.QUIT:
            quit()
    if state.key_is_down(pygame.K_ESCAPE):
        quit()
    
    #current_page.update()
    current_page.render(root)

    pygame.display.update()
    fpsClock.tick(state.FPS)
    state.tick_count += 1

quit()