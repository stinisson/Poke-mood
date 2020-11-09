import pygame as pg
from random import randint
import sys

from constants import *
from poketer import Poketer
from twitter.mood_score import calc_mood_score
from quiz.quiz import QuizStartScreen
from quiz.quiz_api import quiz_categories
from common import TextBox, periodic_movement, music, Button
from sentiment_analysis_screen import SentimentAnalysisScreen


width = 800
height = 600
screen = pg.display.set_mode((width, height))

programIcon = pg.image.load('media/images/icon.png')
icon = pg.transform.smoothscale(programIcon, (32, 32))
pg.display.set_icon(icon)


bg = pg.image.load("media/images/Background_forest.jpg")
background = pg.transform.scale(bg, (800, 600))

vs_sign = pg.image.load("media/images/VS.PNG")
vs_sign = pg.transform.scale(vs_sign, (200, 150))

background_win = pg.image.load("media/images/winning_pic.jpg")
background_win = pg.transform.scale(background_win, (800, 600))

logo = pg.image.load("media/images/LOGO.PNG")
logo = pg.transform.scale(logo, (360, 222))

start_background = pg.image.load("media/images/background_start.png")
start_background = pg.transform.scale(start_background, (800, 600))

instructions_frame = pg.image.load("media/images/Frame_background.PNG")
instructions_frame = pg.transform.scale(instructions_frame, (650, 450))

start_screen = None


def text_speech(screen, font: str, size: int, text: str, color, x, y, bold: bool):
    font = pg.font.Font(font, size)
    font.set_bold(bold)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def attack_function(attacker, defender):
    defender.add_health(-attacker.attack)
    return attacker.attack


def special_attack(attacker, defender):
    misschans = randint(1, 6)
    if misschans <= 2:
        defender.add_health(-attacker.attack * 2)
        return attacker.attack * 2
    return 0


def cpu_random_attack():
    random_number = randint(1, 11)
    if random_number <= 7:
        return True
    if random_number >= 8:
        return False


class MenuStartScreen:
    def __init__(self):
        music("media/music/intro_song_1.mp3", 0.0)

    def handle_keydown(self, key):
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        start_game_button_rect = pg.Rect(275, 280, 240, 65)
        instructions_button_rect = pg.Rect(275, 360, 240, 65)
        quit_game_button_rect = pg.Rect(275, 440, 240, 65)
        if button == 1:
            if start_game_button_rect.collidepoint((mx, my)):
                return start_screen
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
        self.popup_state = "not clicked"
        self.gunnar_mood_score = 0
        self.ada_mood_score = 0

    def handle_keydown(self, key):
        if key == pg.K_RETURN:
            if self.popup_state == "not clicked":
                self.gunnar_mood_score = calc_mood_score(gunnar.mood, "Göteborg", live=False)
                gunnar.add_health(self.gunnar_mood_score)
                self.popup_state = "one click"
            elif self.popup_state == "one click":
                self.ada_mood_score = calc_mood_score(ada.mood, "Västerås", live=False)
                ada.add_health(self.ada_mood_score)
                self.popup_state = "two clicks"
        return self

    def handle_mouse_button(self, button):
        mx, my = pg.mouse.get_pos()
        battle_button_rect = pg.Rect(285, 245, 225, 70)
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        if button == 1:
            if battle_button_rect.collidepoint((mx, my)):
                music("media/music/battle_time_1.mp3", 0.0)
                return BattleScreen()
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        ada_name, ada_stats = aggressive_ada(520, 250, 0.75, 0.9, 0.76, 0.95)
        ada_name.render(screen)
        ada_stats.render(screen)
        gunnar_name, gunnar_stats = glada_gunnar(8, 70, 0.2, 0.05, 0.22, 0.1)
        gunnar_name.render(screen)
        gunnar_stats.render(screen)

        pop_up_bubbles(self.popup_state, self.gunnar_mood_score, self.ada_mood_score)

        battle_time_button()
        quit_button()
        text_speech(screen, "fonts/RobotoSlab-Medium.ttf", 15, "Press [enter] for moodscores", BLACK, 397, 330, True)


