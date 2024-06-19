import pygame
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from io import BytesIO
from pydub import AudioSegment

class RadioPage:
    def __init__(self, width, height, audio_dir):
        self.width = width
        self.height = height
        self.audio_dir = audio_dir
        self.font = pygame.font.Font(None, 24)

        # Initialize Pygame mixer
        pygame.mixer.init()

        # List of audio files
        self.audio_files = ["Radio Off"]
        for file in os.listdir(audio_dir):
            if file.endswith(".mp3") or file.endswith(".ogg"):
                self.audio_files.append(file)

        self.selected_index = 0

        # Variables to store waveform data
        self.waveform = None

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Draw list of audio files
        for i, file in enumerate(self.audio_files):
            color = (0, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(file, True, color)
            screen.blit(text, (20, 40 + i * 30))

        # Draw waveform
        if self.waveform is not None:
            waveform_surf = pygame.surfarray.make_surface(self.waveform)
            screen.blit(waveform_surf, (self.width // 2, 40))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self.load_waveform()
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.audio_files) - 1, self.selected_index + 1)
                self.load_waveform()
            elif event.key == pygame.K_RETURN:
                self.play_audio()

    def load_waveform(self):
        if self.selected_index == 0:
            self.waveform = None
            return

        file_path = os.path.join(self.audio_dir, self.audio_files[self.selected_index])
        
        if file_path.endswith(".mp3") or file_path.endswith(".ogg"):
            audio = AudioSegment.from_file(file_path)
            wav_data = np.array(audio.get_array_of_samples())
            sample_rate = audio.frame_rate
        else:
            sample_rate, wav_data = wavfile.read(file_path)

        # Normalize and convert to mono if necessary
        if len(wav_data.shape) == 2:
            wav_data = wav_data.mean(axis=1)
        wav_data = wav_data / np.max(np.abs(wav_data))

        # Generate waveform image
        fig, ax = plt.subplots()
        ax.plot(wav_data[:1000])  # Plot first 1000 samples for performance reasons
        ax.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        self.waveform = pygame.image.load(buf)

    def play_audio(self):
        pygame.mixer.music.stop()
        if self.selected_index == 0:
            return

        file_path = os.path.join(self.audio_dir, self.audio_files[self.selected_index])
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Radio Page Example")

    audio_dir = "path/to/your/audio/files"
    radio_page = RadioPage(640, 480, audio_dir)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            radio_page.handle_event(event)

        radio_page.draw(screen)
        pygame.display.flip()

    pygame.quit()
