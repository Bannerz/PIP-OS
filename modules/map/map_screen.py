import pygame

class Screen4:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (250, 250, 100)  # Yellowish background

    def draw(self, screen):
        # Draw the screen background
        screen_rect = pygame.Rect(0, 50, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, screen_rect)
