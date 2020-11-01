import pygame as pg
from random import randint
import sys
import math
from Pygame.constants import *
from mood_score import calc_mood_score
from quiz import QuizStartScreen
from quiz_api import quiz_categories

import common
common.common_init()

pg.init()
width = 800
height = 600
screen = pg.display.set_mode((width, height))

bg = pg.image.load("Background_forest.jpg")
background = pg.transform.scale(bg, (800, 600))

vs_sign = pg.image.load("VS.PNG")
vs_sign = pg.transform.scale(vs_sign, (200, 150))


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


class StartScreen:
    def __init__(self):
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

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        aggressive_ada(520, 300, 640, 300, active_health_ada)
        glada_gunnar(8, 30, 122, 45, active_health_gunnar)
        pop_up_bubbles(button)
        battle_time_button()
        quit_button()
        text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Press [enter] for moodscores", BLACK, 397, 330, True)


class BattleScreen:
    def __init__(self):
        print(self)

    def handle_keydown(self, key):
        if key == pg.K_BACKSPACE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        global shield_blit
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        back_button_rect = pg.Rect(30, 540, 140, 40)
        # attack_button_rect = pg.Rect(200, 430, 150, 50)
        # block_button_rect = pg.Rect(445, 430, 150, 50)
        # Kristin
        attack_button_rect = pg.Rect(87, 430, 150, 50)
        block_button_rect = pg.Rect(325, 430, 150, 50)
        quiz_button = pg.Rect(563, 430, 150, 50)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            if back_button_rect.collidepoint((mx, my)):
                return StartScreen()
            if attack_button_rect.collidepoint((mx,my)):
                attack_function(gunnar)
                return AttackScreen()
            if block_button_rect.collidepoint((mx, my)):
                special_attack(gunnar)
                return SpecialAttackScreen()
            if quiz_button.collidepoint((mx, my)):
                print("In BattleScreen")
                common.next_screen = QuizStartScreen(5, quiz_categories, self, gunnar)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        time = pg.time.get_ticks()
        x_off = 5 * math.cos(time * 3.14 / 1000)
        y_off = 5 * math.sin(time * 3.14 / 1000)

        aggressive_ada(504 + x_off, 156, 650, 550, active_health_ada)
        glada_gunnar(24, 144 + y_off, 122, 45, active_health_gunnar)
        screen.blit(vs_sign, (300, 225))
        quit_button()
        back_button()
        attack_button()
        special_attack_button()
        quiz_button()


class AttackScreen:
    def __init__(self):
        print(self)

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
        #special_attack_button = pg.Rect(445, 430, 150, 50)
        #attack_button_rect = pg.Rect(200, 430, 150, 50)
        # Kristin
        attack_button_rect = pg.Rect(87, 430, 150, 50)
        special_attack_button = pg.Rect(325, 430, 150, 50)
        quiz_button = pg.Rect(563, 430, 150, 50)
        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            if special_attack_button.collidepoint((mx, my)):
                special_attack(gunnar)
                if active_health_ada <= 0:
                    return StartScreen()
                if active_health_gunnar <= 0:
                    return StartScreen()
                return SpecialAttackScreen()
            if attack_button_rect.collidepoint((mx, my)):
                attack_function(gunnar)
                if active_health_ada <= 0:
                    return StartScreen()
                if active_health_gunnar <= 0:
                    return StartScreen()
            # Kristin
            if quiz_button.collidepoint((mx, my)):
                print("In AttackScreen")
                common.next_screen = QuizStartScreen(5, quiz_categories, self, gunnar)
            return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        time = pg.time.get_ticks()
        x_off = 5 * math.cos(time * 3.14 / 1000)
        y_off = 5 * math.sin(time * 3.14 / 1000)

        aggressive_ada(504, 156 + y_off, 650, 550, active_health_ada)
        glada_gunnar(24 + x_off, 144, 122, 45, active_health_gunnar)
        quit_button()
        back_button()
        attack_button()
        special_attack_button()
        quiz_button()
        sword()


click = False
button = 0


