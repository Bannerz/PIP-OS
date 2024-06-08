import pygame
from modules.data.sub_menu.holotapes_page import HolotapesPage
from modules.data.sub_menu.quests_page import QuestsPage
from modules.data.sub_menu.misc_page import MiscPage

class DataPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.submenu_items = ["HOLOTAPES", "QUESTS", "MISC"]
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font

        self.submenu_selected_index = 0
        self.left_margin = 60  # Define a left margin for the submenu
        self.gap = 10  # Define the gap between submenu items

        content_height = height - 30
        self.holotapes_page = HolotapesPage(width, content_height)
        self.quests_page = QuestsPage(width, content_height)
        self.misc_page = MiscPage(width, content_height)
        self.active_page = self.holotapes_page

    def set_selected_index(self, index):
        self.submenu_selected_index = index
        if index == 0:
            self.active_page = self.holotapes_page
        elif index == 1:
            self.active_page = self.quests_page
        elif index == 2:
            self.active_page = self.misc_page

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.set_selected_index(0)
            elif event.key == pygame.K_2:
                self.set_selected_index(1)
            elif event.key == pygame.K_3:
                self.set_selected_index(2)
            else:
                self.active_page.handle_event(event)

    def draw_submenu(self, screen):
        submenu_rect = pygame.Rect(0, 0, self.width, 30)
        screen.fill((0, 0, 0), submenu_rect)  # Black background for submenu

        current_x = self.left_margin
        for i, item in enumerate(self.submenu_items):
            color = (0, 255, 0) if i == self.submenu_selected_index else (0, 100, 0)
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(midleft=(current_x, 15))
            screen.blit(text_surface, text_rect)
            current_x += text_rect.width + self.gap

    def draw(self, screen):
        self.draw_submenu(screen)
        content_rect = pygame.Rect(0, 30, self.width, self.height - 30)
        content_surface = screen.subsurface(content_rect)
        self.active_page.draw(content_surface)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Data Screen Example")

    data_screen = DataPage(640, 480)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            data_screen.handle_event(event)

        data_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()