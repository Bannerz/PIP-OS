import pygame
import time
from gif_loader import GifLoader  # Assuming the GIF loader script is named gif_loader.py

class InitialAnimation:
    def __init__(self, screen, font_path, on_complete):
        self.screen = screen
        self.font_path = font_path
        self.font = pygame.font.Font(font_path, 16)
        self.on_complete = on_complete
        self.fade_cycles = 0
        self.max_fade_cycles = 2
        self.scroll_texts = [
            "0x00000000000000000 start memory discovery 0 0x0000A4 ",
            "CPUO starting cell relocation0 0x0000A4 0x00000000000000000 ",
            "CPUO launch EFI0 0x0000A4 0x00000000000000000 ",
            # Truncated text
            "0x00000000000000000 start memory discovery 0 0x0000A4 END"
        ]
        
        self.char_text = [
            "*************** PIP-0S (R) V7.1.0.8 ***************",
            " ",
            " ",
            "COPYRIGHT 2075 ROBCO(R) ",
            "LOADER VI.1 ",
            "EXEC VERSION 41.10 ",
            "64k RAM SYSTEM ",
            "38911 BYTES FREE ",
            "NO HOLOTAPE FOUND ",
            "LOAD ROM(1): DEITRIX 303 "
        ]
        
        self.scroll_y = self.screen.get_height()
        self.char_labels = [""] * len(self.char_text)
        self.cursor_visible = False
        self.fade_label = None
        self.current_char_index = 0
        self.current_line_index = 0

        self.gif_loader = None
        self.gif = None
        self.scaled_gif = None  # To hold the scaled GIF

        self.cursor = pygame.Rect(10, 10, 10, 20)  # Position cursor at the top initially

        self.scrolling_finished = False
        self.chars_since_last_blink = 0
        self.chars_per_blink = 3  # Blink cursor after every 3 characters
        self.text_printing_finished = False
        self.text_y = 10  # Initial Y position for text
        self.animation_complete = False  # Flag for animation completion

    def setup(self):
        pygame.time.set_timer(pygame.USEREVENT, 1000 // 60)
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def update_fast_scroll(self):
        self.scroll_y -= 5
        if self.scroll_y <= -len(self.scroll_texts) * 20:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            self.scrolling_finished = True
            self.start_text_printing()

    def start_text_printing(self):
        self.current_char_index = 0
        self.current_line_index = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)
        pygame.time.set_timer(pygame.USEREVENT + 3, 200)  # Blink cursor every 200ms

    def print_text(self):
        if self.current_line_index < len(self.char_text):
            if self.current_char_index < len(self.char_text[self.current_line_index]):
                self.char_labels[self.current_line_index] += self.char_text[self.current_line_index][self.current_char_index]
                self.current_char_index += 1
                self.chars_since_last_blink += 1
                if self.chars_since_last_blink >= self.chars_per_blink:
                    self.cursor_visible = not self.cursor_visible
                    self.chars_since_last_blink = 0
            else:
                self.current_char_index = 0
                self.current_line_index += 1
        else:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            pygame.time.set_timer(pygame.USEREVENT + 4, 500)  # Blink cursor at the end of text printing
            self.text_printing_finished = True

    def start_slow_scroll(self):
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000 // 60)

    def update_slow_scroll(self):
        self.text_y -= 2
        if self.text_y <= -len(self.char_text) * 20:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            self.display_gif()

    def display_gif(self):
        self.gif_loader = GifLoader('animation.gif')
        self.gif = self.gif_loader.get_current_frame()

        # Get original dimensions
        original_width, original_height = self.gif.get_size()

        # Scale the GIF while maintaining aspect ratio
        desired_height = 180
        aspect_ratio = original_width / original_height
        scaled_width = int(desired_height * aspect_ratio)
        scaled_height = desired_height
        self.scaled_gif = pygame.transform.scale(self.gif, (scaled_width, scaled_height))

        self.gif_x = (self.screen.get_width() - scaled_width) // 2
        self.gif_y = (self.screen.get_height() - scaled_height) // 2
        self.fade_initiating()

    def fade_initiating(self):
        self.fade_label = self.font.render('INITIATING', True, (0, 255, 0))
        self.fade_alpha = 255
        self.fade_direction = -5
        pygame.time.set_timer(pygame.USEREVENT + 5, 1000 // 60)

    def fade_text(self):
        self.fade_alpha += self.fade_direction
        if self.fade_alpha <= 0:
            self.fade_alpha = 0
            self.fade_cycles += 1
            self.fade_direction = 5
        elif self.fade_alpha >= 255:
            self.fade_alpha = 255
            self.fade_cycles += 1
            self.fade_direction = -5

        if self.fade_cycles >= self.max_fade_cycles * 2:
            pygame.time.set_timer(pygame.USEREVENT + 5, 0)
            self.on_complete()

    def draw(self):
        self.screen.fill((0, 0, 0))

        if not self.scrolling_finished:
            for i, text in enumerate(self.scroll_texts):
                label = self.font.render(text, True, (0, 255, 0))
                self.screen.blit(label, (10, self.scroll_y + i * 20))
        else:
            y = self.text_y
            for i, label in enumerate(self.char_labels):
                rendered_label = self.font.render(label, True, (0, 255, 0))
                self.screen.blit(rendered_label, (10, y + i * 20))

            if self.cursor_visible and self.current_line_index < len(self.char_labels):
                cursor_y = y + self.current_line_index * 20
                self.cursor.topleft = (10 + self.font.size(self.char_labels[self.current_line_index])[0], cursor_y)
                pygame.draw.rect(self.screen, (0, 255, 0), self.cursor)

            if self.gif_loader:
                self.gif = self.gif_loader.get_current_frame()
                self.scaled_gif = pygame.transform.scale(self.gif, (self.scaled_gif.get_width(), self.scaled_gif.get_height()))
                self.screen.blit(self.scaled_gif, (self.gif_x, self.gif_y))

                # Draw "INITIATING" text below the GIF
                if self.fade_label:
                    fade_surface = self.fade_label.copy()
                    fade_surface.set_alpha(self.fade_alpha)
                    fade_y = self.gif_y + self.scaled_gif.get_height() + 10
                    self.screen.blit(fade_surface, (self.screen.get_width() // 2 - fade_surface.get_width() // 2, fade_y))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            self.update_fast_scroll()
        elif event.type == pygame.USEREVENT + 1:
            self.print_text()
        elif event.type == pygame.USEREVENT + 2:
            self.update_slow_scroll()
        elif event.type == pygame.USEREVENT + 3:
            if self.text_printing_finished:
                self.cursor_visible = not self.cursor_visible
            else:
                self.cursor_visible = not self.cursor_visible
        elif event.type == pygame.USEREVENT + 4:
            pygame.time.set_timer(pygame.USEREVENT + 4, 0)
            self.start_slow_scroll()
        elif event.type == pygame.USEREVENT + 5:
            self.fade_text()

    def cleanup(self):
        pygame.time.set_timer(pygame.USEREVENT, 0)
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        pygame.time.set_timer(pygame.USEREVENT + 3, 0)
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        pygame.time.set_timer(pygame.USEREVENT + 5, 0)

def on_complete():
    print("Animation complete")

pygame.init()
screen = pygame.display.set_mode((480, 320))
font_path = 'fonts/RobotoCondensed-Regular.ttf'
animation = InitialAnimation(screen, font_path, on_complete)
animation.setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        animation.handle_event(event)

    animation.draw()
    time.sleep(0.01)  # Cap the frame rate

animation.cleanup()
pygame.quit()
