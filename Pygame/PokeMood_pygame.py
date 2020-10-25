import pygame as pg
from pathlib import Path
from Pygame.constants import WHITE, BLACK, BLUE, RED, YELLOW, GREEN

pg.init()

display_width = 800
display_height = 600

screen = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Demo - PokeMood')

clock = pg.time.Clock()
crashed = False

font_path = Path("RobotoSlab-Medium.ttf")

surface_bg = pg.Surface((800, 600))


def addRect():
    pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
    pg.display.update()


def text_speech(font: str, size: int, text: str, color, x, y, bold: bool):
    font = pg.font.Font(font, size)
    font.set_bold(bold)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def Aggressive_Ada(x, y):
    pink_dragon = pg.image.load('Pink_dragon_01.png').convert_alpha()
    screen.blit(pink_dragon, (x, y))


def Happy_Hasse(x, y):
    green_monster = pg.image.load('Green_monster_resized.png').convert_alpha()
    screen.blit(green_monster, (x, y))


def chat_bubble_left():
    image = pg.image.load('Chat_bubble_left.png')
    chat_bubble_small = pg.transform.scale(image, (300, 170))
    screen.blit(chat_bubble_small, (250, 50))


def chat_bubble_right():
    image = pg.image.load('Chat_bubble_right.png')
    chat_bubble_small = pg.transform.scale(image, (300, 170))
    screen.blit(chat_bubble_small, (260, 350))


def background():
    bg = pg.image.load("Background_forest.jpg").convert_alpha()
    bg_bigger = pg.transform.scale(bg, (800, 600))
    surface_bg.blit(bg_bigger, (0,0))


def demoscreen():
    Aggressive_Ada(display_width * 0.65, display_height * 0.5)
    Happy_Hasse(display_width * 0.01, display_width * 0.05)
    chat_bubble_left()
    chat_bubble_right()
    text_speech("RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, display_width / 2.02, display_height / 2.15, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Aggressive Ada", RED, 640, 300, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Happy Hasse", BLUE, 122, 45, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Moodscore: 123", BLACK, 370, 435, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Moodscore: 113", BLACK, 390, 135, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Stats: HP: 123, Attack: 20, Mood: Angry", WHITE, 630, 575, True)
    text_speech("RobotoSlab-Medium.ttf", 15, "Stats: HP: 113, Attack: 20, Mood: Happy", WHITE, 170, 20, True)
    addRect()


while not crashed:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True

    screen.fill(WHITE)
    screen.blit(surface_bg, (0,0))
    background()
    demoscreen()
    pg.display.update()
    clock.tick(100)

pg.quit()
quit()
