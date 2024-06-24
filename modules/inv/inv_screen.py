import pygame
from modules.inv.sub_menu.weapons_page import WeaponsPage
from modules.inv.sub_menu.apparel_page import ApparelPage
from modules.inv.sub_menu.aid_page import AidPage
from modules.inv.sub_menu.misc_page import MiscPage
from modules.inv.sub_menu.ammo_page import AmmoPage

class InvPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.submenu_items = ["WEAPONS", "APPAREL", "AID", "MISC", "AMMO"]
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font

        self.submenu_selected_index = 0
        self.left_margin = 60  # Define a left margin for the submenu
        self.gap = 10  # Define the gap between submenu items

        content_height = height - 30
        self.weapons_page = WeaponsPage(width, content_height)
        self.apparel_page = ApparelPage(width, content_height)
        self.aid_page = AidPage(width, content_height)
        self.misc_page = MiscPage(width, content_height)
        self.ammo_page = AmmoPage(width, content_height)
        self.active_page = self.weapons_page
        
        self.sub_switch = pygame.mixer.Sound("modules/ui_elements/UISounds/submodule_change.ogg")

    def set_selected_index(self, index):
        self.submenu_selected_index = index
        if index == 0:
            self.active_page = self.weapons_page
        elif index == 1:
            self.active_page = self.apparel_page
        elif index == 2:
            self.active_page = self.aid_page
        elif index == 3:
            self.active_page = self.misc_page
        elif index == 4:
            self.active_page = self.ammo_page

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.sub_switch.play()
                self.set_selected_index(0)
            elif event.key == pygame.K_2:
                self.sub_switch.play()
                self.set_selected_index(1)
            elif event.key == pygame.K_3:
                self.sub_switch.play()
                self.set_selected_index(2)
            elif event.key == pygame.K_4:
                self.sub_switch.play()
                self.set_selected_index(3)
            elif event.key == pygame.K_5:
                self.sub_switch.play()
                self.set_selected_index(4)
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
    pygame.display.set_caption("Inventory Screen Example")

    inv_screen = InvScreen(640, 480)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            inv_screen.handle_event(event)

        inv_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()
