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
        self.height = height
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

        # Example values for inventory footer
        self.weight = "50/100"
        self.caps = "250"
        self.ammo = "120"

        # Load and scale icons
        self.weight_icon = pygame.image.load("img/ui/weight.png")
        self.caps_icon = pygame.image.load("img/ui/caps.png")
        self.ammo_icon = pygame.image.load("img/ui/gun.png")
        self.target_icon = pygame.image.load("img/ui/target.png")

        self.weight_icon = pygame.transform.scale(self.weight_icon, (15, 15))
        self.caps_icon = pygame.transform.scale(self.caps_icon, (15, 15))
        self.ammo_icon = pygame.transform.scale(self.ammo_icon, (10, 10))
        self.target_icon = pygame.transform.scale(self.target_icon, (10, 10))
        
        # Footer texts
        self.default_text = "Default Footer"
        self.inventory_text = "Inventory Footer: [1] Weapons [2] Apparel [3] Aid [4] Ammo [5] Misc"
        self.current_text = self.default_text

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

    def set_footer_text(self, page):
        if page == "inventory":
            self.current_text = self.inventory_text
        else:
            self.current_text = self.default_text

    def draw_default_footer(self, screen):
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

    def draw_inventory_footer(self, screen):
        gap = 4
        side_box_width = self.width // 4
        center_box_width = self.width // 2 - 2 * gap

        weight_box_rect = pygame.Rect(0, screen.get_height() - self.height, side_box_width, self.height)
        caps_box_rect = pygame.Rect(side_box_width + gap, screen.get_height() - self.height, side_box_width, self.height)
        ammo_box_rect = pygame.Rect(2 * side_box_width + 2 * gap, screen.get_height() - self.height, center_box_width, self.height)

        # Fill the background of the footer
        footer_rect = pygame.Rect(0, screen.get_height() - self.height, self.width, self.height)
        screen.fill(self.background_color, footer_rect)

        # Adjust y-offsets for weight and caps icons
        y_offset = 0

        # Draw Weight box
        pygame.draw.rect(screen, self.box_color, weight_box_rect)
        weight_icon_rect = self.weight_icon.get_rect(center=(weight_box_rect.x + 15, weight_box_rect.centery + y_offset))
        screen.blit(self.weight_icon, weight_icon_rect)
        weight_text = self.font.render(self.weight, True, self.text_color)
        weight_text_rect = weight_text.get_rect(midleft=(weight_icon_rect.right + 5, weight_box_rect.centery + y_offset))
        screen.blit(weight_text, weight_text_rect)

        # Draw Caps box
        pygame.draw.rect(screen, self.box_color, caps_box_rect)
        caps_icon_rect = self.caps_icon.get_rect(center=(caps_box_rect.x + 15, caps_box_rect.centery + y_offset))
        screen.blit(self.caps_icon, caps_icon_rect)
        caps_text = self.font.render(self.caps, True, self.text_color)
        caps_text_rect = caps_text.get_rect(midleft=(caps_icon_rect.right + 5, caps_box_rect.centery + y_offset))
        screen.blit(caps_text, caps_text_rect)

        # Draw Ammo box right justified
        pygame.draw.rect(screen, self.box_color, ammo_box_rect)
        ammo_text = self.font.render(self.ammo, True, self.text_color)
        ammo_text_rect = ammo_text.get_rect(midright=(ammo_box_rect.right - 10, ammo_box_rect.centery))
        screen.blit(ammo_text, ammo_text_rect)
        
        # Draw target icon to the right of the gun icon and to the left of the ammo number
        target_icon_rect = self.target_icon.get_rect(midright=(ammo_text_rect.left - 5, ammo_box_rect.centery))
        screen.blit(self.target_icon, target_icon_rect)
        
        ammo_icon_rect = self.ammo_icon.get_rect(midright=(target_icon_rect.left - 5, ammo_box_rect.centery))
        screen.blit(self.ammo_icon, ammo_icon_rect)

    def draw(self, screen, page):
        if page == "inventory":
            self.draw_inventory_footer(screen)
        else:
            self.draw_default_footer(screen)
