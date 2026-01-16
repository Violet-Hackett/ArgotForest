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
    pygame.quit()
    sys.exit()

while(state.running):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
            continue
    
    current_page.render(root)

    pygame.display.update()
    fpsClock.tick(state.FPS)

quit()