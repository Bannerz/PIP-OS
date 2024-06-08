import pygame

class InvFooter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.footer_height = 20
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"
        self.font = pygame.font.Font(self.font_path, 16)
        self.background_color = (50, 50, 50)  # Dark gray background
        self.text_color = (255, 255, 255)  # White text
        self.text = "Inventory Footer: [1] Weapons [2] Apparel [3] Aid [4] Ammo [5] Misc"

    def draw(self, screen):
        footer_rect = pygame.Rect(0, self.height - self.footer_height, self.width, self.footer_height)
        pygame.draw.rect(screen, self.background_color, footer_rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height - self.footer_height // 2))
        screen.blit(text_surface, text_rect)
