import pygame as pg
from random import randint
import sys
import math
from Pygame.constants import *
from mood_score import calc_mood_score
from quiz import QuizStartScreen
from quiz_api import quiz_categories
from pygame import mixer

import common
#common.common_init()

from common import TextBox, periodic_movement

pg.init()
width = 800
height = 600
screen = pg.display.set_mode((width, height))

bg = pg.image.load("Background_forest.jpg")
background = pg.transform.scale(bg, (800, 600))

vs_sign = pg.image.load("VS.PNG")
vs_sign = pg.transform.scale(vs_sign, (200, 150))

background_win = pg.image.load("winning_pic.jpg")
background_win = pg.transform.scale(background_win, (800, 600))

logo = pg.image.load("LOGO.PNG")
logo = pg.transform.scale(logo, (360, 222))

start_background = pg.image.load("background_start.png")
start_background = pg.transform.scale(start_background, (800, 600))

instructions_frame = pg.image.load("Frame_background.PNG")
instructions_frame = pg.transform.scale(instructions_frame, (650, 450))


def text_speech(screen, font: str, size: int, text: str, color, x, y, bold: bool):
    font = pg.font.Font(font, size)
    font.set_bold(bold)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


class Poketer:
    def __init__(self, name, mood, color, health, max_health, attack, catchword, img_name):
        self.name = name
        self.mood = mood
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.color = color
        self.catchword = catchword
        self.image = pg.image.load(img_name).convert_alpha()

    def add_health(self, health_score):
        health = self.health + health_score
        return health
        #self.health += health_score
        #return self.health

    def add_max_health(self, max_health_score):
        self.max_health += max_health_score
        return self.max_health


gunnar = Poketer("Glada Gunnar", 'happy', 'yellow', 50, 50, 45, catchword="#YOLO", img_name="Green_monster_resized.png")
ada = Poketer("Aggressiva Ada", 'angry', 'red', 50, 50, 45, catchword="#FTW", img_name="Pink_dragon_01.png")


def update_max_health(poketer, city):
    mood_score = calc_mood_score(poketer.mood, city, live=False)
    health_with_mood_score = poketer.add_health(mood_score)
    return health_with_mood_score


active_health_gunnar = int(update_max_health(gunnar, 'Göteborg'))
active_health_ada = int(update_max_health(ada, 'Västerås'))


def attack_function(poketer):
    global active_health_ada
    global active_health_gunnar
    if poketer is gunnar:
        result = int(active_health_ada - gunnar.attack)
        active_health_ada = result
        return active_health_ada
    if poketer is ada:
        result = int(active_health_gunnar - ada.attack)
        active_health_gunnar = result
        return active_health_gunnar


def special_attack(poketer):
    global active_health_ada
    global active_health_gunnar
    misschans = randint(1, 6)
    if poketer is gunnar:
        if misschans <= 2:
            result = active_health_ada - gunnar.attack * 2
            active_health_ada = result
            return active_health_ada
        else:
            return active_health_ada

    if poketer is ada:
        if misschans <= 2:
            result = active_health_gunnar - ada.attack * 2
            active_health_gunnar = result
            return active_health_gunnar
        else:
            return active_health_gunnar


def cpu_random_attack():
    random_number = randint(1, 11)
    if random_number <= 7:
        return True
    if random_number >= 8:
        return False


class MenuStartScreen:
    def __init__(self):
        self.music = music_intro()
    def handle_keydown(self, key):
        if key == pg.K_SPACE:
            pass
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        start_game_button_rect = pg.Rect(275, 280, 240, 65)
        instructions_button_rect = pg.Rect(275, 360, 240, 65)
        quit_game_button_rect = pg.Rect(275, 440, 240, 65)
        if button == 1:
            if start_game_button_rect.collidepoint((mx, my)):
                return StartScreen()
            if instructions_button_rect.collidepoint((mx, my)):
                return InstructionsScreen()
            if quit_game_button_rect.collidepoint((mx, my)):
                sys.exit()

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_background, (0, 0))
        screen.blit(logo, (215, -55))
        start_game_button()
        instructions_button()
        quit_button_start()


