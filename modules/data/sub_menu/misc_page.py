import pygame

class MiscPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        content_text = ""
        text = self.font.render(content_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(text, text_rect)

    def handle_event(self, event):
        pass
