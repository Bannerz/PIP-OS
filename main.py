import pygame
import sys
import subprocess
from modules.ui_elements.header import Header
from modules.ui_elements.footer import Footer
from screen_manager import ScreenManager

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pygame Header and Footer Example')

# User's birthday (YYYY-MM-DD)
birthday = "1997-02-08"

# Create instance of Header and Footer
header_height = 40
footer_height = 20
gap = 2  # Gap between the map and header/footer

# Calculate content height with gaps
content_height = SCREEN_HEIGHT - header_height - footer_height - 2 * gap
content_width = SCREEN_WIDTH

header = Header(SCREEN_WIDTH, header_height)
footer = Footer(SCREEN_WIDTH, footer_height, birthday)

mapbox_api_key = "pk.eyJ1IjoiYmFubmVyeiIsImEiOiJjbHd6aHo4MHkwN2U2MmpxcGQ3M2w5eWd5In0.iSjrMliSYCJbQZl_dsyERQ"

audio_dir = "modules/radio/sounds"

# Create instance of ScreenManager
screen_manager = ScreenManager(SCREEN_WIDTH, content_height, mapbox_api_key, audio_dir)

# Define screen pages
PAGES = ["STAT", "INV", "DATA", "MAP", "RADIO"]

# Main loop
running = True
current_page = 0  # Set to STAT page for now

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                current_page = 0
                screen_manager.set_active_screen('screen1')
            elif event.key == pygame.K_F2:
                current_page = 1
                screen_manager.set_active_screen('screen2')
            elif event.key == pygame.K_F3:
                current_page = 2
                screen_manager.set_active_screen('screen3')
            elif event.key == pygame.K_F4:
                current_page = 3
                screen_manager.set_active_screen('screen4')
                screen_manager.screens['screen4'].fetch_map(screen_manager.screens['screen4'].latitude, screen_manager.screens['screen4'].longitude)
            elif event.key == pygame.K_F5:
                current_page = 4
                screen_manager.set_active_screen('screen5')
            header.set_selected_index(current_page)

        # Handle events for the active screen
        screen_manager.active_screen.handle_event(event)

    # Fill the background
    screen.fill((0, 0, 0))  # Black background

    # Draw header and footer
    header.draw(screen)
    footer.draw(screen, "inventory" if current_page == 1 else "default")

    # Draw the active screen with gaps
    content_surface = screen.subsurface((0, header_height + gap, content_width, content_height))
    screen_manager.draw(content_surface)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()