class InstructionsScreen:
    def handle_keydown(self, key):
        if key == pg.K_SPACE:
            pass
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        back_button_rect = pg.Rect(30, 540, 140, 40)
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return MenuStartScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_background, (0, 0))
        screen.blit(instructions_frame, (75, 75))
        back_button()
        quit_button()


class StartScreen:
    def __init__(self):
        #self.music = music_intro()
        print(self)

    def handle_keydown(self, key):
        if key == pg.K_SPACE:
            pass
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        battle_button_rect = pg.Rect(285, 245, 225, 70)
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        if button == 1:
            if battle_button_rect.collidepoint((mx, my)):
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        aggressive_ada(520, 300, 640, 300, active_health_ada)
        glada_gunnar(8, 30, 122, 45, active_health_gunnar)
        pop_up_bubbles(button)
        battle_time_button()
        quit_button()
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Press [enter] for moodscores", BLACK, 397, 330, True)


text_ada = ""
text_gunnar = ""
class BattleScreen:
    def __init__(self):
        self.music = music_battle()
        print(self)

    def handle_keydown(self, key):
        if key == pg.K_BACKSPACE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        global text_ada
        global text_gunnar
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        back_button_rect = pg.Rect(30, 540, 140, 40)
        attack_button_rect = pg.Rect(87, 430, 150, 50)
        block_button_rect = pg.Rect(325, 430, 150, 50)
        quiz_button = pg.Rect(563, 430, 150, 50)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            if back_button_rect.collidepoint((mx, my)):
                return StartScreen()
            if attack_button_rect.collidepoint((mx, my)):
                return AttackScreen("user")

            if block_button_rect.collidepoint((mx, my)):
                return SpecialAttackScreen("user")

            if quiz_button.collidepoint((mx, my)):
                common.next_screen = QuizStartScreen(5, quiz_categories, self, gunnar)

        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        global text_ada
        global text_gunnar

        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        x_off, y_off = periodic_movement(1, 5)
        aggressive_ada(504 + x_off, 156, 650, 550, active_health_ada)
        glada_gunnar(24, 144 + y_off, 122, 45, active_health_gunnar)

        screen.blit(vs_sign, (300, 225))
        quit_button()
        back_button()
        attack_button()
        special_attack_button()
        quiz_button()
        textbox_gunnar = TextBox((0.5, 0.2), "RobotoSlab-Medium.ttf", 30, False, WHITE, "It's your turn!")
        textbox_gunnar.render(screen)


class AttackScreen:
    def __init__(self, turn_):
        print(self, turn_)
        self.turn = turn_
        self.timeout = pg.time.get_ticks()

        global text_gunnar, text_ada
        if self.turn == "user":
            attack_function(gunnar)
            text_gunnar = f"Gunnar attacked Ada! Ada took {gunnar.attack} in damage!"
            text_ada = ""
        else:
            attack_function(ada)
            text_ada = f"Ada attacked Gunnar! You took {ada.attack} in damage!"
            text_gunnar = ""

    global active_health_ada
    global active_health_gunnar

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):

        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        back_button_rect = pg.Rect(30, 540, 140, 40)

        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            return self

    def handle_timer(self):

        time_now = pg.time.get_ticks()
        if time_now - self.timeout > 2500 and self.timeout != 0:
            self.timeout = 0

            if active_health_ada <= 0:
                return WinnerScreenGunnar()
            if active_health_gunnar <= 0:
                return WinnerScreenAda()

            # when the users attack is finished - let cpu make a move
            if self.turn == "user":
                if cpu_random_attack():
                    return AttackScreen("cpu")
                else:
                    return SpecialAttackScreen("cpu")

            # when the cpu's attack is finished - return to Battlescreen
            if self.turn == "cpu":
                return BattleScreen()

        return self

    def render(self, screen):
        global text_ada
        global text_gunnar
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        textbox_gunnar = TextBox((0.5, 0.2), "RobotoSlab-Medium.ttf", 25, False, YELLOW, text_gunnar)
        textbox_gunnar.render(screen)

        textbox_ada = TextBox((0.5, 0.2), "RobotoSlab-Medium.ttf", 25, False, RED, text_ada)
        textbox_ada.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        aggressive_ada(504, 156 + y_off, 650, 550, active_health_ada)
        glada_gunnar(24 + x_off, 144, 122, 45, active_health_gunnar)
        quit_button()
        back_button()

        # Rotate sword depending on whose turn it is
        sword(self.turn)


