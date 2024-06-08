from modules.stat.stat_screen import StatPage
from modules.inv.inv_screen import InvPage
from modules.data.data_screen import DataPage
from modules.map.map_screen import MapPage
from modules.radio.radio_screen import Screen5

class ScreenManager:
    def __init__(self, width, height, mapbox_api_key):
        self.width = width
        self.height = height
        self.screens = {
            'screen1': StatPage(width, height),
            'screen2': InvPage(width, height),
            'screen3': DataPage(width, height),
            'screen4': MapPage(width, height, mapbox_api_key),
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
