import pygame
from gif_loader import GifLoader  # Assuming the GIF loader script is named gif_loader.py

class StatusPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gif_path = "img/ui/body.gif"  # Path to the GIF file
        self.png_path = "img/ui/head.png"  # Path to the PNG file
        self.icon_paths = [
            "img/ui/gun.png",
            "img/ui/target.png",
            "img/ui/helmet.png",
            "img/ui/shield.png",
            "img/ui/lightning.png",
            "img/ui/radiation.png"
        ]  # Paths to the icon images
        
        self.numbers = [None, 18, None, 10, 20, 10]
        self.icon_positions = [140, 185, 220, 265, 295, 325]
        
        self.gif_position = (0, -20)  # Position offset for the GIF
        self.png_position = (0, -53)  # Position offset for the PNG
        self.gif_size = (59, 81)  # Desired size for the GIF (width, height)
        self.png_size = (30, 40)  # Desired size for the PNG (width, height)
        
        self.box_size = 40
        self.rect_width = 25
        self.rect_height = self.box_size
        self.icon_padding = 10  # Padding around each icon
        self.icon_gap = 15  # Gap between icons
        self.number_height = 5 # Height of the number below the icons
        self.rectangle_size = (20, 5)  # Size of the rectangles (width, height)
        self.rectangle_gap = 30  # Gap between the PNG and rectangles

        # Vertical positions for each rectangle
        self.rect_above_y = -10
        self.rect_below_y = 80
        self.rect_left_top_y = 15
        self.rect_left_bottom_y = 70
        self.rect_right_top_y = 15
        self.rect_right_bottom_y = 70

        self.gif = GifLoader(self.gif_path)  # Use GifLoader class to load and animate the GIF
        self.png = pygame.image.load(self.png_path).convert_alpha()  # Load PNG image
        self.png = pygame.transform.scale(self.png, self.png_size)  # Scale PNG image

        # Load icons
        self.icons = [self.load_icon(icon_path) for icon_path in self.icon_paths]
        
        # Load custom font
        self.font_path = "fonts/monofonto.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font
        self.banner_font = pygame.font.Font(self.font_path, 18)  # Load custom font for banner text
        
        

    def load_icon(self, path):
        try:
            icon = pygame.image.load(path).convert_alpha()
            return icon
        except pygame.error:
            # If the icon is not found, create a placeholder surface
            icon = pygame.Surface((self.box_size, self.box_size if 'gun' in path or 'helmet' in path else self.rect_height))
            icon.fill((0, 255, 0))  # Fill with green color as a placeholder
            return icon

    def handle_event(self, event):
        pass  # Add event handling if necessary

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the background with black

        # Get and draw the current frame of the animated GIF
        gif_frame = self.gif.get_current_frame()
        gif_frame = pygame.transform.scale(gif_frame, self.gif_size)  # Scale the GIF frame
        gif_rect = gif_frame.get_rect(center=(self.width // 2 + self.gif_position[0], self.height // 2 + self.gif_position[1]))
        screen.blit(gif_frame, gif_rect)

        # Draw PNG
        png_rect = self.png.get_rect(center=(gif_rect.centerx + self.png_position[0], gif_rect.centery + self.png_position[1]))
        screen.blit(self.png, png_rect)

        # Draw green rectangles around GIF and PNG
        rectangle_color = (0, 255, 0)
        rectangle_width, rectangle_height = self.rectangle_size

        # Rectangle above the PNG
        rect_above = pygame.Rect(png_rect.centerx - rectangle_width // 2, png_rect.top + self.rect_above_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_above)

        # Rectangles on the left of the PNG (corresponding to the body)
        rect_left_top = pygame.Rect(png_rect.left - rectangle_width - self.rectangle_gap, png_rect.centery + self.rect_left_top_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_left_top)
        rect_left_bottom = pygame.Rect(png_rect.left - rectangle_width - self.rectangle_gap, png_rect.centery + self.rect_left_bottom_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_left_bottom)

        # Rectangles on the right of the PNG (corresponding to the body)
        rect_right_top = pygame.Rect(png_rect.right + self.rectangle_gap, png_rect.centery + self.rect_right_top_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_right_top)
        rect_right_bottom = pygame.Rect(png_rect.right + self.rectangle_gap, png_rect.centery + self.rect_right_bottom_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_right_bottom)

        # Rectangle below the GIF
        rect_below = pygame.Rect(png_rect.centerx - rectangle_width // 2, png_rect.bottom + self.rect_below_y, rectangle_width, rectangle_height)
        pygame.draw.rect(screen, rectangle_color, rect_below)

        # Move the entire line up a bit to avoid the footer
        y = self.height // 2 + self.gif_position[1] + 60

        for i, (icon, number) in enumerate(zip(self.icons, self.numbers)):
            if i in [0, 2]:  # Square boxes for gun and helmet
                box_x = self.icon_positions[i]
                box = pygame.Rect(box_x, y, self.box_size, self.box_size)
                scale_factor = 0.8 * min(self.box_size / icon.get_width(), self.box_size / icon.get_height())  # Reduce size by 20%
                icon = pygame.transform.scale(icon, (int(icon.get_width() * scale_factor), int(icon.get_height() * scale_factor)))
                icon_rect = icon.get_rect(midtop=(box_x + self.box_size // 2, y + 5))  # Place icon at the top of the box
                number_y = y + self.box_size - self.number_height - 5
            else:  # Vertical rectangles for other images
                box_x = self.icon_positions[i]
                box = pygame.Rect(box_x, y, self.rect_width, self.rect_height)
                scale_factor = 0.7 * min(self.rect_width / icon.get_width(), (self.rect_height - 20) / icon.get_height())  # Reduce size by 20%
                icon = pygame.transform.scale(icon, (int(icon.get_width() * scale_factor), int(icon.get_height() * scale_factor)))
                icon_rect = icon.get_rect(midtop=(box_x + self.rect_width // 2, y + 5))  # Place icon at the top of the box
                number_y = y + self.rect_height - self.number_height - 5

            pygame.draw.rect(screen, (0, 100, 0), box)
            screen.blit(icon, icon_rect)

            if number is not None:
                number_surface = self.font.render(str(number), True, (0, 255, 0))
                number_rect = number_surface.get_rect(center=(box_x + box.width // 2, number_y))  # Position number within the box
                screen.blit(number_surface, number_rect)

        # Add centered text label "ZapWizard"
        label_x = self.width // 2
        label_y = y + self.box_size + 20  # Adjust the y position as needed
        text_surface = self.banner_font.render('Bannerz', True, (0, 255, 0))
        text_rect = text_surface.get_rect(center=(label_x, label_y))
        screen.blit(text_surface, text_rect)