class SpecialAttackScreen:
    def __init__(self, turn_):
        print(self)
        self.turn = turn_
        self.timeout = pg.time.get_ticks()

        global text_gunnar, text_ada
        if self.turn == "user":
            special_attack(gunnar)
            text_gunnar = f"Gunnar special attacked Ada! Ada took {gunnar.attack} in damage!"
            text_ada = ""
        else:
            special_attack(ada)
            text_ada = f"Ada special attacked Gunnar! You took {ada.attack} in damage!"
            text_gunnar = ""

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        global text_ada
        global text_gunnar
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        back_button_rect = pg.Rect(30, 540, 140, 40)

        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
        return self

    def handle_timer(self):

        time_now = pg.time.get_ticks()
        if time_now - self.timeout > 2500 and self.timeout != 0:
            self.timeout = 0

            if active_health_ada <= 0:
                return WinnerScreenGunnar()
            if active_health_gunnar <= 0:
                return WinnerScreenAda()

            # when the users attack is finished - let cpu make a move
            if self.turn == "user":
                if cpu_random_attack():
                    return AttackScreen("cpu")
                else:
                    return SpecialAttackScreen("cpu")

            # when the cpu's attack is finished - return to Battlescreen
            if self.turn == "cpu":
                return BattleScreen()

        return self

    def render(self, screen):
        global text_ada
        global text_gunnar
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        textbox_gunnar = TextBox((0.5, 0.2), "RobotoSlab-Medium.ttf", 25, False, YELLOW, text_gunnar)
        textbox_gunnar.render(screen)

        textbox_ada = TextBox((0.5, 0.2), "RobotoSlab-Medium.ttf", 25, False, RED, text_ada)
        textbox_ada.render(screen)

        x_off, y_off = periodic_movement(1, 5)

        aggressive_ada(504 + x_off, 156, 650, 550, active_health_ada)
        glada_gunnar(24, 144 + y_off, 122, 45, active_health_gunnar)
        quit_button()
        back_button()

        crossed_sword()

class WinnerScreenGunnar:
    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background_win, (0, 0))
        gunnar_bigger = pg.transform.scale(gunnar.image, (350, 350))
        screen.blit(gunnar_bigger, (220, 235))
        winning_crown_hasse()
        pink_dragon_sad = pg.image.load("Pink_dragon_05.png")
        pink_dragon_sad = pg.transform.scale(pink_dragon_sad, (204, 235))
        screen.blit(pink_dragon_sad, (25, 340))
        screen.blit(logo, (213, -55))
        tear_drop = pg.image.load("tear-png-20.png")
        tear_drop = pg.transform.scale(tear_drop, (25, 25))
        screen.blit(tear_drop, (120, 410))
        text_speech(screen, "RobotoSlab-Medium.ttf", 30, "Congratulations,", YELLOW_LIGHT, 389, 150, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 30, f"{gunnar.name} won!", YELLOW_LIGHT, 388, 200, True)
        quit_button()


