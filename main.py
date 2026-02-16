import pygame as pg
import time
import random

pg.init()

# --- Global stuff --- #
gameRunning = True
currentScreen = "start"
i = 1
knechtX, knechtY = 0, 0
countdown = 3
drawCountdown = True

# Timer(s)
KNECHT_MOVE = pg.event.custom_type()
pg.time.set_timer(KNECHT_MOVE, 200)

ONE_SECOND_EVENT = pg.event.custom_type()

# --- Colors, fonts and images, etc. --- #
info = pg.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
print(WIDTH, "x", HEIGHT, "Pixel")

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Landsknecht - RTS")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

startMenuFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 120)
buttonFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 35)

background = pg.image.load("assets/img/background.png").convert_alpha()

# Buildings and Placeholders
mill_placeholder = pg.image.load("assets/img/farm_placeholder.png").convert_alpha()
mill_placeholder = pg.transform.scale(mill_placeholder, (1000, 1000))

# Hoomans
knecht = pg.image.load("assets/img/knecht.png").convert_alpha()
knecht = pg.transform.scale(knecht, (64, 64))

# --- General stuff --- #
def refresh():
    pg.display.flip()

### Function for drawing Text
def Text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

### Function for drawing Buttons
def Button(X, Y, WIDTH, HEIGHT, colorR, colorG, colorB, text, font, textCOL, Radius):
    borderRect = pg.Rect(0, 0, WIDTH + 20, HEIGHT + 20)
    middleRect = pg.Rect(0, 0, WIDTH, HEIGHT)

    borderRect.center = (X, Y)
    middleRect.center = (X, Y)

    pg.draw.rect(screen, (colorR - 30, colorG - 30, colorB - 30), borderRect, 0, Radius)
    pg.draw.rect(screen, (colorR, colorG, colorB), middleRect, 0, Radius)

    Text(text, font, textCOL, X, Y, True)

    return borderRect, middleRect

### Generating a moving direction for the Landsknecht
def generateNewDirection():
    minDirectionX  = random.randrange(-15, -6)
    minDirectionY = random.randrange(-2, -1)
    maxDirectionX  = random.randrange(6, 10)
    maxDirectionY = random.randrange(1, 2)
    knechtBoyX = random.randrange(0, 1300)
    knechtBoyY = random.randrange(0, 800)
    return minDirectionX, minDirectionY, maxDirectionX, maxDirectionY, knechtBoyX, knechtBoyY

# --- Drawing Functions --- #
### Drawing the starting screen
def drawStart(x, y):
    screen.blit(background, (0,0))
    Text("LANDSKNECHT", startMenuFont, BLACK, WIDTH / 2, 250, True)
    start, startBorder = Button(WIDTH / 2, HEIGHT / 2 + 20, 250, 90, 150, 150, 150, "START", buttonFont, BLACK, 10)
    settings, settingsBorder = Button(WIDTH / 2, HEIGHT / 2 + 200, 250, 90, 150, 150, 150, "SETTINGS", buttonFont, BLACK, 10)

    screen.blit(knecht, (x, y))

    return start, startBorder, settings, settingsBorder

### Drawing the main game screen
def drawGame(countDownLocal):
    screen.blit(background, (0, 0))

    # Drawing all the Placeholders, when countdown ended
    if countDownLocal == False:
        screen.blit(mill_placeholder, (WIDTH / 2, HEIGHT / 2))

### Drawing the settings screen
def drawSettings():
    screen.fill(WHITE)
    Text("Dis is settings", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)

# ----------- Game ----------- #
minDirectionX, minDirectionY, maxDirectionX, maxDirectionY, knechtX, knechtY = generateNewDirection()
start, startBorder, settings, settingsBorder = drawStart(knechtX, knechtY)

# Mainloop
while gameRunning:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePOS = pg.mouse.get_pos()
            if currentScreen == "start":
                if start.collidepoint(mousePOS) or startBorder.collidepoint(mousePOS):
                    currentScreen = "game"
                    pg.time.set_timer(ONE_SECOND_EVENT, 1000)
                    drawGame(drawCountdown)
                elif settings.collidepoint(mousePOS) or settingsBorder.collidepoint(mousePOS):
                    currentScreen = "settings"
                    drawSettings()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and currentScreen == "settings":
                currentScreen = "start"

        elif event.type == ONE_SECOND_EVENT and currentScreen == "game":
            countdown -= 1

        elif countdown <= 0:
            time.sleep(.2)
            drawCountdown = False

        # Landsknecht logic 
        elif currentScreen == "start" and event.type == KNECHT_MOVE:
            knechtX += random.randrange(minDirectionX, maxDirectionX)
            knechtY += random.randrange(minDirectionY, maxDirectionY)

            if knechtX <= 0 or knechtX >= 1400:
                knechtX = random.randrange(0, 1400)
                knechtY= random.randrange(0, 800)

                minDirectionX, minDirectionY, maxDirectionX, maxDirectionY, knechtX, knechtY = generateNewDirection()

            if knechtY <= 0 or knechtY >= 1400:
                knechtX = random.randrange(0, 1400)
                knechtY= random.randrange(0, 800)

                minDirectionX, minDirectionY, maxDirectionX, maxDirectionY, knechtX, knechtY = generateNewDirection()

    # Draw
    screen.fill((0,0,0))
    if currentScreen == "start":
        drawStart(knechtX, knechtY)
    elif currentScreen == "settings":
        drawSettings()
    elif currentScreen == "game":
        drawGame(drawCountdown)
        if drawCountdown == True:
            Text("Game starts in: " + str(countdown), startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)

    refresh()
    pg.time.Clock().tick(24)  # ~24 FPS