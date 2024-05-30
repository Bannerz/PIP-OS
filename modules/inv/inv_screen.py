import pygame

class Screen2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (100, 100, 100)  # Gray background
        self.png_image = pygame.image.load("img/ui/head.png")  # Update the path to your PNG
        self.submenu_items = ["WEAPONS", "APPAREL", "AID", "MISC", "AMMO"]
        self.submenu_selected_index = 0

        # Load custom font
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 18)  # Load custom font

    def set_selected_index(self, index):
        self.submenu_selected_index = index

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.set_selected_index((self.submenu_selected_index - 1) % len(self.submenu_items))
            elif event.key == pygame.K_RIGHT:
                self.set_selected_index((self.submenu_selected_index + 1) % len(self.submenu_items))

    def draw_submenu(self, screen):
        submenu_rect = pygame.Rect(0, 0, self.width, 30)
        screen.fill((0, 0, 0), submenu_rect)  # Black background for submenu

        current_x = 10
        for i, item in enumerate(self.submenu_items):
            color = (0, 255, 0) if i == self.submenu_selected_index else (100, 100, 100)
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(topleft=(current_x, 5))
            screen.blit(text_surface, text_rect)
            current_x += text_rect.width + 20

    def draw(self, screen):
        # Draw the screen background
        screen_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, screen_rect)

        # Draw the PNG
        screen.blit(self.png_image, (100, 100))  # Adjust position as needed

        # Draw submenu
        self.draw_submenu(screen)

# Example usage (if running this module directly):
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Screen2 Example")
    
    screen2 = Screen2(640, 480)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen2.handle_event(event)
        
        screen2.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
