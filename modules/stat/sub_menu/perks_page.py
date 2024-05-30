import pygame
from gif_loader import GifLoader  # Assuming the GIF loader script is named gif_loader.py

class PerksPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.perks = [
            ("Ace Operator", "Your stealth is increased while in shadows to 90% visibility and you deal 25% more damage with silenced weapons."),
            ("Action Boy", "Your Action Points now regenerate 50% faster."),
            ("Cloak & Dagger", "You gain +20% sneak attack damage and the duration of effects of Stealth Boys are increased by +40%."),
            ("Close to Metal", "1 additional guess at choosing passwords in terminals, 50% faster terminal cooldown at hacking"),
            ("Combat Medic", "You can heal 100 Hit Points if their current number of Hit Points is below 10%."),
            ("Massachusetts Surgery", "Inflict +2% limb damage."),
            ("Quiet Reflection", "+5% Experience Points for 8 hours."),
            ("Shield Harmonics", "Your Energy Resistance is increased by +20."),
            ("Trigger Rush", "Your Action Points regenerate 25% faster if the Hit Points value is below 25% of its maximum."),
            ("Well Rested", "+10% Experience Points for 12 hours.")
        ]
        
        self.gifs = [
            "img/perks/perk1.gif",
            "img/perks/perk2.gif",
            "img/perks/perk3.gif",
            "img/perks/perk4.gif",
            "img/perks/perk5.gif",
            "img/perks/perk6.gif",
            "img/perks/perk7.gif",
            "img/perks/perk8.gif",
            "img/perks/perk9.gif",
            "img/perks/perk10.gif"
        ]

        self.selected_index = 0
        self.scroll_offset = 0

        # Load custom font
        self.font_path = "fonts/monofonto.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font
        self.desc_font = pygame.font.Font(self.font_path, 12)  # Load custom font for descriptions

        # Styling variables
        self.perk_box_height = 30  # Height for perk boxes
        self.perk_box_width = self.width // 2 - 20
        self.perk_box_color = (0, 255, 0)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.perk_gap = 0  # Gap for visibility

        # Gif loader for the selected perk
        self.gif_loader = GifLoader(self.gifs[self.selected_index])
        
        # Manually set the desired size for the GIF
        self.gif_size = (150, 150)

        # Load and scale arrows
        self.arrow_scale = 0.5  # Default scale factor
        self.up_arrow = pygame.image.load("img/ui/up_arrow.png")
        self.down_arrow = pygame.image.load("img/ui/down_arrow.png")
        self.set_arrow_scale(self.arrow_scale)

    def set_arrow_scale(self, scale):
        self.arrow_scale = scale
        self.up_arrow = pygame.transform.scale(self.up_arrow, (int(self.up_arrow.get_width() * self.arrow_scale), int(self.up_arrow.get_height() * self.arrow_scale)))
        self.down_arrow = pygame.transform.scale(self.down_arrow, (int(self.down_arrow.get_width() * self.arrow_scale), int(self.down_arrow.get_height() * self.arrow_scale)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self.gif_loader = GifLoader(self.gifs[self.selected_index])
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
            elif event.key == pygame.K_DOWN:
                if self.selected_index < len(self.perks) - 1:
                    self.selected_index += 1
                    self.gif_loader = GifLoader(self.gifs[self.selected_index])
                    if self.selected_index >= self.scroll_offset + self.visible_perks():
                        self.scroll_offset += 1

    def visible_perks(self):
        return 6  # Only display 6 perks at a time

    def draw(self, screen):
        screen.fill(self.background_color)  # Fill the background with black

        y = 1  # Starting y position for perks
        visible_perks = self.visible_perks()

        # Draw up arrow if not at the top
        if self.scroll_offset > 0:
            screen.blit(self.up_arrow, (20, y))
        y += self.up_arrow.get_height() + 3

        # Draw visible perks
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_perks, len(self.perks))):
            perk, desc = self.perks[i]
            if i == self.selected_index:
                box_color = self.highlight_color
                text_color = self.text_color
            else:
                box_color = self.background_color
                text_color = self.default_text_color

            box_rect = pygame.Rect(10, y, self.perk_box_width, self.perk_box_height)
            pygame.draw.rect(screen, box_color, box_rect)

            # Render perk name (left-justified)
            perk_text = self.font.render(perk, True, text_color)
            screen.blit(perk_text, (box_rect.x + 10, box_rect.y + (self.perk_box_height - perk_text.get_height()) // 2))

            # Render value (right-aligned)
            #value_text = self.font.render(str(value), True, text_color)
            #value_text_rect = value_text.get_rect(right=box_rect.right - 10, centery=box_rect.centery)
            #screen.blit(value_text, value_text_rect)

            y += self.perk_box_height + self.perk_gap

        # Draw down arrow if not at the bottom
        if self.scroll_offset + visible_perks < len(self.perks):
            screen.blit(self.down_arrow, (20, y + 3))


        # Draw selected GIF and description
        gif_frame = self.gif_loader.get_current_frame()
        gif_frame = pygame.transform.scale(gif_frame, self.gif_size)
        gif_rect = gif_frame.get_rect(topleft=(310, -10))
        screen.blit(gif_frame, gif_rect)

        # Calculate max_width for text wrapping
        max_width = self.width // 2 - 40
        desc_lines = self.wrap_text(self.perks[self.selected_index][1], self.desc_font, max_width)
        for i, line in enumerate(desc_lines):
            desc_text = self.desc_font.render(line, True, (0, 255, 0))
            desc_rect = desc_text.get_rect(topleft=(self.width // 2 + 20, gif_rect.bottom + 10 + i * self.desc_font.get_height()))
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

# Example usage (if running this module directly):
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Perks Page Example")
    
    perks_page = PerksPage(640, 480)
    perks_page.set_arrow_scale(0.5)  # Set arrow scale factor (e.g., 0.5 for half size)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            perks_page.handle_event(event)
        
        perks_page.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
