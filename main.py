import pygame as pg
import time
import random

pg.init()

# --- Global stuff --- #
gameRunning = True
currentScreen = "start"
i = 1
knechtX, knechtY = 0, 0
drawCountdown = True
gamePaused = False

# Timer(s)
clock = pg.time.Clock()

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
toolTipFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 15)

background = pg.image.load("assets/img/background.png").convert_alpha()

# Buildings and Placeholders
mill_placeholder = ["assets/img/farm_placeholder.png", (223, 229)]
mill_build = ["assets/img/mill.png", (525, 527)]
mill = pg.image.load(mill_placeholder[0]).convert_alpha()
mill = pg.transform.scale(mill, mill_placeholder[1])
mill_rect = mill.get_rect(topleft=(-100, -50))

townhall_placeholder = ["assets/img/rathaus_placeholder.png", (575, 433)]
townhall_build = ["assets/img/rathaus.png", (575, 430)]
townhall = pg.image.load(townhall_placeholder[0]).convert_alpha()
townhall = pg.transform.scale(townhall, townhall_placeholder[1])
townhall_rect = townhall.get_rect(topleft=(175, -325))

mine_placeholder = ["assets/img/mine_placeholder.png", (239, 238)]
mine_build = ["assets/img/mine.png", (335, 333)]
mine = pg.image.load(mine_placeholder[0]).convert_alpha()
mine = pg.transform.scale(mine, mine_placeholder[1])
ironMine_rect = mine.get_rect(topleft=(-300 , 125))
goldMine_rect = mine.get_rect(topleft=(100 , 125))

buildings = {
    "mill": [False, mill_rect],
    "townhall": [False, townhall_rect],
    "ironMine": [False, ironMine_rect],
    "goldMine": [False, goldMine_rect],
}

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
    start, startBorder = Button(WIDTH / 2, HEIGHT / 2 - 25, 300, 90, 154, 103, 53, "START", buttonFont, BLACK, 10)
    settings, settingsBorder = Button(WIDTH / 2, HEIGHT / 2 + 100, 300, 90, 154, 103, 53, "SETTINGS", buttonFont, BLACK, 10)
    quit, quitBorder = Button(WIDTH / 2, HEIGHT / 2 + 225, 300, 90, 154, 103, 53, "QUIT", buttonFont, BLACK, 10)
    

    screen.blit(knecht, (x, y))

    return start, startBorder, settings, settingsBorder, quit, quitBorder

### Drawing ToolTip if hovering above building
def drawToolTip(buildingName, buildStatus, x, y):
    toolTipRect = pg.Rect(x, y, 100, 50)
    pg.draw.rect(screen, GRAY, toolTipRect, 0)

    Text(buildingName, toolTipFont, BLACK, x + 50, y, True)

### Drawing the main game screen
def drawGame(countDownLocal):
    screen.blit(background, (0, 0))

    # Drawing all the Placeholders, when countdown ended
    if countDownLocal == False and all(value[0] is False for value in buildings.values()):
        screen.blit(mill, mill_rect)
        screen.blit(townhall, townhall_rect)
        screen.blit(mine, ironMine_rect)
        screen.blit(mine, goldMine_rect)

### Drawing the settings screen
def drawSettings():
    screen.fill(WHITE)
    Text("Dis is settings", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)

def drawPause():
    screen.blit(background, (0,0))
    Text("PAUSE", startMenuFont, BLACK, WIDTH / 2, 250, True)
    resume, resumeBorder = Button(WIDTH / 2, HEIGHT / 2 + 25, 300, 90, 154, 103, 53, "RESUME", buttonFont, BLACK, 10)
    gameQuit, gameQuitBorder = Button(WIDTH / 2, HEIGHT / 2 + 150, 300, 90, 154, 103, 53, "QUIT GAME", buttonFont, BLACK, 10)
    refresh()

    return resume, resumeBorder, gameQuit, gameQuitBorder

# ----------- Game ----------- #
minDirectionX, minDirectionY, maxDirectionX, maxDirectionY, knechtX, knechtY = generateNewDirection()
start, startBorder, settings, settingsBorder, quit, quitBorder = drawStart(knechtX, knechtY)

# Mainloop
while gameRunning:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False

        # Start menu buttons
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePOS = pg.mouse.get_pos()
            mousePOS_X = pg.mouse.get_pos()[0]
            mousePOS_Y = pg.mouse.get_pos()[1]

            if currentScreen == "start":
                if start.collidepoint(mousePOS) or startBorder.collidepoint(mousePOS):
                    countdown = 1
                    drawCountdown = True
                    currentScreen = "game"
                    pg.time.set_timer(ONE_SECOND_EVENT, 1000)
                    drawGame(drawCountdown)
                    print(countdown)

                elif settings.collidepoint(mousePOS) or settingsBorder.collidepoint(mousePOS):
                    currentScreen = "settings"
                    drawSettings()

                elif quit.collidepoint(mousePOS) or quitBorder.collidepoint(mousePOS):
                    gameRunning = False

            elif currentScreen == "game" and gamePaused:
                if resume.collidepoint(mousePOS) or resumeBorder.collidepoint(mousePOS):
                    gamePaused = False

                elif gameQuit.collidepoint(mousePOS) or gameQuitBorder.collidepoint(mousePOS):
                    gamePaused = False
                    currentScreen = "start"

            elif currentScreen == "game":
                for name, value in buildings.items():
                    print(value[1].collidepoint(mousePOS))
                    print(value[1], mousePOS)
                    # if value[1].collidepoint(mousePOS):
                    #     drawToolTip(name, str(value[0]), mousePOS_X, mousePOS_Y)
                    # else:
                    #     pass

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and currentScreen == "settings":
                currentScreen = "start"
            
            elif event.key == pg.K_ESCAPE and currentScreen == "game":
                gamePaused = True

        elif event.type == ONE_SECOND_EVENT and currentScreen == "game" and drawCountdown == True:
            countdown -= 1
            print(countdown)
            if countdown <= 0:
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

        if gamePaused == True:
            resume, resumeBorder, gameQuit, gameQuitBorder = drawPause()


    refresh()
    clock.tick(24)  # ~24 FPS

print("Window closed")