class SpecialAttackScreen:
    def __init__(self):
        print(self)

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return StartScreen()
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        back_button_rect = pg.Rect(30, 540, 140, 40)
        # attack_button_rect = pg.Rect(200, 430, 150, 50)
        # special_attack_button = pg.Rect(445, 430, 150, 50)
        # Kristin
        attack_button_rect = pg.Rect(87, 430, 150, 50)
        special_attack_button = pg.Rect(325, 430, 150, 50)
        quiz_button = pg.Rect(563, 430, 150, 50)
        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            if attack_button_rect.collidepoint((mx, my)):
                if active_health_ada <= 0:
                    return StartScreen()
                if active_health_gunnar <= 0:
                    return StartScreen()
                return AttackScreen()
            if special_attack_button.collidepoint((mx, my)):
                special_attack(gunnar)
                if active_health_ada <= 0:
                    return StartScreen()
                if active_health_gunnar <= 0:
                    return StartScreen()
            if quiz_button.collidepoint((mx, my)):
                print("In specialAttackScreen")
                common.next_screen = QuizStartScreen(5, quiz_categories, self, gunnar)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        time = pg.time.get_ticks()
        x_off = 5 * math.cos(time * 3.14 / 1000)
        y_off = 5 * math.sin(time * 3.14 / 1000)

        aggressive_ada(504 + x_off, 156, 650, 550, active_health_ada)
        glada_gunnar(24, 144 + y_off, 122, 45, active_health_gunnar)
        quit_button()
        back_button()
        attack_button()
        special_attack_button()
        quiz_button()
        shield()



def mainloop(screen):
    global button
    global click
    state = StartScreen()
    music_intro("intro_song_1.mp3")
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


# def attack_button():
#     mouse = pg.mouse.get_pos()
#     if 200 <= mouse[0] <= 200 + 150 and 430 <= mouse[1] <= 430 + 50:
#         pg.draw.rect(screen, LIGHT_RED_SELECTED, [202, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [200, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 272, 453, True)
#     else:
#         pg.draw.rect(screen, LIGHT_RED_UNSELECTED, [202, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [200, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 272, 453, True)
#
#
# def special_attack_button():
#     mouse = pg.mouse.get_pos()
#     if 445 <= mouse[0] <= 445 + 150 and 430 <= mouse[1] <= 430 + 50:
#         pg.draw.rect(screen, LIGHT_BLUE_SELECTED, [447, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Special", BLACK, 517, 453, True)
#     else:
#         pg.draw.rect(screen, LIGHT_BLUE_UNSELECTED, [447, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Special", BLACK, 517, 453, True)
#
#
# def quiz_button():
#     mouse = pg.mouse.get_pos()
#     if 445 <= mouse[0] <= 445 + 150 and 430 <= mouse[1] <= 430 + 50:
#         pg.draw.rect(screen, LIGHT_GREEN_SELECTED, [447, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Quiz", BLACK, 517, 453, True)
#     else:
#         pg.draw.rect(screen, LIGHT_GREEN_UNSELECTED, [447, 432, 147, 47])
#         pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
#         text_speech(screen, "RobotoSlab-Black.ttf", 25, "Quiz", BLACK, 517, 453, True)

def attack_button():
    mouse = pg.mouse.get_pos()
    if 87 <= mouse[0] <= 87 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_RED_SELECTED, [89, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [87, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 162, 453, True)
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
    else:
        pg.draw.rect(screen, LIGHT_GREEN_UNSELECTED, [565, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [563, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Quiz", BLACK, 638, 453, True)


def shield():
    shield = pg.image.load("shield_white.png")
    screen.blit(shield, (305, 160))


def sword():
    sword = pg.image.load("sword_resized.png")
    screen.blit(sword, (315, 170))

def music_intro(intro_song):
    pg.mixer.init()
    pg.mixer.music.load(intro_song)
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.1)


if __name__ == '__main__':
    pg.display.set_caption("PokeMood")
    font = pg.font.Font(pg.font.match_font('arial'), 30)
    mainloop(screen)
    pg.quit()