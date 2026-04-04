import pygame as pg
import random
import os
import sys

pg.init()

def resource_path(relative_path):
    """ Pfade für Entwicklung + EXE (PyInstaller) """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

    # Powershell command: 
    # python -m PyInstaller --onefile --windowed --name "Landsknecht" --add-data "assets;assets" main.py

# --- Global stuff --- #
gameRunning = True
currentScreen = "start"
FPS = 60
knechtX, knechtY = 0, 0
drawCountdown = True
gamePaused = False
hoverText = None

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
LIGHTGRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

startMenuFont = pg.font.Font(resource_path("assets/fonts/UncialAntiqua-Regular.ttf"), 120)
buttonFont = pg.font.Font(resource_path("assets/fonts/UncialAntiqua-Regular.ttf"), 35)
toolTipFont_M = pg.font.Font(resource_path("assets/fonts/UncialAntiqua-Regular.ttf"), 15)
toolTipFont_L = pg.font.Font(resource_path("assets/fonts/UncialAntiqua-Regular.ttf"), 25)

background = pg.image.load(resource_path("assets/img/background.png")).convert_alpha()

# Buildings and Placeholders
mill_placeholder = [resource_path("assets/img/farm_placeholder.png"), (229 / 2, 228 / 2)]
mill_build = [resource_path("assets/img/mill.png"), (525 / 2, 527 / 2)]
mill = pg.image.load(mill_placeholder[0]).convert_alpha()
mill = pg.transform.scale(mill, mill_placeholder[1])
mill_rect = mill.get_rect(topleft=(290, 350))

townhall_placeholder = [resource_path("assets/img/rathaus_placeholder.png"), (575 / 2, 433 / 2)]
townhall_build = [resource_path("assets/img/rathaus.png"), (575 / 2, 430 / 2)]
townhall = pg.image.load(townhall_placeholder[0]).convert_alpha()
townhall = pg.transform.scale(townhall, townhall_placeholder[1])
townhall_rect = townhall.get_rect(topleft=(200, 50))

mine_placeholder = [resource_path("assets/img/mine_placeholder.png"), (239 / 2, 238 / 2)]
mine_build = [resource_path("assets/img/mine.png"), (335 / 2, 333 / 2)]
mine = pg.image.load(mine_placeholder[0]).convert_alpha()
mine = pg.transform.scale(mine, mine_placeholder[1])
ironMine_rect = mine.get_rect(topleft=(45, 350))
goldMine_rect = mine.get_rect(topleft=(535, 350))

knights_placeholder = [resource_path("assets/img/knight_barracks_placeholder.png"), (192 * 1.5, 174 * 1.5)]
knights_build = [resource_path("assets/img/knight_barracks.png"), (767 / 2, 700 / 2)]
knights = pg.image.load(knights_placeholder[0]).convert_alpha()
knights = pg.transform.scale(knights, knights_placeholder[1])
knights_rect = knights.get_rect(topleft=(450, 525))

archers_placeholder = [resource_path("assets/img/archrers_placeholder.png"), (190 * 1.5, 142 * 1.5)]
archers_build = [resource_path("assets/img/archers.png"), (191 * 1.5, 141 * 1.5)]
archers = pg.image.load(archers_placeholder[0]).convert_alpha()
archers = pg.transform.scale(archers, archers_placeholder[1])
archers_rect = archers.get_rect(topleft=(50, 550))

buildings = {
    "Mill": [False, mill_rect, 0, "Passive", 100],
    "Townhall": [False, townhall_rect, 0, "Passive", 100],
    "Iron Mine": [False, ironMine_rect, 0, "Passive", 100],
    "Gold Mine": [False, goldMine_rect, 0, "Passive", 100],
    "Knight Barrack": [False, knights_rect, 0, "Passive", 100],
    "Archer Barrack": [False, archers_rect, 0, "Passive", 100]
}

# Hoomans
knecht = pg.image.load(resource_path("assets/img/knecht.png")).convert_alpha()
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
def drawToolTip(buildingName, buildStatus, level, workingStatus, health, x, y):
    toolTipSurface = pg.Surface((250, 155))
    toolTipSurface.set_alpha(225)
    toolTipSurface.fill(LIGHTGRAY)
    screen.blit(toolTipSurface, (x - 125, y - 25))

    Text(buildingName, toolTipFont_L, BLACK, x, y, True)
    Text(f"Build: {buildStatus}", toolTipFont_M, BLACK, x, y + 35, True)
    Text(f"Level: {level}", toolTipFont_M, BLACK, x, y + 60, True)
    Text(f"Status: {workingStatus}", toolTipFont_M, BLACK, x, y + 85, True)
    Text(f"Health: {health}", toolTipFont_M, BLACK, x, y + 110, True)

### Drawing the main game screen
def drawGame(countDownLocal):
    screen.blit(background, (0, 0))

    # Drawing all the Placeholders, when countdown ended
    if countDownLocal == False and all(value[0] is False for value in buildings.values()):
        screen.blit(mill, mill_rect)
        screen.blit(townhall, townhall_rect)
        screen.blit(mine, ironMine_rect)
        screen.blit(mine, goldMine_rect)
        screen.blit(knights, knights_rect)
        screen.blit(archers, archers_rect)

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

        # Tooltip
        elif event.type == pg.MOUSEMOTION and not drawCountdown and not gamePaused:  
            mousePOS = pg.mouse.get_pos() 
            mousePOS_X = pg.mouse.get_pos()[0]
            mousePOS_Y = pg.mouse.get_pos()[1]        
            hoverText = None

            if currentScreen == "game":
                for name, value in buildings.items():
                    if value[1].collidepoint(mousePOS):
                        hoverText = name
                        hoverValue = value
                        break


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

        if hoverText:
            drawToolTip(hoverText, hoverValue[0], hoverValue[2], hoverValue[3], hoverValue[4], mousePOS_X, mousePOS_Y)

    refresh()
    clock.tick(FPS)  # FPS

print("Window closed")