import pygame as pg

from constants import *
from poketer import Poketer
from intro_screens import FirstScreen, PoketerIntroScreen

start_screen = None


def text_speech(screen, font: str, size: int, text: str, color, x, y, bold: bool):
    font = pg.font.Font(font, size)
    font.set_bold(bold)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

#
# def glada_gunnar(x, y, name_relx, name_rely, stats_relx, stats_rely):
#     screen.blit(gunnar.image, (x, y))
#     name = TextBox((name_relx, name_rely), 18, False, LIGHT_GREEN, f"{gunnar.name}")
#     stats = TextBox((stats_relx, stats_rely), 18, False, WHITE,
#                     f"Attack: {gunnar.attack} Health: {gunnar.health}")
#     return name, stats
#
#
# def aggressive_ada(x, y, name_relx, name_rely, stats_relx, stats_rely):
#     screen.blit(ada.image, (x, y))
#     name = TextBox((name_relx, name_rely), 18, False, LIGHT_PINK, f"{ada.name}")
#     stats = TextBox((stats_relx, stats_rely), 18, False, WHITE,
#                     f"Attack: {ada.attack} Health: {ada.health}")
#     return name, stats


def left_chat_bubble(mood_score):
    left_bubble = pg.image.load("media/images/Chat_bubble_left.png")
    left_bubble = pg.transform.scale(left_bubble, (300, 170))
    screen.blit(left_bubble, (250, 50))
    text_speech(screen, "fonts/RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 390, 135, True)


def right_chat_bubble(mood_score):
    right_bubble = pg.image.load("media/images/Chat_bubble_right.png")
    right_bubble = pg.transform.scale(right_bubble, (300, 170))
    screen.blit(right_bubble, (260, 350))
    text_speech(screen, "fonts/RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 370, 435, True)


def pop_up_bubbles(state, gunnar_mood_score, ada_mood_score):
    if state == "one click":
        left_chat_bubble(gunnar_mood_score)

    if state == "two clicks":
        left_chat_bubble(gunnar_mood_score)
        right_chat_bubble(ada_mood_score)


def battle_time_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 240 and 245 <= mouse[1] <= 225 + 100:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (287, 247, 221, 66))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, WIDTH / 2.02,
                    HEIGHT / 2.15, True)
    else:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (287, 247, 221, 66))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, WIDTH / 2.02,
                    HEIGHT / 2.15, True)


def quit_button():
    mouse = pg.mouse.get_pos()
    if 650 <= mouse[0] <= 650 + 140 and 30 <= mouse[1] <= 30 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [652, 32, 137, 37])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 25, "QUIT", BLACK, 715, 48, True)
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [650, 30, 140, 40])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 25, "QUIT", BLACK, 715, 48, True)


def back_button():
    mouse = pg.mouse.get_pos()
    if 30 <= mouse[0] <= 30 + 140 and 540 <= mouse[1] <= 540 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)


def start_game_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 225 and 280 <= mouse[1] <= 280 + 65:
        pg.draw.rect(screen, BLACK, (275, 280, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 282, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Start Game", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.93, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 280, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 282, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Start Game", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.93, True)


def instructions_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 240 and 360 <= mouse[1] <= 360 + 65:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 362, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "How To Play", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.54, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 362, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "How To Play", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.54, True)


def quit_button_start():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 225 and 440 <= mouse[1] <= 440 + 65:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 442, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.27, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 442, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, WIDTH / 2.025,
                    HEIGHT / 1.27, True)





def mainloop(screen):
    # To be able to go back to startscreen and run popups if not run before
    # global start_screen
    # start_screen = StartScreen()

    state = FirstScreen()
    #state = PoketerIntroScreen()

    clock = pg.time.Clock()
    while True:
        # Event handling
        ev = pg.event.poll()

        if ev.type == pg.KEYDOWN:
            state = state.handle_keydown(ev.key)

        if ev.type == pg.MOUSEBUTTONDOWN:
            temp_state = state.handle_mouse_button(ev.button)
            if temp_state is not None:
                state = temp_state

        elif ev.type == pg.QUIT:
            break

        state = state.handle_timer()
        state.render(screen)

        pg.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)

    pg.display.set_caption("PokeMood")
    programIcon = pg.image.load('media/images/icon.png')
    icon = pg.transform.smoothscale(programIcon, (32, 32))
    pg.display.set_icon(icon)
    gunnar = Poketer("Happy Hasse", 'happy', 'yellow', 50, 45, catchword="#YOLO",
                     img_name="media/images/Green_monster_resized.png")
    ada = Poketer("Aggressive Ada", 'angry', 'red', 50, 45, catchword="#FTW",
                  img_name="media/images/Pink_dragon_01.png")
    mainloop(screen)
    pg.quit()
