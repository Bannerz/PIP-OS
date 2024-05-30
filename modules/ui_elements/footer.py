import pygame
from datetime import datetime

def draw_rounded_rect(screen, color, rect, corner_radius):
    """
    Draw a rectangle with rounded corners.
    """
    pygame.draw.rect(screen, color, rect, border_radius=corner_radius)

class Footer:
    def __init__(self, width, height, birthday):
        self.width = width
        self.height = height  # Reduce height to half
        self.background_color = (0, 0, 0)  # Black background
        self.box_color = (0, 100, 0)  # Darker green box color
        self.text_color = (0, 255, 0)  # Bright green text color for contrast
        self.border_color = (0, 200, 0)  # Different green color for border
        self.progress_bg_color = (0, 50, 0)  # Darker green color for progress bar background
        
          # Load custom font
        self.font_path = "fonts/RobotoCondensed-Bold.ttf"  # Replace with actual path to your custom font file
        self.font = pygame.font.Font(self.font_path, 18)  # Load custom font
        
        self.birthday = birthday  # User's birthday
        self.age = self.calculate_age()  # User's age
        self.level_progress = self.calculate_progress()  # Progress towards next birthday
        self.hp = "75/100"  # Example HP value
        self.ap = "50/90"  # Example AP value

    def calculate_age(self):
        today = datetime.today()
        birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    def calculate_progress(self):
        today = datetime.today()
        birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
        next_birthday = birth_date.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        total_days = (next_birthday - birth_date.replace(year=today.year - 1)).days
        days_passed = (today - birth_date.replace(year=today.year)).days
        return days_passed / total_days

    def draw(self, screen):
        # Calculate box dimensions and positions
        gap = 4
        side_box_width = self.width // 5
        level_box_width = self.width - 2 * side_box_width - 2 * gap

        hp_box_rect = pygame.Rect(0, screen.get_height() - self.height, side_box_width, self.height)
        level_box_rect = pygame.Rect(side_box_width + gap, screen.get_height() - self.height, level_box_width, self.height)
        ap_box_rect = pygame.Rect(side_box_width + level_box_width + 2 * gap, screen.get_height() - self.height, side_box_width, self.height)

        # Fill the background of the footer
        footer_rect = pygame.Rect(0, screen.get_height() - self.height, self.width, self.height)
        screen.fill(self.background_color, footer_rect)

        # Draw HP box
        pygame.draw.rect(screen, self.box_color, hp_box_rect)
        hp_text = self.font.render(f"HP {self.hp}", True, self.text_color)
        hp_text_rect = hp_text.get_rect(center=hp_box_rect.center)
        screen.blit(hp_text, hp_text_rect)

        # Draw LEVEL box
        pygame.draw.rect(screen, self.box_color, level_box_rect)
        level_text = self.font.render(f"LEVEL {self.age}", True, self.text_color)
        level_text_rect = level_text.get_rect(midleft=(level_box_rect.x + 10, level_box_rect.centery))
        screen.blit(level_text, level_text_rect)

        # Draw level progress bar next to the level label
        progress_bar_width = level_box_rect.width - level_text_rect.width - 30
        progress_bar_height = 10
        progress_bar_x = level_text_rect.right + 10
        progress_bar_y = level_box_rect.centery - progress_bar_height // 2

        # Draw the border for the progress bar
        border_rect = pygame.Rect(progress_bar_x - 1, progress_bar_y - 1, progress_bar_width + 2, progress_bar_height + 2)
        draw_rounded_rect(screen, self.border_color, border_rect, 2)

        # Draw the background of the progress bar (darker green)
        progress_bar_bg_rect = pygame.Rect(progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)
        draw_rounded_rect(screen, self.progress_bg_color, progress_bar_bg_rect, 2)

        # Draw the progress bar (bright green)
        progress_bar_rect = pygame.Rect(progress_bar_x, progress_bar_y, int(progress_bar_width * self.level_progress), progress_bar_height)
        draw_rounded_rect(screen, (0, 255, 0), progress_bar_rect, 2)

        # Draw AP box
        pygame.draw.rect(screen, self.box_color, ap_box_rect)
        ap_text = self.font.render(f"AP {self.ap}", True, self.text_color)
        ap_text_rect = ap_text.get_rect(center=ap_box_rect.center)
        screen.blit(ap_text, ap_text_rect)
