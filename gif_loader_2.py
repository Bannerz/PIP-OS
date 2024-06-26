from PIL import Image, ImageSequence
import pygame

class GifLoader:
    def __init__(self, gif_path):
        self.gif_path = gif_path
        self.frames = self.load_gif()
        self.current_frame = 0
        self.total_frames = len(self.frames)
        self.frame_delay = 100  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()

    def load_gif(self):
        image = Image.open(self.gif_path)
        frames = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_image)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % self.total_frames

    def get_current_frame(self):
        self.update()
        return self.frames[self.current_frame]
