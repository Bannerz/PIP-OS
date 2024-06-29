import pygame
import random
import math

# Initiates pygame
pygame.init()
# Set main screen's dimensions
screen = pygame.display.set_mode((480, 320), pygame.NOFRAME)

# Hide mouse
pygame.mouse.set_visible(0)

# Load the missile image
missile_image = pygame.image.load('modules/atomic-command/Resources/bomb.png')
missile_image = pygame.transform.scale(missile_image, (7, 22))  # Scale it to a proper size

# Load the player images
player_base_image = pygame.image.load('modules/atomic-command/Resources/player_base.png')
player_base_image = pygame.transform.scale(player_base_image, (36, 60))  # Scale it to a proper size
player_gun_image = pygame.image.load('modules/atomic-command/Resources/player_gun.png')
player_gun_image = pygame.transform.scale(player_gun_image, (7, 16))  # Scale it to a proper size

# Load the city images
city_images = [
    pygame.image.load('modules/atomic-command/Resources/bridge.png'),
    pygame.image.load('modules/atomic-command/Resources/mtrushmore.png'),
    pygame.image.load('modules/atomic-command/Resources/empire.png'),
    pygame.image.load('modules/atomic-command/Resources/capitol.png'),
    pygame.image.load('modules/atomic-command/Resources/statue.png'),
    pygame.image.load('modules/atomic-command/Resources/vegas.png')
]

for i in range(len(city_images)):
    city_images[i] = pygame.transform.scale(city_images[i], (31, 58))  # Adjust the size as needed

# Load the splash screen image
splash_image = pygame.image.load('modules/atomic-command/Resources/splash.png')
splash_image = pygame.transform.scale(splash_image, (440, 320))  # Scale to full screen

# Levels

class Level:
    def __init__(self, lvl, time, qnt):
        self.lvl = lvl
        self.time = time
        self.qnt = qnt

levels = [Level(i, 60000, 6 * i + 6) for i in range(1, 21)]

# City

class City:
    def __init__(self, index, x, sprite):
        self.index = index
        self.x = x
        self.y = 262
        self.status = "alive"
        self.sprite = sprite

cities = [City(i, x, city_images[i]) for i, x in enumerate([5, 80, 145, 290, 350, 410])]

isAlive = [True] * 6

def allDead():
    return all(not status for status in isAlive)

# Player

playerColor = (0, 255, 0)
playerHeight = 8
playerWidth = 8
playerX = 240
playerY = 160

# Bomb

bombColor = (0, 255, 0)
bombRadius = 10
bombRange = 50
bomb_state = "ready"
bombX = playerX
bombY = playerY

# Projectile

projectile_color = (0, 255, 0)
projectile_speed = 10
projectile_state = "ready"
projectile_x = 0
projectile_y = 0
projectile_dx = 0
projectile_dy = 0

def fire_projectile(x, y, dx, dy):
    global projectile_state, projectile_x, projectile_y, projectile_dx, projectile_dy
    projectile_state = "fire"
    projectile_x = x
    projectile_y = y
    projectile_dx = dx
    projectile_dy = dy

# Missiles

class Missile:
    def __init__(self, index, originX, originY, destinyX, destinyY):
        self.index = index
        self.originX = originX
        self.originY = originY
        self.destinyX = destinyX
        self.destinyY = destinyY
        self.x = originX
        self.y = originY
        self.status = "flying"

missilesList = []

def genMissile():
    if not allDead():
        city = random.choice([c for c in cities if c.status == "alive"])
        m = Missile(city.index, random.randrange(0, 480), 0, city.x + 25, city.y)
        missilesList.append(m)

which_level = 1
missilesSent = 0
points = 0

def resetGame():
    global isAlive, cities, bomb_state, bombRange, bombRadius, playerX, playerY, cont, points, missilesSent, which_level
    global projectile_state

    playerX = 240
    playerY = 160
    bombRange = 50
    bombRadius = 10
    cont = 0
    missilesSent = 0
    which_level = 1
    points = 0
    bomb_state = "ready"
    projectile_state = "ready"

    missilesList.clear()

    isAlive = [True] * 6
    for city in cities:
        city.status = "alive"

cont = 0
clock = pygame.time.Clock()

# Function to handle the splash screen fade-in effect
def show_splash_screen():
    alpha = 0
    splash = pygame.Surface((480, 320))
    splash.blit(splash_image, (20, 0))
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return False
        alpha += 5
        splash.set_alpha(alpha)
        screen.blit(splash, (0, 0))
        pygame.display.flip()
        pygame.time.delay(50)
    return True

# Show the splash screen before starting the game
if not show_splash_screen():
    pygame.quit()
    exit()

# Function to rotate the image around the pivot point
def blit_rotate_center(surf, image, pos, angle, pivot):
    # Calculate the offset vector
    offset_center_to_pivot = pygame.math.Vector2(pivot) - pygame.math.Vector2(image.get_size()) / 2
    # Rotate the offset vector
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    # Get the center of the new rectangle
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    # Rotate the image
    rotated_image = pygame.transform.rotate(image, angle)
    # Get the new rectangle
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    # Blit the rotated image
    surf.blit(rotated_image, rotated_image_rect.topleft)
    return rotated_image_rect

