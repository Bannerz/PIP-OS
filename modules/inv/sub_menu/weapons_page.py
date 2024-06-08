import pygame
from gif_loader import GifLoader  # Assuming the GIF loader script is named gif_loader.py


class WeaponsPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.weapons = [
            ("10mm Pistol", [("Damage", 18), ("Fire Rate", 46), ("Range", 83), ("Accuracy", 60), ("Weight", 3.5), ("Value", 50)], "img/items/10mmpistol.gif", True),
            ("Fragmentation Grenade [5]", [("Damage", 151), ("Weight", 0.5), ("Value", 50)], "img/items/grenade.gif", True),
            ("Combat Knife", [("Damage", 6), ("Fire Rate", "FAST"), ("Weight", 0.5), ("Value", 100)], "img/items/knife.gif", False),
            ("Laser Musket", [("Damage", 30), ("Fire Rate", 6), ("Range", 71), ("Accuracy", 70), ("Weight", 12.6), ("Value", 57)], "img/items/lasermusket.gif", False),
            ("Wazer Wifle", [("Damage", 55), ("Fire Rate", 50), ("Range", 302), ("Accuracy", 76), ("Weight", 6.3), ("Value", 364)], "img/items/laserrifle.gif", False),
            ("Bottlecap Mine [2]", [("Damage", 301), ("Weight", 0.5), ("Value", 75)], "img/items/capmine.gif", False),
            ("Plasma Mine [2]", [("Damage", 300), ("Weight", 0.5), ("Value", 100)], "img/items/plasmamine.gif", False)
        ]
        self.selected_index = 0
        self.scroll_offset = 0
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"
        self.font = pygame.font.Font(self.font_path, 16)
        self.box_height = 20
        self.box_color = (0, 255, 0)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.symbol_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.gap = 0
        self.second_gap = 2
        self.weapons_box_width = self.width // 2 - 20
        self.weapons_box_height = 30

        # Attributes for the selected weapon
        self.attribute_font = pygame.font.Font(self.font_path, 12)
        self.attribute_bg_color = (0, 100, 0)
        self.attribute_text_color = (0, 255, 0)
        self.target_icon = pygame.image.load("img/ui/target.png")  # Load the target icon
        self.target_icon = pygame.transform.scale(self.target_icon, (10, 10))  # Scale the icon

        # Load and scale arrows
        self.arrow_scale = 0.5  # Default scale factor
        self.up_arrow = pygame.image.load("img/ui/up_arrow.png")
        self.down_arrow = pygame.image.load("img/ui/down_arrow.png")
        self.set_arrow_scale(self.arrow_scale)

        self.gif_loader = None
        self.gif_scale = 0.5  # Set the desired scale for the GIFs

        self.update_gif_loader()  # Ensure the GIF is loaded initially

    def set_arrow_scale(self, scale):
        self.arrow_scale = scale
        self.up_arrow = pygame.transform.scale(self.up_arrow, (int(self.up_arrow.get_width() * self.arrow_scale), int(self.up_arrow.get_height() * self.arrow_scale)))
        self.down_arrow = pygame.transform.scale(self.down_arrow, (int(self.down_arrow.get_width() * self.arrow_scale), int(self.down_arrow.get_height() * self.arrow_scale)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
                    self.update_gif_loader()
            elif event.key == pygame.K_DOWN:
                if self.selected_index < len(self.weapons) - 1:
                    self.selected_index += 1
                    if self.selected_index >= self.scroll_offset + self.visible_weapons():
                        self.scroll_offset += 1
                    self.update_gif_loader()

    def visible_weapons(self):
        return 6  # Only display 6 weapons at a time

    def update_gif_loader(self):
        selected_weapon_gif = self.weapons[self.selected_index][2]
        self.gif_loader = GifLoader(selected_weapon_gif)

    def draw(self, screen):
        screen.fill(self.background_color)
        y = 1
        visible_weapons = self.visible_weapons()

        # Draw up arrow if not at the top
        if self.scroll_offset > 0:
            screen.blit(self.up_arrow, (20, y))
        y += self.up_arrow.get_height() + 3

        # Draw GIF for the selected item above the attributes
        if self.gif_loader:
            gif_image = self.gif_loader.get_current_frame()
            # Scale the GIF
            scaled_size = (int(gif_image.get_width() * self.gif_scale), int(gif_image.get_height() * self.gif_scale))
            gif_image = pygame.transform.scale(gif_image, scaled_size)
            gif_rect = gif_image.get_rect(center=(self.width // 2 + self.width // 4, self.height // 4))
            screen.blit(gif_image, gif_rect.topleft)

        # Draw visible weapons
        symbol_y_offset = 5  # Adjust this value to move the symbol up or down
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_weapons, len(self.weapons))):
            weapon, attributes, effects, is_equipped = self.weapons[i]
            if i == self.selected_index:
                box_color = self.highlight_color
                text_color = self.text_color
                symbol_color = (0, 0, 0)
            else:
                box_color = self.background_color
                text_color = self.default_text_color
                symbol_color = self.default_text_color

            box_rect = pygame.Rect(10, y, self.weapons_box_width, self.weapons_box_height)
            pygame.draw.rect(screen, box_color, box_rect)

            if is_equipped:  # Draw the equipped symbol next to the weapon name
                symbol_rect = pygame.Rect(box_rect.x + 10, box_rect.y + (self.box_height - 10) // 2 + symbol_y_offset, 10, 10)
                pygame.draw.rect(screen, symbol_color, symbol_rect)
                text_x = box_rect.x + 30  # Push text to the right to clear the symbol
            else:
                text_x = box_rect.x + 10

            weapon_text = self.font.render(weapon, True, text_color)
            screen.blit(weapon_text, (text_x, box_rect.y + (self.weapons_box_height - weapon_text.get_height()) // 2))

            y += self.weapons_box_height + self.gap

        # Draw down arrow if not at the bottom
        if self.scroll_offset + visible_weapons < len(self.weapons):
            screen.blit(self.down_arrow, (20, y + 3))

        # Draw attributes on the right side from the bottom up
        selected_weapon_attributes = self.weapons[self.selected_index][1]
        effects_text = self.weapons[self.selected_index][2]
        num_attributes = len(selected_weapon_attributes)
        attribute_width = self.width // 2 - 40

        # Calculate the total height of all attributes including gaps
        total_height = num_attributes * (self.box_height + self.gap) - self.gap

        # Calculate the starting y position for attributes
        attribute_y = self.height - total_height + 10

        # Draw effects text if it exists
        if effects_text:
            effects_surface = self.attribute_font.render("  " + effects_text, True, self.attribute_text_color)
            effects_rect = effects_surface.get_rect(topleft=(self.width // 2 + 20, attribute_y - 30))
            screen.blit(effects_surface, effects_rect)
            attribute_y -= 30  # Adjust starting y position for attributes to accommodate effects text

        for i, (attr_name, attr_value) in enumerate(selected_weapon_attributes):
            attr_rect = pygame.Rect(self.width // 2 + 20, attribute_y + i * (self.box_height + self.second_gap), attribute_width, self.box_height)
            pygame.draw.rect(screen, self.attribute_bg_color, attr_rect)

            if i == 0:
                left_rect = pygame.Rect(attr_rect.x, attr_rect.y, attr_rect.width * 3 // 4, attr_rect.height)
                right_rect = pygame.Rect(left_rect.right, attr_rect.y, attr_rect.width // 4, attr_rect.height)
                pygame.draw.rect(screen, self.attribute_bg_color, left_rect)
                pygame.draw.rect(screen, self.attribute_bg_color, right_rect)
                # Draw separator
                pygame.draw.line(screen, (0, 0, 0), (left_rect.right, left_rect.y), (left_rect.right, left_rect.y + left_rect.height))

                attr_name_text = self.attribute_font.render(attr_name, True, self.attribute_text_color)
                screen.blit(attr_name_text, (left_rect.x + 10, left_rect.y + (left_rect.height - attr_name_text.get_height()) // 2))

                screen.blit(self.target_icon, (right_rect.x + 10, right_rect.y + (right_rect.height - self.target_icon.get_height()) // 2))
                attr_value_text = self.attribute_font.render(str(attr_value), True, self.attribute_text_color)
                screen.blit(attr_value_text, (right_rect.x + 10 + self.target_icon.get_width() + 5, right_rect.y + (right_rect.height - attr_value_text.get_height()) // 2))
            else:
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
