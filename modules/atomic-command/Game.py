# Import pygame library
import pygame
# Import random library (used for generating missiles)
import random
# Import math library (used for square root method)
import math

# Initiates pygame
pygame.init()
# Set main screen's dimensions
screen = pygame.display.set_mode((480, 320))

# Load the missile image
missile_image = pygame.image.load('./Resources/bomb.png')
missile_image = pygame.transform.scale(missile_image, (20, 20))  # Scale it to a proper size

# Load the player image
player_image = pygame.image.load('./Resources/player.png')
player_image = pygame.transform.scale(player_image, (40, 47))  # Scale it to a proper size

# Load the city images
city_images = [
    pygame.image.load('./Resources/bridge.png'),
    pygame.image.load('./Resources/nukaworld.png'),
    pygame.image.load('./Resources/empire.png'),
    pygame.image.load('./Resources/capitol.png'),
    pygame.image.load('./Resources/statue.png'),
    pygame.image.load('./Resources/vegas.png')
]

for i in range(len(city_images)):
    city_images[i] = pygame.transform.scale(city_images[i], (35, 42))  # Adjust the size as needed

#Levels

# Class for level storage:
## self.lvl    Which level it is
## self.time   Total amount of time the player has to survive for
## self.qnt    Quantity of missiles in the determined amount of time
class Level:
    def __init__(self, lvl, time, qnt):
        self.lvl = lvl
        self.time = time
        self.qnt = qnt

# Creating all of the Level objects
lvl1 = Level(1, 60000, 12)
lvl2 = Level(2, 60000, 18)
lvl3 = Level(3, 60000, 24)
lvl4 = Level(4, 60000, 30)
lvl5 = Level(5, 60000, 36)
lvl6 = Level(6, 60000, 42)
lvl7 = Level(7, 60000, 48)
lvl8 = Level(8, 60000, 54)
lvl9 = Level(9, 60000, 60)
lvl10 = Level(10, 60000, 66)
lvl11 = Level(11, 60000, 72)
lvl12 = Level(12, 60000, 78)
lvl13 = Level(13, 60000, 84)
lvl14 = Level(14, 60000, 90)
lvl15 = Level(15, 60000, 96)
lvl16 = Level(16, 60000, 102)
lvl17 = Level(17, 60000, 108)
lvl18 = Level(18, 60000, 114)
lvl19 = Level(19, 60000, 120)
lvl20 = Level(20, 60000, 126)

# Add every level to the levels list
levels = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10, lvl11, lvl12, lvl13, lvl14, lvl15, lvl16, lvl17, lvl18, lvl19, lvl20]


# City

# Fixed variables for the cities
#cityColor = (0,255,0)
#ruinsColor = (0, 155, 0)

# Class for city storage:
## self.index         Index for the current city
## self.x and self.y  Coordinates for the city
## self.status        Status (alive or dead) of the city
class City:
    def __init__(self, index, x, sprite):
        self.index = index
        self.x = x
        self.y = 278
        self.status = "alive"
        self.sprite = sprite

# Creating all of the cities objects with sprites
city1 = City(0, 40, city_images[0])
city2 = City(1, 80, city_images[1])
city3 = City(2, 120, city_images[2])
city4 = City(3, 340, city_images[3])
city5 = City(4, 380, city_images[4])
city6 = City(5, 420, city_images[5])
# Add every city in the list
cities = [city1, city2, city3, city4, city5, city6]

# Variable for city status verification
isAlive = [True, True, True, True, True, True]

## Function return boolean if every single city isn't alive
def allDead():
    for cityStatus in isAlive:
        if cityStatus == True:
            return False
    return True

# Player

# Fixed variables
playerColor = (0,255,0)
playerHeight = 8
playerWidth = 8

# Player coordinates
playerX = 240
playerY = 160

# Bomb

# Fixed variables
bombColor = (0,255,0)

# Bomb's explosion current radius
bombRadius = 10

# Max explosion range
bombRange = 50

# Bomb state
bomb_state = "ready"

# Bomb coordinates
bombX = playerX
bombY = playerY

# Function that draws the bomb when fired:
## x and y  Bomb current coordinates (usually bombX and bombY)
## r        Bomb current radius (usually bombRadius)
def fire_bomb(x, y, r):
    # Sets the bomb state to "fire" (it's firing currently)
    global bomb_state
    bomb_state = "fire"
    pygame.draw.circle(screen, bombColor, (x, y), r, 1)

# Missiles

# Class for missile storage:
## self.index                        This missile's index
## self.originX and self.originY     Missile's departure point's coordinates
## self.destinyX and self.destinyY   Missile's destiny's coordinates
## self.x and self.y                 Current position
## self.status                       Current status
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

# List of all of the current missiles
missilesList = []

# Function for creating a new missile
def genMissile():
    # If there's still cities alive
    if not allDead():
        # Gets a random city from the list
        city = random.randrange(0,len(cities))
        # Keeps on until finds a city that is alive (since there's at least one of them)
        while cities[city].status != "alive":
            city = random.randrange(0,len(cities))
        # Create the missile with a random origin coordinates
        m = Missile(city, random.randrange(0,480), 0,cities[city].x+25, cities[city].y)
        # Adds the missile to the list
        missilesList.append(m)

# Level control
witch_level = 1
missilesSent = 0
points = 0

# Reset function prepares all of the variables for a new game
def resetGame():
    global isAlive
    global cities
    global bomb_state, bombRange, bombRadius
    global playerX, playerY, cont, points, missilesSent, witch_level

    playerX = 240
    playerY = 160
    bombRange = 50
    bombRadius = 10
    cont = 0
    missilesSent = 0
    witch_level = 1
    points = 0
    bomb_state = "ready"

    missilesList.clear()

    for x in range(len(isAlive)):
        isAlive[x] = True

    for city in cities:
        city.status = "alive"