class BattleScreen:
    def __init__(self):
        self.attack_button = Button((0.14, 0.8), (0.2, 0.1), PURPLE_1, PURPLE_5, 22, WHITE, "Attack", frame=PURPLE_2)
        self.special_button = Button((0.38, 0.8), (0.2, 0.1), PURPLE_2, PURPLE_5, 22, WHITE, "Special", frame=PURPLE_3)
        self.sentiment_button = Button((0.62, 0.8), (0.2, 0.1), PURPLE_3, PURPLE_5, 22, WHITE, "Sentiment", frame=PURPLE_4)
        self.quiz_button = Button((0.86, 0.8), (0.2, 0.1), PURPLE_4, PURPLE_5, 22, WHITE, "Quiz", frame=PURPLE_1)
        self.quit_button = Button((0.7, 0.1), (0.2, 0.1), LIGHT_GREEN_UNSELECTED, LIGHT_GREEN_SELECTED, 22, WHITE, "QUIT")

    def handle_keydown(self, key):
        if key == pg.K_BACKSPACE:
            return start_screen
        return self

    def handle_mouse_button(self, button):
        if button == 1:
            if self.attack_button.handle_mouse_button(button):
                return AttackScreen("user")
            if self.special_button.handle_mouse_button(button):
                return SpecialAttackScreen("user")
            if self.sentiment_button.handle_mouse_button(button):
                return SentimentAnalysisScreen(gunnar, BattleScreen())
            if self.quiz_button.handle_mouse_button(button):
                return QuizStartScreen(5, quiz_categories, self, gunnar)
            if self.quit_button.handle_mouse_button(button):
                sys.exit()

        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        x_off, y_off = periodic_movement(1, 5)
        gunnar_name, gunnar_stats = glada_gunnar(24, 123 + y_off, 0.22, 0.05, 0.22, 0.1)
        ada_name, ada_stats = aggressive_ada(504, 135, 0.79, 0.05, 0.78, 0.1)
        ada_name.render(screen)
        ada_stats.render(screen)
        gunnar_name.render(screen)
        gunnar_stats.render(screen)

        self.attack_button.render(screen)
        self.special_button.render(screen)
        self.sentiment_button.render(screen)

        self.quiz_button.render(screen)

        screen.blit(vs_sign, (300, 200))
        textbox_gunnar = TextBox((0.5, 0.2), 30, False, WHITE, "It's your turn!")
        textbox_gunnar.render(screen)


class AttackScreen:
    def __init__(self, turn_):
        self.turn = turn_
        self.timeout = pg.time.get_ticks()

        if self.turn == "user":
            attack_score = attack_function(gunnar, ada)
            self.text_gunnar = f"Gunnar attacked Ada! Ada took {attack_score} in damage!"
            self.text_ada = ""
        else:
            attack_score = attack_function(ada, gunnar)
            self.text_ada = f"Ada attacked Gunnar! You took {attack_score} in damage!"
            self.text_gunnar = ""

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return start_screen
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
        if time_now - self.timeout > 3000 and self.timeout != 0:
            self.timeout = 0

            if ada.health <= 0:
                return WinnerScreenGunnar()
            if gunnar.health <= 0:
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
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        textbox_gunnar = TextBox((0.5, 0.2), 25, False, LIGHT_GREEN, self.text_gunnar)
        textbox_gunnar.render(screen)

        textbox_ada = TextBox((0.5, 0.2), 25, False, LIGHT_PINK, self.text_ada)
        textbox_ada.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        if self.turn == "user":
            gunnar_name, gunnar_stats = glada_gunnar(24, 144 + y_off, 0.2, 0.05, 0.22, 0.1)
            ada_name, ada_stats = aggressive_ada(504, 156, 0.75, 0.9, 0.76, 0.95)
        else:
            gunnar_name, gunnar_stats = glada_gunnar(24, 144, 0.2, 0.05, 0.22, 0.1)
            ada_name, ada_stats = aggressive_ada(504, 156 + y_off, 0.75, 0.9, 0.76, 0.95)

        ada_name.render(screen)
        ada_stats.render(screen)
        gunnar_name.render(screen)
        gunnar_stats.render(screen)

        quit_button()
        back_button()

        # Rotate sword depending on whose turn it is
        sword(self.turn)


