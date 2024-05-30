import pygame

class InitialAnimation:
    def __init__(self, window, font, on_complete):
        self.window = window
        self.font = font
        self.on_complete = on_complete
        self.fade_cycles = 0  # Number of fade cycles completed
        self.max_fade_cycles = 2  # Number of fade cycles to complete
        self.scroll_texts = [
            "* 1 0 0x0000A4 0x00000000000000000 start memory discovery 0 0x0000A4 ",
            "0x00000000000000000 1 0 0x000014 0x00000000000000000 CPUO starting cell ",
            "relocation0 0x0000A4 0x00000000000000000 1 0 0x000009 ",
            "0x00000000000000000 CPUO launch EFI0 0x0000A4 0x00000000000000000 1 0 ",
            "0x000009 0x000000000000E003D CPUO starting EFI0 0x0000A4 ",
        ]
        self.elements = []

    def setup(self):
        self.elements.clear()
        self.current_text = ""
        self.current_index = 0
        self.update_fast_scroll()

        # Load and play the GIF animation
        animation = pygame.image.load('animation.gif')
        sprite = pygame.transform.scale(animation, (180, int(180 * animation.get_height() / animation.get_width())))
        sprite_rect = sprite.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.elements.append((sprite, sprite_rect))

        self.fade_label = self.font.render('INITIATING', True, (0, 255, 0))
        self.fade_label_rect = self.fade_label.get_rect(center=(self.window.get_width() // 2, 50))
        self.fade_initiating()

    def update_fast_scroll(self):
        self.current_index += 1
        if self.current_index < len(self.scroll_texts):
            self.current_text = self.scroll_texts[self.current_index]
        else:
            self.current_index = 0
            self.current_text = self.scroll_texts[self.current_index]
        self.fast_scroll_label = self.font.render(self.current_text, True, (0, 255, 0))
        self.fast_scroll_label_rect = self.fast_scroll_label.get_rect(center=(self.window.get_width() // 2, 150))
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

    def fade_initiating(self):
        self.fade_alpha = 255
        self.fade_direction = -5
        self.fade_timer = pygame.time.set_timer(pygame.USEREVENT + 2, 1000 // 60)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.update_fast_scroll()
        elif event.type == pygame.USEREVENT + 2:
            self.fade_text()

    def fade_text(self):
        self.fade_alpha += self.fade_direction
        if self.fade_alpha <= 0:
            self.fade_alpha = 0
            self.fade_direction = 5
            self.fade_cycles += 1
        elif self.fade_alpha >= 255:
            self.fade_alpha = 255
            self.fade_direction = -5
            self.fade_cycles += 1

        if self.fade_cycles >= self.max_fade_cycles * 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            self.on_complete()
        self.fade_label.set_alpha(self.fade_alpha)

    def draw(self):
        self.window.blit(self.fade_label, self.fade_label_rect)
        self.window.blit(self.fast_scroll_label, self.fast_scroll_label_rect)
        for element, rect in self.elements:
            self.window.blit(element, rect)

    def cleanup(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        self.elements.clear()
