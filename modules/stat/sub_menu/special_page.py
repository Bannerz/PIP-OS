import pygame
from gif_loader import GifLoader  # Assuming the GIF loader script is named gif_loader.py

class SpecialPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.attributes = [
            ("Strength", 5, "Strength is a measure of your raw physical power. It affects how much you can carry, and the damage of all melee attacks."),
            ("Perception", 7, "Perception is your environmental awareness and 'sixth sense,' and affects weapon accuracy in V.A.T.S."),
            ("Endurance", 6, "Endurance is a measure of your overall physical fitness. It affects your total Health and the Action Point drain from sprinting."),
            ("Charisma", 8, "Charisma is your ability to charm and convince others. It affects your success to persuade in dialogue and prices when you barter."),
            ("Intelligence", 9, "Intelligence is a measure of your overall mental acuity, and affects the number of Experience Points earned."),
            ("Agility", 6, "Agility is a measure of your overall finesse and reflexes. It affects the number of Action Points in V.A.T.S. and your ability to sneak."),
            ("Luck", 7, "Luck is a measure of your general good fortune, and affects the recharge rate of Critical Hits.")
        ]

        self.gifs = [
            "img/perks/strength.gif",
            "img/perks/perception.gif",
            "img/perks/endurance.gif",
            "img/perks/charisma.gif",
            "img/perks/intelligence.gif",
            "img/perks/agility.gif",
            "img/perks/luck.gif"
        ]

        self.selected_index = 0

        # Load custom font
        self.font_path = "fonts/monofonto.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font
        self.desc_font = pygame.font.Font(self.font_path, 12)  # Load custom font for descriptions

        # Styling variables
        self.attribute_box_height = (self.height - 20) // len(self.attributes)
        self.attribute_box_width = 200
        self.attribute_box_color = (0, 255, 0)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.attribute_gap = 0  # Adjusted gap for visibility

        # Gif loader for the selected attribute
        self.gif_loader = GifLoader(self.gifs[self.selected_index])
        
        # Manually set the desired size for the GIF
        self.gif_size = (130, 130)
        
        self.dial_switch = pygame.mixer.Sound("modules/ui_elements/UISounds/dial_move.ogg")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.dial_switch.play()
                self.selected_index = (self.selected_index - 1) % len(self.attributes)
                self.gif_loader = GifLoader(self.gifs[self.selected_index])
            elif event.key == pygame.K_DOWN:
                self.dial_switch.play()
                self.selected_index = (self.selected_index + 1) % len(self.attributes)
                self.gif_loader = GifLoader(self.gifs[self.selected_index])


    def draw(self, screen):
        screen.fill(self.background_color)  # Fill the background with black

        y = 10  # Starting y position for attributes
        for i, (attribute, value, desc) in enumerate(self.attributes):
            if i == self.selected_index:
                box_color = self.highlight_color
                text_color = self.text_color
            else:
                box_color = self.background_color
                text_color = self.default_text_color

            box_rect = pygame.Rect(10, y, self.attribute_box_width, self.attribute_box_height)
            pygame.draw.rect(screen, box_color, box_rect)

            # Render attribute name
            attribute_text = self.font.render(attribute, True, text_color)
            screen.blit(attribute_text, (box_rect.x + 10, box_rect.y + (self.attribute_box_height - attribute_text.get_height()) // 2))

            y += self.attribute_box_height + self.attribute_gap

        # Draw selected GIF and description
        gif_frame = self.gif_loader.get_current_frame()
        gif_frame = pygame.transform.scale(gif_frame, self.gif_size)
        gif_rect = gif_frame.get_rect(topleft=(self.attribute_box_width + 80, 0))  # Adjusted y position for better layout
        screen.blit(gif_frame, gif_rect)

        # Calculate max_width for text wrapping
        max_width = self.width - self.attribute_box_width - 40
        desc_lines = self.wrap_text(self.attributes[self.selected_index][2], self.desc_font, max_width)
        for i, line in enumerate(desc_lines):
            desc_text = self.desc_font.render(line, True, (0, 255, 0))
            desc_rect = desc_text.get_rect(topleft=(self.attribute_box_width + 30, gif_rect.bottom + 10 + i * self.desc_font.get_height()))
            screen.blit(desc_text, desc_rect)

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit a given width when rendered."""
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            line_width, _ = font.size(' '.join(current_line))
            if line_width > max_width:
                # Pop the last word and add the line to lines
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        # Add the last line
        lines.append(' '.join(current_line))
        return lines