# Main
cont = 0
clock = pygame.time.Clock()

# Loop control variables
victory = False
done = False
while not done:
    # If there's still cities alive
    if not allDead():
        for event in pygame.event.get():
                # Quits of the game
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                    # Fires the bomb
                    if event.key == pygame.K_SPACE:
                        if bomb_state != "fire":
                            bombX = playerX
                            bombY = playerY
                            fire_bomb(bombX, bombY, bombRadius)

        # Movement handler
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and playerY >= 3: playerY -= 3
        if pressed[pygame.K_DOWN] and playerY <= 500: playerY += 3
        if pressed[pygame.K_LEFT] and playerX >= 3: playerX -= 3
        if pressed[pygame.K_RIGHT] and playerX <= 792: playerX += 3

        # Erases all
        screen.fill((0, 0, 0))
        # Draws floor
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(0,320,480,320))
        # Draws the main base
        #pygame.draw.rect(screen, (0,155,0), pygame.Rect(200, 280, 80,40))
        #pygame.draw.rect(screen, (0,255,0), pygame.Rect(220, 260, 40,80))

        screen.blit(player_image, (200, 280))
        # Draw all of the cities
        for city in cities:
            # Draw the city sprite
            if city.status == "alive":
                screen.blit(city.sprite, (city.x, city.y))
            else:
                # Optionally, you can have a different sprite for ruined cities
                screen.blit(city.sprite, (city.x, 600))
                isAlive[city.index] = False
        # Generates the missiles
        time = levels[witch_level].time
        qnt = levels[witch_level].qnt
        cont += 1
        auxCont = ( time / qnt ) / 60
        if cont >= 2.5*auxCont:
            genMissile()
            missilesSent += 1
            cont = 0

        # Draws every missile in the list
        for m in missilesList:
            if m.status == "flying":
                dx = m.destinyX - m.x
                dy = m.destinyY - m.y

                # Gets the hypotenuse
                d = math.sqrt(dx*dx + dy*dy)

                # Calculate the change to the enemy position
                speed = 2
                cx = speed * dx / d
                cy = speed * dy / d

                # Update enemy position
                m.x += cx
                m.y += cy

                # Calculate the angle of the missile
                angle = math.degrees(math.atan2(dy, dx)) + 90
                rotated_missile = pygame.transform.rotate(missile_image, -angle)

                # Center the missile image on its current position
                missile_rect = rotated_missile.get_rect(center=(m.x, m.y))

                # Draw the missile
                screen.blit(rotated_missile, missile_rect.topleft)

                # Arrived on destiny
                if m.y >= m.destinyY:
                    m.status = "arrived"
                    cities[m.index].status = "dead"

                # Blew up
                if (m.x - bombX)*(m.x - bombX) + (m.y - bombY)*(m.y - bombY) < bombRadius*bombRadius:
                    m.status = "blew"
                    points += 50*witch_level

                # Missile trail
                pygame.draw.line(screen, (0,255,0), (m.originX, m.originY), (m.x, m.y))
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(m.x-2, m.y-2, 5,5))

        # Detecs colisions between the cities, the bomb an the missiles AND add the points to the score
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
            witch_level += 1

        # Victory stablished
        if witch_level > 15:
            done = True
            victory = True

        # Handles bomb animation and reloading
        if bomb_state == "fire":
            bombRadius = bombRadius + 1
            if bombRadius <= 14:
                pygame.draw.line(screen, (0,255,0), (bombX, bombY), (240,280))
            fire_bomb(bombX, bombY, bombRadius)
            if bombRadius >= bombRange:
                bombRadius = 10
                bomb_state = "ready"

        # Draws the player
        pygame.draw.rect(screen, playerColor, pygame.Rect(playerX, playerY, playerWidth, playerHeight))

        # Writes the display
        font = pygame.font.Font('./Resources/AtariSmall.ttf', 16)
        text = font.render("Lvl: " + str(witch_level), False, (0,255,0))
        screen.blit(text, (405, 40))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 13)
        text = font.render("pts: " + str(points), False, (0,255,0))
        screen.blit(text, (405, 54))

        pygame.display.flip()
        clock.tick(60)
    else:
        # "YOU LOST" scenario

        # Erases all
        screen.fill((0, 0, 0))

        # Writes all of the messages and your score
        font = pygame.font.Font('./Resources/AtariSmall.ttf', 72)
        text = font.render("You Lost", False, (0,255,0))
        screen.blit(text, (100, 80))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 22)
        text = font.render("Play again? (Y/N)", False, (0,255,0))
        screen.blit(text, (150, 180))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 24)
        text = font.render("points: " + str(points), False, (0,255,0))
        screen.blit(text, (160, 230))

        pygame.display.flip()
        clock.tick(60)

        # Waits for command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    done = True
                if event.key == pygame.K_y:
                    resetGame()
                    done = False
if victory:
    # "YOU WIN" scenario

    # Ends main loop
    done = False
    while not done:
        # Writes message
        screen.fill((0, 0, 0))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 72)
        text = font.render("You Won!", False, (0,255,0))
        screen.blit(text, (100,80))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 22)
        text = font.render("Congratulations!", False, (0,255,0))
        screen.blit(text, (150,180))

        font = pygame.font.Font('./Resources/AtariSmall.ttf', 24)
        text = font.render("points: " + str(points), False, (0,255,0))
        screen.blit(text, (160,230))

        pygame.display.flip()
        clock.tick(60)

        # Wait for command to exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                done = True
