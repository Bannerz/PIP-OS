import pygame
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps

class MapPage:
    def __init__(self, width, height, mapbox_api_key):
        self.width = width
        self.height = height
        self.api_key = mapbox_api_key
        self.map_image = None
        self.latitude, self.longitude = self.fetch_location()
        self.zoom = 15  # Default zoom level
        self.scroll_step = 0.001  # Amount of change in latitude/longitude per key press
        self.marker_image = Image.open('img/ui/marker.png')  # Load the marker image
        self.marker_size = (20, 20)  # Desired marker size
        self.scaled_marker_image = self.marker_image.resize(self.marker_size, Image.Resampling.LANCZOS)
        self.marker_position = (self.latitude, self.longitude)  # Store the marker's initial coordinates

    def scan_wifi_networks(self):
        wifi_data = []
        # Scan for Wi-Fi networks
        try:
            # Run the command to scan for Wi-Fi networks
            result = subprocess.run(['nmcli', '-t', '-f', 'BSSID,SIGNAL', 'dev', 'wifi'], capture_output=True, text=True)
            # Parse the result
            lines = result.stdout.splitlines()
            for line in lines:
                match = re.match(r'^(.*?):(.*?)$', line)
                if match:
                    bssid = match.group(1)
                    signal = int(match.group(2))
                    wifi_data.append({'macAddress': bssid, 'signalStrength': signal})
        except Exception as e:
            print(f"Error scanning Wi-Fi networks: {e}")
        return wifi_data

    def get_location_from_mls(self, wifi_data):
        url = 'https://location.services.mozilla.com/v1/geolocate?key=test'
        payload = {
            'wifiAccessPoints': wifi_data
        }
        try:
            response = requests.post(url, json=payload)
            location = response.json()
            return location['location']['lat'], location['location']['lng']
        except Exception as e:
            print(f"Error getting location from MLS: {e}")
            return None, None

    def fetch_location(self):
        wifi_data = self.scan_wifi_networks()
        latitude, longitude = self.get_location_from_mls(wifi_data)
        if latitude and longitude:
            return latitude, longitude
        else:
            # Fallback to a fixed location if unable to fetch accurate location
            return 37.7749, -122.4194  # San Francisco, CA

    def fetch_map(self, latitude, longitude):
        url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{longitude},{latitude},{self.zoom},0,0/{self.width}x{self.height}?access_token={self.api_key}&attribution=false&logo=false"
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content)).convert("RGB")
            image = self.tint_image(image, (0, 255, 0))
            # Overlay the marker on the map at the initial position
            image = self.overlay_marker(image, latitude, longitude, self.marker_position)
            self.map_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        else:
            print("Failed to fetch map data")

    def tint_image(self, image, tint_color):
        """Tint PIL image with the given color."""
        r, g, b = tint_color
        tinted_image = Image.new("RGB", image.size)
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                tinted_pixel = (pixel[0] * r // 255, pixel[1] * g // 255, pixel[2] * b // 255)
                tinted_image.putpixel((x, y), tinted_pixel)
        return tinted_image

    def overlay_marker(self, image, center_latitude, center_longitude, marker_position):
        """Overlay the marker image at the user's initial location."""
        map_width, map_height = image.size
        marker_width, marker_height = self.scaled_marker_image.size

        # Calculate relative position of the marker
        marker_latitude, marker_longitude = marker_position
        lat_diff = (marker_latitude - center_latitude) * (map_height / 180)
        lon_diff = (marker_longitude - center_longitude) * (map_width / 360)

        position = (
            map_width // 2 + int(lon_diff) - marker_width // 2,
            map_height // 2 - int(lat_diff) - marker_height // 2
        )

        image.paste(self.scaled_marker_image, position, self.scaled_marker_image)  # Use the marker's alpha channel as mask
        return image

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.longitude -= self.scroll_step
                self.fetch_map(self.latitude, self.longitude)
            elif event.key == pygame.K_RIGHT:
                self.longitude += self.scroll_step
                self.fetch_map(self.latitude, self.longitude)
            elif event.key == pygame.K_UP:
                self.latitude += self.scroll_step
                self.fetch_map(self.latitude, self.longitude)
            elif event.key == pygame.K_DOWN:
                self.latitude -= self.scroll_step
                self.fetch_map(self.latitude, self.longitude)

    def draw(self, screen):
        if self.map_image:
            screen.blit(self.map_image, (0, 0))
        else:
            font = pygame.font.Font(None, 36)
            text = font.render("Loading map...", True, (0, 255, 0))
            screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
