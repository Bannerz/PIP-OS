import pygame

class Header:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (0, 0, 0)  # Black background
        self.line_color = (0, 255, 0)  # Green lines
        self.font_color = (0, 255, 0)  # Green text
        
        # Load custom font
        self.font_path = "fonts/RobotoCondensed-Bold.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 18)  # Load custom font
        
        self.texts = ["STAT", "INV", "DATA", "MAP", "RADIO"]
        self.text_positions = self.calculate_text_positions()
        self.selected_index = 0  # Start with the first item selected

    def calculate_text_positions(self):
        gap_between_tabs = 30  # Adjust gap between tabs
        total_text_width = sum([self.font.size(text)[0] for text in self.texts]) + (len(self.texts) - 1) * gap_between_tabs
        start_x = (self.width - total_text_width) // 2
        positions = []
        for text in self.texts:
            text_width = self.font.size(text)[0]
            positions.append(start_x + text_width // 2)
            start_x += text_width + gap_between_tabs  # Move start_x for the next tab position
        return positions

    def draw(self, screen):
        # Fill the background
        screen.fill(self.background_color, (0, 0, self.width, self.height))

        # Draw the texts
        for i, text in enumerate(self.texts):
            text_surface = self.font.render(text, True, self.font_color)
            text_rect = text_surface.get_rect(center=(self.text_positions[i], self.height // 2))
            screen.blit(text_surface, text_rect)

        # Calculate gap for the selected tab based on text width
        selected_text_surface = self.font.render(self.texts[self.selected_index], True, self.font_color)
        selected_text_rect = selected_text_surface.get_rect(center=(self.text_positions[self.selected_index], self.height // 2))
        gap_width = selected_text_rect.width + 20  # Slightly wider than text width
        gap_start = self.text_positions[self.selected_index] - gap_width // 2
        gap_end = self.text_positions[self.selected_index] + gap_width // 2

        # Draw the horizontal line below the text with a gap under the selected text
        line_y = self.height - 10

        # Draw left part of the line
        pygame.draw.line(screen, self.line_color, (0, line_y), (gap_start, line_y), 2)
        # Draw right part of the line
        pygame.draw.line(screen, self.line_color, (gap_end, line_y), (self.width, line_y), 2)

        # Draw the small lines pointing down at each edge
        edge_line_length = 10
        pygame.draw.line(screen, self.line_color, (0, line_y), (0, line_y + edge_line_length), 2)
        pygame.draw.line(screen, self.line_color, (self.width - 2, line_y), (self.width - 2, line_y + edge_line_length), 2)

        # Draw vertical lines at the edges of the blank space
        vertical_line_height = (self.height // 2) * 3 // 4  # 3/4 of the way up the text
        pygame.draw.line(screen, self.line_color, (gap_start, line_y), (gap_start, line_y - vertical_line_height), 2)
        pygame.draw.line(screen, self.line_color, (gap_end, line_y), (gap_end, line_y - vertical_line_height), 2)

        # Draw horizontal lines pointing in from the top of the vertical lines
        horizontal_line_length = 6  # Adjusted horizontal line length for smaller window
        pygame.draw.line(screen, self.line_color, (gap_start, line_y - vertical_line_height), (gap_start + horizontal_line_length, line_y - vertical_line_height), 2)
        pygame.draw.line(screen, self.line_color, (gap_end, line_y - vertical_line_height), (gap_end - horizontal_line_length, line_y - vertical_line_height), 2)

    def set_selected_index(self, index):
        self.selected_index = index
