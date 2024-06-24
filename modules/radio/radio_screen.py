import pygame
import os
import numpy as np
import random
from scipy.io import wavfile

class RadioPage:
    def __init__(self, width, height, audio_dir):
        self.width = width
        self.height = height
        self.audio_dir = audio_dir
        self.font_path = "fonts/RobotoCondensed-Regular.ttf"
        self.font = pygame.font.Font(self.font_path, 16)

        # Initialize Pygame mixer
        pygame.mixer.init()
        print("Pygame mixer initialized")

        # Path for the "Radio Off" sound
        self.radio_off_sound = "modules/ui_elements/UISounds/UI_Pipboy_Radio_Off.ogg"
        print(f"Radio off sound path: {self.radio_off_sound}")

        # List of directories
        self.directories = ["Radio Off"]
        for entry in os.listdir(audio_dir):
            if os.path.isdir(os.path.join(audio_dir, entry)):
                self.directories.append(entry)
        print(f"Directories found: {self.directories}")

        self.selected_index = 0
        self.scroll_offset = 0
        self.current_playlist = []
        self.current_song_index = 0

        # Variables to store waveform data
        self.waveform = None
        self.audio_data = None
        self.sample_rate = None
        self.chunk_size = 2048  # Number of samples per chunk
        self.current_chunk = 0
        self.audio_pos = 0

        # Timer event for updating waveform
        self.WAVEFORM_UPDATE_EVENT = pygame.USEREVENT + 1
        print("RadioPage initialized")

        # Colors and dimensions
        self.box_height = 25
        self.highlight_color = (0, 100, 0)
        self.text_color = (0, 0, 0)
        self.default_text_color = (0, 255, 0)
        self.box_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.max_visible_items = 6

        # Load and scale arrows
        self.arrow_scale = 0.5  # Default scale factor
        self.up_arrow = pygame.image.load("img/ui/up_arrow.png")
        self.down_arrow = pygame.image.load("img/ui/down_arrow.png")
        self.set_arrow_scale(self.arrow_scale)

        # Load initial playlist and play audio
        self.load_playlist()

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
                print(f"Selected index: {self.selected_index}")
                self.load_playlist()
            elif event.key == pygame.K_DOWN:
                if self.selected_index < len(self.directories) - 1:
                    self.selected_index += 1
                    if self.selected_index >= self.scroll_offset + self.max_visible_items:
                        self.scroll_offset += 1
                print(f"Selected index: {self.selected_index}")
                self.load_playlist()
        elif event.type == self.WAVEFORM_UPDATE_EVENT:
            print("Waveform update event triggered")
            self.update_waveform()

    def draw(self, screen):
        screen.fill(self.background_color)
        y = 40
        visible_items = self.max_visible_items

        # Draw up arrow if not at the top
        if self.scroll_offset > 0:
            screen.blit(self.up_arrow, (10, y - self.up_arrow.get_height() - 5))

        # Draw visible items
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_items, len(self.directories))):
            directory = self.directories[i]
            if i == self.selected_index:
                box_color = self.box_color
                text_color = self.text_color
            else:
                box_color = self.background_color
                text_color = self.default_text_color

            box_rect = pygame.Rect(10, y, 200, self.box_height)
            pygame.draw.rect(screen, box_color, box_rect)
            #pygame.draw.rect(screen, self.box_color, box_rect, 2)

            directory_text = self.font.render(directory, True, text_color)
            screen.blit(directory_text, (box_rect.x + 10, box_rect.y + (self.box_height - directory_text.get_height()) // 2))

            y += self.box_height + 5

        # Draw down arrow if not at the bottom
        if self.scroll_offset + visible_items < len(self.directories):
            screen.blit(self.down_arrow, (10, y + 5))

        # Draw waveform
        if self.waveform is not None:
            self.draw_graph(screen)
            self.draw_waveform(screen)

    def draw_graph(self, screen):
        # Define dimensions and padding
        graph_x = self.width // 2
        graph_y = 40
        graph_width = self.width // 2 - 20
        graph_height = 200
        outer_padding = 5
        inner_padding = 20

        # Draw the outer graph border (bottom and right only)
        pygame.draw.line(screen, (0, 255, 0), (graph_x + outer_padding, graph_y + graph_height - outer_padding), (graph_x + graph_width - outer_padding, graph_y + graph_height - outer_padding), 3)  # bottom border
        pygame.draw.line(screen, (0, 255, 0), (graph_x + graph_width - outer_padding, graph_y + outer_padding), (graph_x + graph_width - outer_padding, graph_y + graph_height - outer_padding), 3)  # right border

        # Draw y-axis grid lines protruding slightly inside the graph
        num_lines = 5
        line_spacing = (graph_height - 2 * outer_padding) // num_lines
        line_length_short = 3  # Length of the shorter protruding lines
        line_length_long = 6  # Length of the longer protruding lines
        for i in range(num_lines + 1):
            y = graph_y + outer_padding + i * line_spacing
            line_length = line_length_long if i % 2 == 0 else line_length_short
            pygame.draw.line(screen, (0, 255, 0), (graph_x + graph_width - outer_padding - line_length, y), (graph_x + graph_width - outer_padding, y), 2)

        # Draw bottom axis grid lines protruding slightly inside the graph
        num_lines = 10
        line_spacing = (graph_width - 2 * outer_padding) // num_lines
        for i in range(num_lines + 1):
            x = graph_x + outer_padding + i * line_spacing
            line_length = line_length_long if i % 2 == 0 else line_length_short
            pygame.draw.line(screen, (0, 255, 0), (x, graph_y + graph_height - outer_padding), (x, graph_y + graph_height - outer_padding - line_length), 2)

        # Draw inner black border inside the graph for the visualization
        pygame.draw.rect(screen, (0, 0, 0), (graph_x + inner_padding, graph_y + inner_padding, graph_width - 2 * inner_padding, graph_height - 2 * inner_padding), 1)

    def draw_waveform(self, screen):
        graph_x = self.width // 2
        graph_y = 40
        graph_width = self.width // 2 - 20
        graph_height = 200
        inner_padding = 20

        bar_width = (graph_width - 2 * inner_padding) / len(self.waveform)
        max_height = graph_height - 2 * inner_padding

        for i in range(len(self.waveform)):
            x = graph_x + inner_padding + i * bar_width
            y = graph_y + graph_height - inner_padding - (self.waveform[i] * max_height)
            pygame.draw.line(screen, (0, 255, 0), (x, graph_y + graph_height - inner_padding), (x, y))

    def play_audio(self):
        if not self.current_playlist:
            pygame.mixer.music.stop()
            return

        file_path = self.current_playlist[self.current_song_index]
        print(f"Playing audio: {file_path}")
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            print(f"Playing: {file_path}")
        except pygame.error as e:
            print(f"Error playing audio: {e}")

    def load_playlist(self):
        print("Loading playlist")
        if self.selected_index == 0:
            self.current_playlist = [self.radio_off_sound]
            self.current_song_index = 0
            self.load_waveform()
            self.play_audio()  # Play audio immediately
            return

        directory_path = os.path.join(self.audio_dir, self.directories[self.selected_index])
        print(f"Loading playlist from: {directory_path}")

        self.current_playlist = [
            os.path.join(directory_path, file)
            for file in os.listdir(directory_path)
            if file.endswith((".wav", ".ogg"))
        ]

        print(f"Playlist: {self.current_playlist}")

        if self.current_playlist:
            random.shuffle(self.current_playlist)
            self.current_song_index = 0
            self.load_waveform()
            self.play_audio()  # Play audio immediately
        else:
            print("No valid audio files found in directory")

    def load_waveform(self):
        if not self.current_playlist:
            self.waveform = None
            pygame.mixer.music.stop()
            pygame.time.set_timer(self.WAVEFORM_UPDATE_EVENT, 0)
            return

        file_path = self.current_playlist[self.current_song_index]
        print(f"Loading waveform for: {file_path}")

        try:
            if file_path.endswith(".wav"):
                self.sample_rate, self.audio_data = wavfile.read(file_path)
            elif file_path.endswith(".ogg"):
                sound = pygame.mixer.Sound(file_path)
                self.audio_data = np.frombuffer(sound.get_raw(), dtype=np.int16)
                self.sample_rate = 44100  # Typical sample rate

            print(f"Sample rate: {self.sample_rate}, Audio data length: {len(self.audio_data)}")

            # Normalize and convert to mono if necessary
            if len(self.audio_data.shape) == 2:
                self.audio_data = self.audio_data.mean(axis=1)
            self.audio_data = self.audio_data / np.max(np.abs(self.audio_data))

            self.current_chunk = 0
            self.audio_pos = 0

            # Start the timer to update the waveform
            pygame.time.set_timer(self.WAVEFORM_UPDATE_EVENT, int(1000 * self.chunk_size / self.sample_rate))
        except Exception as e:
            print(f"Error loading waveform: {e}")

    def update_waveform(self):
        if self.audio_data is None:
            return

        start = self.audio_pos
        end = start + self.chunk_size
        if start >= len(self.audio_data):
            self.waveform = None
            return

        chunk = self.audio_data[start:end]
        self.audio_pos = end

        # Perform FFT on the chunk
        fft_data = np.abs(np.fft.rfft(chunk))
        fft_data = fft_data / np.max(fft_data)  # Normalize

        # Update the waveform data
        self.waveform = fft_data

    def handle_end_of_song(self):
        print("End of song")
        self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)
        self.load_waveform()
        self.play_audio()  # Automatically play the next song

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
            elif event.type == pygame.USEREVENT:
                radio_page.handle_end_of_song()
            else:
                radio_page.handle_event(event)

        radio_page.draw(screen)
        pygame.display.flip()

    pygame.quit()
