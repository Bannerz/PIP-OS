import pygame

class Screen5:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (250, 100, 250)  # Pinkish background

    def draw(self, screen):
        # Draw the screen background
        screen_rect = pygame.Rect(0, 50, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, screen_rect)
        
    def handle_event(self, event):
        # Placeholder for handling events in the data screen
        pass