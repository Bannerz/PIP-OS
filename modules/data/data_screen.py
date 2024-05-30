import pygame

class Screen3:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (100, 100, 250)  # Blueish background

    def draw(self, screen):
        # Draw the screen background
        screen_rect = pygame.Rect(0, 50, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, screen_rect)