class SpecialAttackScreen:
    def __init__(self, turn_):
        self.turn = turn_
        self.timeout = pg.time.get_ticks()

        if self.turn == "user":
            attack_score = special_attack(gunnar, ada)
            self.text_gunnar = f"Gunnar special attacked Ada! Ada took {attack_score} in damage!"
            self.text_ada = ""
        else:
            attack_score = special_attack(ada, gunnar)
            self.text_ada = f"Ada special attacked Gunnar! You took {attack_score} in damage!"
            self.text_gunnar = ""

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return start_screen
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
        if time_now - self.timeout > 3000 and self.timeout != 0:
            self.timeout = 0

            if ada.health <= 0:
                return WinnerScreenGunnar()
            if gunnar.health <= 0:
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
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        textbox_gunnar = TextBox((0.5, 0.2), 25, False, LIGHT_GREEN, self.text_gunnar)
        textbox_gunnar.render(screen)

        textbox_ada = TextBox((0.5, 0.2), 25, False, LIGHT_PINK, self.text_ada)
        textbox_ada.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        if self.turn == "user":
            gunnar_name, gunnar_stats = glada_gunnar(24, 144 + y_off, 0.2, 0.05, 0.22, 0.1)
            ada_name, ada_stats = aggressive_ada(504, 156, 0.75, 0.9, 0.76, 0.95)
        else:
            gunnar_name, gunnar_stats = glada_gunnar(24, 144, 0.2, 0.05, 0.22, 0.1)
            ada_name, ada_stats = aggressive_ada(504, 156 + y_off, 0.75, 0.9, 0.76, 0.95)

        ada_name.render(screen)
        ada_stats.render(screen)
        gunnar_name.render(screen)
        gunnar_stats.render(screen)

        quit_button()
        back_button()
        crossed_sword()


class WinnerScreenGunnar:
    def __init__(self):
        music("media/music/vinnar_låt_utkast.mp3", 0.0)

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return start_screen
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
        x_off, y_off = periodic_movement(1, 5)
        gunnar_bigger = pg.transform.scale(gunnar.image, (350, 350))
        screen.blit(gunnar_bigger, (220, 235 + y_off))
        winning_crown_hasse_moving()
        pink_dragon_sad = pg.image.load("media/images/Pink_dragon_05.png")
        pink_dragon_sad = pg.transform.scale(pink_dragon_sad, (204, 235))
        screen.blit(pink_dragon_sad, (25, 340))
        screen.blit(logo, (213, -55))
        tear_drop = pg.image.load("media/images/tear-png-20.png")
        tear_drop = pg.transform.scale(tear_drop, (25, 25))
        screen.blit(tear_drop, (120, 410))
        game_won = TextBox((0.5, 0.2), 35, False, YELLOW_LIGHT, f"Congratulations, {gunnar.name} won!")
        game_won.render(screen)
        quit_button()


class WinnerScreenAda:
    def __init__(self):
        music("media/music/lose_game_melody.mp3", 0.0)

    def handle_keydown(self, key):
        if key == pg.K_ESCAPE:
            return start_screen
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
        ada_win_pic = pg.image.load("media/images/Pink_dragon_08.png")
        ada_win_pic = pg.transform.scale(ada_win_pic, (350, 350))
        screen.blit(ada_win_pic, (205, 285))
        winning_crown_ada_moving()
        gunnar_lose = pg.transform.scale(gunnar.image, (200, 200))
        screen.blit(gunnar_lose, (25, 355))
        tear_drop = pg.image.load("media/images/tear-png-20.png")
        tear_drop = pg.transform.scale(tear_drop, (25, 25))
        screen.blit(tear_drop, (90, 430))
        screen.blit(logo, (215, -55))
        game_lost = TextBox((0.5, 0.2), 35, False, PINK, "Better luck next time!")
        game_lost.render(screen)
        quit_button()


