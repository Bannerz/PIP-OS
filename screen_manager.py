from modules.stat.stat_screen import StatPage
from modules.inv.inv_screen import Screen2
from modules.data.data_screen import Screen3
from modules.map.map_screen import Screen4
from modules.radio.radio_screen import Screen5

class ScreenManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screens = {
            'screen1': StatPage(width, height),
            'screen2': Screen2(width, height),
            'screen3': Screen3(width, height),
            'screen4': Screen4(width, height),
            'screen5': Screen5(width, height),
        }
        self.active_screen = self.screens['screen1']

    def set_active_screen(self, screen_name):
        if screen_name in self.screens:
            self.active_screen = self.screens[screen_name]

    def handle_event(self, event):
        self.active_screen.handle_event(event)

    def draw(self, screen):
        self.active_screen.draw(screen)