# Main game loop
victory = False
done = False
while not done:
    if not allDead():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and projectile_state == "ready":
                    bombX = playerX
                    bombY = playerY
                    dx = bombX - gun_tip_x
                    dy = bombY - gun_tip_y
                    dist = math.sqrt(dx ** 2 + dy ** 2)
                    fire_projectile(gun_tip_x, gun_tip_y, dx / dist * projectile_speed, dy / dist * projectile_speed)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and playerY >= 3: playerY -= 3
        if pressed[pygame.K_DOWN] and playerY <= 500: playerY += 3
        if pressed[pygame.K_LEFT] and playerX >= 3: playerX -= 3
        if pressed[pygame.K_RIGHT] and playerX <= 792: playerX += 3

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 316, 480, 4))

        # Draw the player base
        base_x = 240
        base_y = 305
        screen.blit(player_base_image, (base_x - player_base_image.get_width() // 2, base_y - player_base_image.get_height() // 2))

        # Calculate the angle between the player position and the player's square position
        dx = playerX - base_x
        dy = playerY - base_y
        angle = math.degrees(math.atan2(-dy, dx))  # Negate dy to correct the angle

        # Add initial rotation of 45 degrees
        initial_rotation = -89.5
        angle += initial_rotation

        # Define the custom pivot point for rotation (coordinates relative to the image)
        pivot_point = (4, 15)  # (x, y) of the red dot in player_gun2.png

        # Rotate the gun image around the custom pivot point (red dot)
        gun_rect = blit_rotate_center(screen, player_gun_image, (base_x + 1, base_y + 3 - pivot_point[1]), angle, pivot_point)

        # Calculate the tip of the gun based on rotation
        gun_tip_x = gun_rect.centerx + math.cos(math.radians(-angle)) + 0
        gun_tip_y = gun_rect.centery - math.sin(math.radians(-angle)) // 2

        # Visualize the gun tip position
        #pygame.draw.circle(screen, (255, 0, 0), (int(gun_tip_x), int(gun_tip_y)), 3)

        if projectile_state == "fire":
            # Draw the projectile
            pygame.draw.circle(screen, projectile_color, (int(projectile_x), int(projectile_y)), 3)
            pygame.draw.line(screen, projectile_color, (gun_tip_x, gun_tip_y), (projectile_x, projectile_y), 1)

            # Move the projectile
            projectile_x += projectile_dx
            projectile_y += projectile_dy

            # Check for collision with the target position
            if math.sqrt((projectile_x - bombX) ** 2 + (projectile_y - bombY) ** 2) < 5:
                bomb_state = "fire"
                bombX = projectile_x
                bombY = projectile_y
                projectile_state = "ready"

        for city in cities:
            if city.status == "alive":
                screen.blit(city.sprite, (city.x, city.y))
            else:
                screen.blit(city.sprite, (city.x, 600))
                isAlive[city.index] = False

        time = levels[which_level - 1].time
        qnt = levels[which_level - 1].qnt
        cont += 1
        auxCont = (time / qnt) / 60
        if cont >= 2.5 * auxCont:
            genMissile()
            missilesSent += 1
            cont = 0

        for m in missilesList:
            if m.status == "flying":
                dx = m.destinyX - m.x
                dy = m.destinyY - m.y
                d = math.sqrt(dx * dx + dy * dy)
                speed = 2
                cx = speed * dx / d
                cy = speed * dy / d
                m.x += cx
                m.y += cy
                angle = math.degrees(math.atan2(dy, dx)) + 90
                rotated_missile = pygame.transform.rotate(missile_image, -angle)
                missile_rect = rotated_missile.get_rect(center=(m.x, m.y))
                screen.blit(rotated_missile, missile_rect.topleft)
                if m.y >= m.destinyY:
                    m.status = "arrived"
                    cities[m.index].status = "dead"
                if (m.x - bombX) * (m.x - bombX) + (m.y - bombY) * (m.y - bombY) < bombRadius * bombRadius:
                    m.status = "blew"
                    points += 50 * which_level
                pygame.draw.line(screen, (0, 255, 0), (m.originX, m.originY), (m.x, m.y))
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(m.x - 2, m.y - 2, 5, 5))

        if missilesSent >= qnt:
            mult = 1
            for city in cities:
                if city.status == "alive":
                    mult += 1
            points *= mult
            if bombRadius > 5:
                bombRadius -= 0.5
            if bombRange > 25:
                bombRange -= 2.5
            which_level += 1

        if which_level > 15:
            done = True
            victory = True

        if bomb_state == "fire":
            bombRadius += 1
            pygame.draw.circle(screen, bombColor, (int(bombX), int(bombY)), bombRadius, 1)
            if bombRadius >= bombRange:
                bombRadius = 10
                bomb_state = "ready"

        pygame.draw.rect(screen, playerColor, pygame.Rect(playerX, playerY, playerWidth, playerHeight))

        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 16)
        text = font.render("Lvl: " + str(which_level), False, (0, 255, 0))
        screen.blit(text, (405, 10))

        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 13)
        text = font.render("pts: " + str(points), False, (0, 255, 0))
        screen.blit(text, (15, 10))

        pygame.display.flip()
        clock.tick(60)
    else:
        screen.fill((0, 0, 0))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 72)
        text = font.render("You Lost", False, (0, 255, 0))
        screen.blit(text, (100, 80))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 22)
        text = font.render("Play again? (Y/N)", False, (0, 255, 0))
        screen.blit(text, (150, 180))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 24)
        text = font.render("points: " + str(points), False, (0, 255, 0))
        screen.blit(text, (160, 230))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    done = True
                if event.key == pygame.K_y:
                    resetGame()
                    done = False

if victory:
    done = False
    while not done:
        screen.fill((0, 0, 0))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 72)
        text = font.render("You Won!", False, (0, 255, 0))
        screen.blit(text, (100, 80))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 22)
        text = font.render("Congratulations!", False, (0, 255, 0))
        screen.blit(text, (150, 180))
        font = pygame.font.Font('modules/atomic-command/Resources/AtariSmall.ttf', 24)
        text = font.render("points: " + str(points), False, (0, 255, 0))
        screen.blit(text, (160, 230))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            if event.type == pygame.KEYDOWN:
                done = True

pygame.quit()
