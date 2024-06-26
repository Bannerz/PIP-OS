import pygame
from gif_loader_2 import GifLoader  # Assuming the GIF loader script is named gif_loader.py

class AmmoPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ammo_items = [
            ("10mm Rounds", [("Damage", 18), ("Weight", 0.1), ("Value", 5)], "img/items/10mmround.gif", False, "Standard 10mm rounds"),
            ("Fusion Cells", [("Damage", 15), ("Weight", 0.05), ("Value", 8)], "img/items/fusioncell.gif", False, "Used in energy weapons")
        ]
        self.selected_index = 0
        self.scroll_offset = 0
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"
        self.font = pygame.font.Font(self.font_path, 16)
        self.box_height = 20
        self.box_color = (0, 255, 0)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.gap = 0
        self.second_gap = 2
        self.ammo_box_width = self.width // 2 - 20
        self.ammo_box_height = 30

        # Attributes for the selected ammo item
        self.attribute_font = pygame.font.Font(self.font_path, 12)
        self.attribute_bg_color = (0, 100, 0)
        self.attribute_text_color = (0, 255, 0)

        # Load and scale arrows
        self.arrow_scale = 1.0  # Default scale factor
        self.up_arrow = pygame.image.load("img/ui/up_arrow.png")
        self.down_arrow = pygame.image.load("img/ui/down_arrow.png")
        self.set_arrow_scale(self.arrow_scale)

        self.gif_loader = None
        self.gif_scale = 0.5  # Set the desired scale for the GIFs

        self.update_gif_loader()  # Ensure the GIF is loaded initially

        self.dial_switch = pygame.mixer.Sound("modules/ui_elements/UISounds/dial_move.ogg")

    def set_arrow_scale(self, scale):
        self.arrow_scale = scale
        self.up_arrow = pygame.transform.scale(self.up_arrow, (int(self.up_arrow.get_width() * self.arrow_scale), int(self.up_arrow.get_height() * self.arrow_scale)))
        self.down_arrow = pygame.transform.scale(self.down_arrow, (int(self.down_arrow.get_width() * self.arrow_scale), int(self.down_arrow.get_height() * self.arrow_scale)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.dial_switch.play()
                if self.selected_index > 0:
                    self.selected_index -= 1
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
                    self.update_gif_loader()
            elif event.key == pygame.K_DOWN:
                self.dial_switch.play()
                if self.selected_index < len(self.ammo_items) - 1:
                    self.selected_index += 1
                    if self.selected_index >= self.scroll_offset + self.visible_ammo_items():
                        self.scroll_offset += 1
                    self.update_gif_loader()

    def visible_ammo_items(self):
        return 6  # Only display 6 ammo items at a time

    def update_gif_loader(self):
        selected_item_gif = self.ammo_items[self.selected_index][2]
        self.gif_loader = GifLoader(selected_item_gif)

    def draw(self, screen):
        screen.fill(self.background_color)
        y = 10
        visible_ammo_items = self.visible_ammo_items()

        # Draw up arrow if not at the top
        if self.scroll_offset > 0:
            screen.blit(self.up_arrow, (10, y))
        y += self.up_arrow.get_height() + 3

        # Draw GIF for the selected item above the attributes
        if self.gif_loader:
            gif_image = self.gif_loader.get_current_frame()
            # Scale the GIF
            scaled_size = (int(gif_image.get_width() * self.gif_scale), int(gif_image.get_height() * self.gif_scale))
            gif_image = pygame.transform.scale(gif_image, scaled_size)
            gif_rect = gif_image.get_rect(center=(self.width // 2 + self.width // 4, self.height // 4))
            screen.blit(gif_image, gif_rect.topleft)

        # Draw visible ammo items
        symbol_y_offset = 0  # Adjust this value to move the symbol up or down
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_ammo_items, len(self.ammo_items))):
            ammo, attributes, gif_path, is_equipped, description = self.ammo_items[i]
            if i == self.selected_index:
                box_color = self.highlight_color
                text_color = self.text_color
                symbol_color = (0, 0, 0)  # Black when selected
            else:
                box_color = self.background_color
                text_color = self.default_text_color
                symbol_color = self.default_text_color  # Default color when not selected

            box_rect = pygame.Rect(10, y, self.width // 2 - 20, self.ammo_box_height)
            pygame.draw.rect(screen, box_color, box_rect)

            if is_equipped:  # Draw the equipped symbol next to the ammo item name
                symbol_rect = pygame.Rect(box_rect.x + 10, box_rect.y + (self.ammo_box_height - 10) // 2 + symbol_y_offset, 10, 10)
                pygame.draw.rect(screen, symbol_color, symbol_rect)
                text_x = box_rect.x + 30  # Push text to the right to clear the symbol
            else:
                text_x = box_rect.x + 10

            ammo_text = self.font.render(ammo, True, text_color)
            screen.blit(ammo_text, (text_x, box_rect.y + (self.ammo_box_height - ammo_text.get_height()) // 2))

            y += self.ammo_box_height + self.gap

        # Draw down arrow if not at the bottom
        if self.scroll_offset + visible_ammo_items < len(self.ammo_items):
            screen.blit(self.down_arrow, (10, y + 3))

        # Draw attributes on the right side from the bottom up
        selected_ammo_attributes = self.ammo_items[self.selected_index][1]
        description_text = self.ammo_items[self.selected_index][4]
        num_attributes = len(selected_ammo_attributes)
        attribute_width = self.width // 2 - 40

        # Calculate the total height of all attributes including gaps
        total_height = num_attributes * (self.box_height + self.gap) - self.gap

        # Calculate the starting y position for attributes
        attribute_y = self.height - total_height - 20

        # Draw description text if it exists
        if description_text:
            description_surface = self.attribute_font.render("  " + description_text, True, self.attribute_text_color)
            description_rect = description_surface.get_rect(topleft=(self.width // 2 + 20, attribute_y - 30))
            screen.blit(description_surface, description_rect)
            attribute_y -= 30  # Adjust starting y position for attributes to accommodate description text

        for i, (attr_name, attr_value) in enumerate(selected_ammo_attributes):
            attr_rect = pygame.Rect(self.width // 2 + 20, attribute_y + i * (self.box_height + self.second_gap), attribute_width, self.box_height)
            pygame.draw.rect(screen, self.attribute_bg_color, attr_rect)

            attr_name_text = self.attribute_font.render(attr_name, True, self.attribute_text_color)
            screen.blit(attr_name_text, (attr_rect.x + 10, attr_rect.y + (attr_rect.height - attr_name_text.get_height()) // 2))

            attr_value_text = self.attribute_font.render(str(attr_value), True, self.attribute_text_color)
            screen.blit(attr_value_text, (attr_rect.right - attr_value_text.get_width() - 10, attr_rect.y + (attr_rect.height - attr_value_text.get_height()) // 2))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            line_width, _ = font.size(' '.join(current_line))
            if line_width > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines
