import pygame
import sys
from modules.ui_elements.header import Header
from modules.ui_elements.footer import Footer
from screen_manager import ScreenManager
from modules.stat.stat_screen import StatPage
from modules.inv.inv_screen import Screen2

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
header = Header(SCREEN_WIDTH, header_height)
footer = Footer(SCREEN_WIDTH, footer_height, birthday)

# Create instance of ScreenManager
content_height = SCREEN_HEIGHT - header_height - footer_height
screen_manager = ScreenManager(SCREEN_WIDTH, content_height)

# Create instance of StatPage
stat_page = StatPage(SCREEN_WIDTH, content_height)

# Create instance of InvScreen
inv_screen = Screen2(SCREEN_WIDTH, content_height)

# Define screen pages
PAGES = ["STAT", "INV", "DATA", "MAP", "RADIO"]

# Main loop
running = True
current_page = 0

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
            elif event.key == pygame.K_F5:
                current_page = 4
                screen_manager.set_active_screen('screen5')
            header.set_selected_index(current_page)

            # Handle submenu navigation for STAT, INV, and DATA
            if current_page == 0:
                if event.key == pygame.K_1:
                    stat_page.set_selected_index(0)
                elif event.key == pygame.K_2:
                    stat_page.set_selected_index(1)
                elif event.key == pygame.K_3:
                    stat_page.set_selected_index(2)
                stat_page.handle_event(event)
            elif current_page == 1:
                if event.key == pygame.K_1:
                    inv_screen.set_selected_index(0)
                elif event.key == pygame.K_2:
                    inv_screen.set_selected_index(1)
                elif event.key == pygame.K_3:
                    inv_screen.set_selected_index(2)
                elif event.key == pygame.K_4:
                    inv_screen.set_selected_index(3)
                elif event.key == pygame.K_5:
                    inv_screen.set_selected_index(4)
                inv_screen.handle_event(event)
            elif current_page == 2:
                if event.key == pygame.K_1:
                    data_screen.set_selected_index(0)
                elif event.key == pygame.K_2:
                    data_screen.set_selected_index(1)
                elif event.key == pygame.K_3:
                    data_screen.set_selected_index(2)
                data_screen.handle_event(event)

    # Fill the background
    screen.fill((0, 0, 0))  # Black background

    # Draw header and footer
    header.draw(screen)
    footer.draw(screen)
    
    # Draw the active screen
    content_surface = screen.subsurface((0, header_height, SCREEN_WIDTH, content_height))
    if current_page == 0:
        stat_page.draw(content_surface)
    elif current_page == 1:
        inv_screen.draw(content_surface)
    else:
        screen_manager.draw(content_surface)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