def mainloop(screen):
    # To be able to go back to startscreen and run popups if not run before
    global start_screen
    start_screen = StartScreen()

    state = MenuStartScreen()

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


def glada_gunnar(x, y, name_relx, name_rely, stats_relx, stats_rely):
        screen.blit(gunnar.image, (x, y))
        name = TextBox((name_relx, name_rely), 18, False, LIGHT_GREEN, f"{gunnar.name}")
        stats = TextBox((stats_relx, stats_rely), 18, False, WHITE,
                        f"Mood: {gunnar.mood.capitalize()} Attack: {gunnar.attack} Health: {gunnar.health}")
        return name, stats


def aggressive_ada(x, y, name_relx, name_rely, stats_relx, stats_rely):
    screen.blit(ada.image, (x, y))
    name = TextBox((name_relx, name_rely), 18, False, LIGHT_PINK, f"{ada.name}")
    stats = TextBox((stats_relx, stats_rely), 18, False, WHITE,
                    f"Mood: {ada.mood.capitalize()} Attack: {ada.attack} Health: {ada.health}")
    return name, stats


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
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, width / 2.02,
                    height / 2.15, True)
    else:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (287, 247, 221, 66))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, width / 2.02,
                    height / 2.15, True)


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
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Start Game", BLACK, width / 2.025,
                    height / 1.93, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 280, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 282, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Start Game", BLACK, width / 2.025,
                    height / 1.93, True)


def instructions_button():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 240 and 360 <= mouse[1] <= 360 + 65:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 362, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "How To Play", BLACK, width / 2.025,
                    height / 1.54, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 360, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 362, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "How To Play", BLACK, width / 2.025,
                    height / 1.54, True)


def quit_button_start():
    mouse = pg.mouse.get_pos()
    if 275 <= mouse[0] <= 275 + 225 and 440 <= mouse[1] <= 440 + 65:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (277, 442, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, width / 2.025,
                    height / 1.27, True)
    else:
        pg.draw.rect(screen, BLACK, (275, 440, 240, 65), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (277, 442, 236, 61))
        text_speech(screen, "fonts/RobotoSlab-Black.ttf", 30, "Quit Game", BLACK, width / 2.025,
                    height / 1.27, True)


def sword(turn):
    sword = pg.image.load("media/images/sword_resized.png")
    x_off, y_off = periodic_movement(1, 5)
    if turn == "user":
        rotate_image = pg.transform.rotozoom(sword, 0 + x_off, 1)
    else:
        rotate_image = pg.transform.rotozoom(sword, 70 + x_off, 1)
    new_rect = rotate_image.get_rect(center=(400, 300))
    screen.blit(rotate_image, new_rect)


def crossed_sword():
    double_sword = pg.image.load("media/images/Sword_crossed_01.PNG")
    double_sword = pg.transform.smoothscale(double_sword, (230, 230))
    rect = double_sword.get_rect()
    x_off, y_off = periodic_movement(1, 7)
    shield = pg.transform.smoothscale(double_sword, (rect.width + int(x_off), rect.height + int(x_off)))
    blit_rect = shield.get_rect()
    blit_rect.center = (420, 280)
    screen.blit(shield, blit_rect)


def winning_crown_hasse_moving():
    winning_crown = pg.image.load("media/images/crown.png")
    winning_crown = pg.transform.scale(winning_crown, (170, 140))
    x_off, y_off = periodic_movement(1, 5)
    screen.blit(winning_crown, (270, 180 + y_off))


def winning_crown_ada_moving():
    winning_crown = pg.image.load("media/images/crown.png")
    winning_crown = pg.transform.scale(winning_crown, (151, 124))
    x_off, y_off = periodic_movement(1, 5)
    screen.blit(winning_crown, (340, 245 + y_off))


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("PokeMood")
    gunnar = Poketer("Happy Hasse", 'happy', 'yellow', 50, 45, catchword="#YOLO",
                     img_name="media/images/Green_monster_resized.png")
    ada = Poketer("Aggressive Ada", 'angry', 'red', 50, 45, catchword="#FTW",
                  img_name="media/images/Pink_dragon_01.png")
    mainloop(screen)
    pg.quit()
