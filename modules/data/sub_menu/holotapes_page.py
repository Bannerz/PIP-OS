import pygame
import subprocess
import sys
from gif_loader_2 import GifLoader  # Ensure the GIF loader script is available and correctly implemented

class HolotapesPage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.holotapes = [
            {"name": "Atomic Command", "gif": "img/items/holotape.gif", "game": "modules/atomic-command/Game.py"},
            {"name": "A.F.A.D. manifesto", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/AFAD_manifesto.ogg"},
            {"name": "C.I.T. recon report", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/C.I.T._Recon_Report-Holotape.ogg"},
            {"name": "Find the Silver Shroud", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/Find_the_Silver_Shroud.ogg"},
            {"name": "Hi honey!", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/Nora.ogg"},
            {"name": "Nuka-Cola Clear", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/Nuka-Cola_Clear(holodisk).ogg"},
            {"name": "Nuka-World paramedic report", "gif": "img/items/holotape.gif", "audio": "modules/data/sounds/Nuka-World_paramedic_report.ogg"}
        ]

        self.selected_index = 0
        self.scroll_offset = 0

        # Load custom font
        self.font_path = "fonts/monofonto.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 16)  # Load custom font
        self.desc_font = pygame.font.Font(self.font_path, 12)  # Load custom font for descriptions

        # Styling variables
        self.holotape_box_height = 30  # Height for holotape boxes
        self.holotape_box_width = self.width // 2 - 20
        self.holotape_box_color = (0, 255, 0)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.holotape_gap = 0  # Gap for visibility

        # Gif loader for the selected holotape
        self.gif_loader = GifLoader(self.holotapes[self.selected_index]["gif"])

        # Manually set the desired size for the GIF
        self.gif_size = (150, 150)

        # Load and scale arrows
        self.arrow_scale = 0.5  # Default scale factor
        self.up_arrow = pygame.image.load("img/ui/up_arrow.png")
        self.down_arrow = pygame.image.load("img/ui/down_arrow.png")
        self.set_arrow_scale(self.arrow_scale)

        self.dial_switch = pygame.mixer.Sound("modules/ui_elements/UISounds/dial_move.ogg")

        # Initialize mixer for playing audio
        pygame.mixer.init()

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
                    self.gif_loader = GifLoader(self.holotapes[self.selected_index]["gif"])
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
            elif event.key == pygame.K_DOWN:
                self.dial_switch.play()
                if self.selected_index < len(self.holotapes) - 1:
                    self.selected_index += 1
                    self.gif_loader = GifLoader(self.holotapes[self.selected_index]["gif"])
                    if self.selected_index >= self.scroll_offset + self.visible_holotapes():
                        self.scroll_offset += 1
            elif event.key == pygame.K_RETURN:
                self.launch_game()

    def visible_holotapes(self):
        return 6  # Only display 6 holotapes at a time

    def launch_game(self):
        selected_holotape = self.holotapes[self.selected_index]
        if selected_holotape.get("game"):
            game_script = selected_holotape["game"]
            subprocess.Popen(["python", game_script]).wait()
            if sys.platform.startswith('linux'):
                subprocess.Popen(["xdotool", "search", "--name", "RobCo PIP-OS v1", "windowactivate"])
        elif selected_holotape.get("audio"):
            audio_file = selected_holotape["audio"]
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

    def draw(self, screen):
        screen.fill(self.background_color)  # Fill the background with black

        y = 1  # Starting y position for holotapes
        visible_holotapes = self.visible_holotapes()

        # Draw up arrow if not at the top
        if self.scroll_offset > 0:
            screen.blit(self.up_arrow, (20, y))
        y += self.up_arrow.get_height() + 3

        # Draw visible holotapes
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_holotapes, len(self.holotapes))):
            holotape = self.holotapes[i]["name"]
            if i == self.selected_index:
                box_color = self.highlight_color
                text_color = self.text_color
            else:
                box_color = self.background_color
                text_color = self.default_text_color

            box_rect = pygame.Rect(10, y, self.holotape_box_width, self.holotape_box_height)
            pygame.draw.rect(screen, box_color, box_rect)

            # Render holotape name (left-justified)
            holotape_text = self.font.render(holotape, True, text_color)
            screen.blit(holotape_text, (box_rect.x + 10, box_rect.y + (self.holotape_box_height - holotape_text.get_height()) // 2))

            y += self.holotape_box_height + self.holotape_gap

        # Draw down arrow if not at the bottom
        if self.scroll_offset + visible_holotapes < len(self.holotapes):
            screen.blit(self.down_arrow, (20, y + 3))

        # Draw selected GIF
        gif_frame = self.gif_loader.get_current_frame()
        gif_frame = pygame.transform.scale(gif_frame, self.gif_size)
        gif_rect = gif_frame.get_rect(topleft=(self.width - self.gif_size[0] - 20, 0))
        screen.blit(gif_frame, gif_rect)

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    holotapes_page = HolotapesPage(480, 320)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            holotapes_page.handle_event(event)
        holotapes_page.draw(screen)
        pygame.display.flip()
    pygame.quit()