class WinnerScreenAda:
    def __init__(self):
        self.music = music_lose_game_melody()

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background_win, (0, 0))
        ada_win_pic = pg.image.load("Pink_dragon_08.png")
        ada_win_pic = pg.transform.scale(ada_win_pic, (350, 350))
        screen.blit(ada_win_pic, (205, 285))
        winning_crown_ada()
        gunnar_lose = pg.transform.scale(gunnar.image, (200, 200))
        screen.blit(gunnar_lose, (25, 355))
        tear_drop = pg.image.load("tear-png-20.png")
        tear_drop = pg.transform.scale(tear_drop, (25, 25))
        screen.blit(tear_drop, (90, 430))
        screen.blit(logo, (215, -55))
        text_speech(screen, "RobotoSlab-Medium.ttf", 30, "Congratulations,", YELLOW_LIGHT, 386, 150, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 30, f"{ada.name} won!", YELLOW_LIGHT, 385, 200, True)
        quit_button()

click = False
button = 0

def mainloop(screen):
    global button
    global click
    state = MenuStartScreen()
    while True:
        # Event handling
        ev = pg.event.poll()
        if ev.type == pg.KEYDOWN:
            state = state.handle_keydown(ev.key)
            if ev.key == 1:
                click = True
            if ev.key == pg.K_RETURN:
                button += 1
        if ev.type == pg.MOUSEBUTTONDOWN:
            temp_state = state.handle_mouse_button(ev.button)
            if temp_state is not None:
                state = temp_state
        elif ev.type == pg.QUIT:
            break

        if common.next_screen is not None:
            print("changing frames to", type(common.next_screen))
            state = common.next_screen
            common.next_screen = None

        state = state.handle_timer()

        # Render
        state.render(screen)
        pg.display.update()


def glada_gunnar(x, y, a, b, active_health):
    if 1 <= button <= 10:
        screen.blit(gunnar.image, (x, y))
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{gunnar.name}", gunnar.color, a, b, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 15,
                    f"Stats: HP: {active_health}, Attack: {gunnar.attack}, Mood: {gunnar.mood}",
                    WHITE, 170, 20,
                    True)
    else:
        screen.blit(gunnar.image, (x, y))
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{gunnar.name}", gunnar.color, a, b, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 15,
                    f"Stats: HP: {gunnar.health}, Attack: {gunnar.attack}, Mood: {gunnar.mood}", WHITE, 170, 20,
                    True)


def aggressive_ada(x, y, a, b, active_health):
    if 2 <= button <= 10:
        screen.blit(ada.image, (x, y))
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{ada.name}", ada.color, a, b, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Stats: HP: {active_health} Attack: {ada.attack} Mood: {ada.mood}",
                    WHITE, 630, 575, True)
    else:
        screen.blit(ada.image, (x, y))
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{ada.name}", ada.color, a, b, True)
        text_speech(screen, "RobotoSlab-Medium.ttf", 15,
                    f"Stats: HP: {ada.health} Attack: {ada.attack} Mood: {ada.mood}",
                    WHITE, 630, 575, True)


def left_chat_bubble():
    left_bubble = pg.image.load("Chat_bubble_left.png")
    left_bubble = pg.transform.scale(left_bubble, (300, 170))
    screen.blit(left_bubble, (250, 50))
    mood_score = calc_mood_score(gunnar.mood, "Göteborg", live=False)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 390, 135, True)


def right_chat_bubble():
    right_bubble = pg.image.load("Chat_bubble_right.png")
    right_bubble = pg.transform.scale(right_bubble, (300, 170))
    screen.blit(right_bubble, (260, 350))
    mood_score = calc_mood_score(ada.mood, "Västerås", live=False)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 370, 435, True)


def pop_up_bubbles(button):
    if button == 1:
        left_chat_bubble()

    if button == 2:
        left_chat_bubble()
        right_chat_bubble()


def battle_time_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 240 and 245 <= mouse[1] <= 225 + 100:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (287, 247, 221, 66))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, width / 2.02,
                    height / 2.15, True)
    else:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (287, 247, 221, 66))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, width / 2.02,
                    height / 2.15, True)


def quit_button():
    mouse = pg.mouse.get_pos()
    if 650 <= mouse[0] <= 650 + 140 and 30 <= mouse[1] <= 30 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [652, 32, 137, 37])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "QUIT", BLACK, 715, 48, True)
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [650, 30, 140, 40])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "QUIT", BLACK, 715, 48, True)


