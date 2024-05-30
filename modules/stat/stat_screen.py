import pygame
from modules.stat.sub_menu.status_page import StatusPage
from modules.stat.sub_menu.special_page import SpecialPage
from modules.stat.sub_menu.perks_page import PerksPage

class StatPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.header_height = 40
        self.submenu_height = 30
        self.submenu_items = ["STATUS", "SPECIAL", "PERKS"]
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font

        self.submenu_selected_index = 0
        self.left_margin = 60  # Define a left margin for the submenu
        self.gap = 10  # Define the gap between submenu items

        content_height = height - self.submenu_height
        self.status_page = StatusPage(width, content_height)
        self.special_page = SpecialPage(width, content_height)
        self.perks_page = PerksPage(width, content_height)
        self.active_page = self.status_page

    def set_selected_index(self, index):
        self.submenu_selected_index = index
        if index == 0:
            self.active_page = self.status_page
        elif index == 1:
            self.active_page = self.special_page
        elif index == 2:
            self.active_page = self.perks_page

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.set_selected_index((self.submenu_selected_index - 1) % len(self.submenu_items))
            elif event.key == pygame.K_RIGHT:
                self.set_selected_index((self.submenu_selected_index + 1) % len(self.submenu_items))
            else:
                self.active_page.handle_event(event)

    def draw_submenu(self, screen):
        submenu_rect = pygame.Rect(0, 0, self.width, self.submenu_height)
        screen.fill((0, 0, 0), submenu_rect)  # Black background for submenu

        current_x = self.left_margin
        for i, item in enumerate(self.submenu_items):
            color = (0, 255, 0) if i == self.submenu_selected_index else (0, 100, 0)
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(midleft=(current_x, self.submenu_height // 2))
            screen.blit(text_surface, text_rect)
            current_x += text_rect.width + self.gap

    def draw(self, screen):
        self.draw_submenu(screen)
        content_rect = pygame.Rect(0, self.submenu_height, self.width, self.height - self.submenu_height)
        content_surface = screen.subsurface(content_rect)
        self.active_page.draw(content_surface)