def back_button():
    mouse = pg.mouse.get_pos()
    if 30 <= mouse[0] <= 30 + 140 and 540 <= mouse[1] <= 540 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)


def attack_button():
    mouse = pg.mouse.get_pos()
    if 87 <= mouse[0] <= 87 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_RED_SELECTED, [89, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [87, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 162, 453, True)
        sound_ambient_hover_over_attack_btn()
    else:
        pg.draw.rect(screen, LIGHT_RED_UNSELECTED, [89, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [87, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 162, 453, True)


def special_attack_button():
    mouse = pg.mouse.get_pos()
    if 325 <= mouse[0] <= 325 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_BLUE_SELECTED, [327, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [325, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Special", BLACK, 400, 453, True)
        sound_ambient_hover_over_special_attack_btn()
    else:
        pg.draw.rect(screen, LIGHT_BLUE_UNSELECTED, [327, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [325, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Special", BLACK, 400, 453, True)


def quiz_button():
    mouse = pg.mouse.get_pos()
    if 563 <= mouse[0] <= 563 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_GREEN_SELECTED, [565, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [563, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Quiz", BLACK, 638, 453, True)
        sound_ambient_hover_quizz_btn()
    else:
        pg.draw.rect(screen, LIGHT_GREEN_UNSELECTED, [565, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [563, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Quiz", BLACK, 638, 453, True)


def start_game_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 225 and 280 <= mouse[1] <= 280 + 65:
        pg.draw.rect(screen, BLACK, (275, 280, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 282, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Start Game", BLACK, width / 2.025,
                    height / 1.93, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 280, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 282, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Start Game", BLACK, width / 2.025,
                    height / 1.93, True)


def instructions_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 240 and 360 <= mouse[1] <= 360 + 65:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 362, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "How To Play", BLACK, width / 2.025,
                    height / 1.54, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 362, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "How To Play", BLACK, width / 2.025,
                    height / 1.54, True)


def quit_button_start():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 225 and 440 <= mouse[1] <= 440 + 65:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 442, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, width / 2.025,
                    height / 1.27, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 442, 236, 61))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, width / 2.025,
                    height / 1.27, True)


def sword(turn):
    sword = pg.image.load("sword_resized.png")
    screen.blit(sword, (315, 170))


def crossed_sword():
    double_sword = pg.image.load("Sword_crossed_01.PNG")
    double_sword = pg.transform.scale(double_sword, (230, 230))
    screen.blit(double_sword, (305, 160))

def winning_crown_hasse():
    winning_crown = pg.image.load("crown.png")
    winning_crown = pg.transform.scale(winning_crown, (170, 140))
    screen.blit(winning_crown, (270, 180))

def winning_crown_ada():
    winning_crown = pg.image.load("crown.png")
    winning_crown = pg.transform.scale(winning_crown, (151, 124))
    screen.blit(winning_crown, (340, 245))


def music_intro():
    pg.mixer.init()
    pg.mixer.music.load("intro_song_1.mp3")
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.1)


def music_battle():
    pg.mixer.init()
    pg.mixer.music.load("battle_time_1.mp3")
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.1)

def music_lose_game_melody():
    pg.mixer.init()
    pg.mixer.music.load("lose_game_melody.mp3")
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.2)

def sound_ambient_hover_over_attack_btn():
    sound = mixer.Sound("ambient_attack_c.mp3")
    sound.play()
    sound.set_volume(0.1)

def sound_ambient_hover_over_special_attack_btn():
    sound = mixer.Sound("ambient_special_attack_c1.mp3")
    sound.play()
    sound.set_volume(0.1)

def sound_ambient_hover_quizz_btn():
    sound = mixer.Sound("ambient_quizz_c2.mp3")
    sound.play()
    sound.set_volume(0.1)



if __name__ == '__main__':
    common.common_init()
    pg.display.set_caption("PokeMood")
    font = pg.font.Font(pg.font.match_font('arial'), 30)
    mainloop(screen)
    pg.quit()
