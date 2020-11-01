from random import randint

import pygame as pg
import sys
from Pygame.constants import *
from mood_score import calc_mood_score
from pygame import mixer

pg.init()


def music_intro(intro_song):
    pg.mixer.init()
    pg.mixer.music.load(intro_song)
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.5)

def music_battle(battle_song):
    pg.mixer.init()
    pg.mixer.music.load(battle_song)
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.5)

def sound_attack_dino(dinsosaur_growl):
    dino_sound = mixer.Sound(dinsosaur_growl)
    dino_sound.play()
    dino_sound.set_volume(0.2)

def sound_click_block_button(cymbal):
    block_sound = mixer.Sound(cymbal)
    block_sound.play()
    block_sound.set_volume(0.2)

def sound_enter_battle(enter_battle):
    enter_battle = mixer.Sound(enter_battle)
    enter_battle.play()
    enter_battle.set_volume(0.1)

def sound_booing_crowd(quit_button):
    enter_battle = mixer.Sound(quit_button)
    enter_battle.play()
    enter_battle.set_volume(0.1)

display_width = 800
display_height = 600

screen = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Demo - PokeMood')

clock = pg.time.Clock()
crashed = False

base_font = pg.font.SysFont("roboto mono", 30, True)

bg = pg.image.load("Background_forest.jpg").convert()
background = pg.transform.scale(bg, (800, 600))
screen.blit(background, (0, 0))

# logo = pg.image.load("LOGO2.PNG")
# logo = pg.transform.scale(logo, (300, 185))

shield = pg.image.load("shield_white.png")
sword = pg.image.load("sword_resized.png")



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
        result = self.health + health_score
        return result

    def add_max_health(self, max_health_score):
        result = self.max_health + max_health_score
        return result

    def get_health(self):
        return self.health

    def attack_fnc(self, opponent_pokemon):
        miss_chance = randint(1, 6)
        crit_chance = randint(1, 6)
        dmg_modifier = randint(-3, 3)
        if miss_chance <= 5:
            if crit_chance >= 5:
                opponent_pokemon.health = opponent_pokemon.health - (self.attack + dmg_modifier) * 2
                # atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Kritisk träff!", BLACK, 300, 150, True)
                # self.healtcheck_color(opponent_pokemon)
                # self.healthcheck(opponent_pokemon, opponent.name)
                return opponent_pokemon.health
            else:
                opponent_pokemon.health = opponent_pokemon.health - (self.attack + dmg_modifier)
                # atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Attacken träffade!", BLACK, 300, 150, True)
                # self.healtcheck_color(opponent_pokemon)
                # self.healthcheck(opponent_pokemon, opponent.name)
                return opponent_pokemon.health
        else:
            text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Attacken missade!", BLACK, 300, 150, True)


gunnar = Poketer("Glada Gunnar", 'happy', 'yellow', 50, 50, 45, catchword="#YOLO", img_name="Green_monster_resized.png")
ada = Poketer("Aggressiva Ada", 'angry', 'red', 50, 50, 45, catchword="#FTW", img_name="Pink_dragon_01.png")


# louise = Poketer("Ledsna Louise", 'sad', 'blue', 50, 50, 45, catchword="#TGIF")
# kalle = Poketer("Kärleksfulla Kalle", 'loving', 'magenta', 50, 50, 45, catchword="#XOXO")


def text_input(input_rect, user_text):
    pg.draw.rect(screen, BLACK, input_rect, 2)
    pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [72.6, 537.5, 197, 37])
    text_surface = base_font.render(user_text, True, BLACK)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))


def vs_logo():
    vs_sign = pg.image.load("VS.PNG")
    vs_sign = pg.transform.scale(vs_sign, (200, 150))
    screen.blit(vs_sign, (300, 225))


def text_speech(screen, font: str, size: int, text: str, color, x, y, bold: bool):
    font = pg.font.Font(font, size)
    font.set_bold(bold)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def Aggressive_Ada(x, y, a, b):
    mood_score = calc_mood_score(ada.mood, "Stockholm", live=False)
    result1 = ada.add_max_health(mood_score)
    result2 = ada.add_health(mood_score)
    screen.blit(ada.image, (x, y))
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{ada.name}", ada.color, a, b, True)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Stats: HP: {result1}, Attack: {ada.attack}, Mood: {ada.mood}",
                WHITE, 630, 575,
                True)


def Glada_Gunnar(x, y, a, b):
    mood_score = calc_mood_score(gunnar.mood, "Göteborg", live=False)
    result1 = gunnar.add_max_health(mood_score)
    result2 = gunnar.add_health(mood_score)
    screen.blit(gunnar.image, (x, y))
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"{gunnar.name}", gunnar.color, a, b, True)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15,
                f"Stats: HP: {result1}, Attack: {gunnar.attack}, Mood: {gunnar.mood}", WHITE, 170, 20,
                True)


def quit_button(mouse):
    text = base_font.render('QUIT', True, BLACK)
    if 650 <= mouse[0] <= 650 + 140 and 30 <= mouse[1] <= 30 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [652, 32, 137, 37])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
        sound_booing_crowd("electric_surge.mp3")
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [650, 30, 140, 40])
        pg.draw.rect(screen, BLACK, [650, 30, 140, 40], 3)
    screen.blit(text, (690, 40))


def battle_time_button(mouse):
    if 275 <= mouse[0] <= 275 + 240 and 245 <= mouse[1] <= 225 + 100:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, (287, 247, 221, 66))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, display_width / 2.02,
                    display_height / 2.15, True)
        sound_enter_battle("boomer_fx.mp3")
    else:
        pg.draw.rect(screen, BLACK, (285, 245, 225, 70), 3)
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, (287, 247, 221, 66))
        text_speech(screen, "RobotoSlab-Black.ttf", 30, "Battle time!", BLACK, display_width / 2.02,
                    display_height / 2.15, True)


def back_button(mouse):
    if 30 <= mouse[0] <= 30 + 140 and 540 <= mouse[1] <= 540 + 40:
        pg.draw.rect(screen, COLOR_LIGHT_SELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)
    else:
        pg.draw.rect(screen, COLOR_LIGHT_UNSELECTED, [32, 542, 137, 37])
        pg.draw.rect(screen, BLACK, [30, 540, 140, 40], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "BACK", BLACK, 97, 558, True)


def attack_button(mouse):
    if 200 <= mouse[0] <= 200 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_RED_SELECTED, [202, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [200, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 272, 453, True)
    else:
        pg.draw.rect(screen, LIGHT_RED_UNSELECTED, [202, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [200, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Attack", BLACK, 272, 453, True)


def block_button(mouse):
    if 445 <= mouse[0] <= 445 + 150 and 430 <= mouse[1] <= 430 + 50:
        pg.draw.rect(screen, LIGHT_BLUE_SELECTED, [447, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Block", BLACK, 517, 453, True)
    else:

        pg.draw.rect(screen, LIGHT_BLUE_UNSELECTED, [447, 432, 147, 47])
        pg.draw.rect(screen, BLACK, [445, 430, 150, 50], 3)
        text_speech(screen, "RobotoSlab-Black.ttf", 25, "Block", BLACK, 517, 453, True)


def chat_bubble_left():
    left = pg.image.load('Chat_bubble_left.png').convert_alpha()
    left_small = pg.transform.scale(left, (300, 170))
    screen.blit(left_small, (250, 50))
    mood_score = calc_mood_score(gunnar.mood, "Göteborg", live=False)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 390, 135, True)


def chat_bubble_right():
    right = pg.image.load('Chat_bubble_right.png').convert_alpha()
    right_small = pg.transform.scale(right, (300, 170))
    screen.blit(right_small, (260, 350))
    mood_score = calc_mood_score(ada.mood, "Stockholm", live=False)
    text_speech(screen, "RobotoSlab-Medium.ttf", 15, f"Moodscore: {mood_score}", BLACK, 370, 435, True)


button = 0
click = False


def battle_menu():
    global button
    # active = False
    # user_text = ''
    music_intro("intro_song_1.mp3")
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        Aggressive_Ada(520, 300, 640, 300)
        Glada_Gunnar(8, 30, 122, 45)

        mx, my = pg.mouse.get_pos()
        mouse = pg.mouse.get_pos()

        battle_button_rect = pg.Rect(285, 245, 225, 70)
        battle_time_button(mouse)

        quit_button_rect = pg.Rect(650, 30, 140, 40)
        quit_button(mouse)

        # input_rect = pg.Rect(70, 535, 200, 40)
        # text_input(input_rect, user_text,)

        text_speech(screen, "RobotoSlab-Medium.ttf", 15, "Press [enter] for moodscores", BLACK, 397, 330, True)

        if battle_button_rect.collidepoint((mx, my)):
            if click:
                pg.mixer.music.stop()
                battle_time()

        if quit_button_rect.collidepoint((mx, my)):
            if click:
                pg.quit()
                sys.exit()

        if button == 1:
            chat_bubble_left()

        if button == 2:
            chat_bubble_left()
            chat_bubble_right()

        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_RETURN:
                    button += 1

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            # if event.type == pg.MOUSEBUTTONDOWN:
            #     if input_rect.collidepoint(event.pos):
            #         active = True
            #     else:
            #         active = False

            # if event.type == pg.KEYDOWN:
            #     keys = pg.key.get_pressed()
            #     if active:
            #         if keys[pg.K_BACKSPACE]:
            #             user_text = user_text[:-1]
            #         else:
            #             user_text += event.unicode

        pg.display.update()
        clock.tick(60)


def battle_time():
    music_battle("battle_time_1.mp3")
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        Aggressive_Ada(display_width * 0.63, display_height * 0.26, 650, 550)
        Glada_Gunnar(display_width * 0.03, display_height * 0.24, 122, 45)
        mouse = pg.mouse.get_pos()
        vs_logo()
        quit_button_rect = pg.Rect(650, 30, 140, 40)
        quit_button(mouse)

        back_button_rect = pg.Rect(30, 540, 140, 40)
        back_button(mouse)

        attack_button_rect = pg.Rect(200, 430, 150, 50)
        attack_button(mouse)

        block_button_rect = pg.Rect(445, 430, 150, 50)
        block_button(mouse)

        mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint((mx, my)):
                    battle_menu()
                if quit_button_rect.collidepoint((mx, my)):
                    pg.quit()
                if block_button_rect.collidepoint((mx, my)):
                    block_func()
                if attack_button_rect.collidepoint((mx, my)):
                    attack_func()

        pg.display.update()
        clock.tick(60)


def block_func():
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        Aggressive_Ada(display_width * 0.63, display_height * 0.26, 650, 550)
        Glada_Gunnar(display_width * 0.03, display_height * 0.24, 122, 45)
        screen.blit(shield, (305, 160))
        mouse = pg.mouse.get_pos()

        quit_button_rect = pg.Rect(650, 30, 140, 40)
        quit_button(mouse)

        back_button_rect = pg.Rect(30, 540, 140, 40)
        back_button(mouse)

        attack_button_rect = pg.Rect(200, 430, 150, 50)
        attack_button(mouse)

        block_button_rect = pg.Rect(445, 430, 150, 50)
        block_button(mouse)

        mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint((mx, my)):
                    battle_menu()
                if quit_button_rect.collidepoint((mx, my)):
                    pg.quit()
                if attack_button_rect.collidepoint((mx, my)):
                    attack_func()

        pg.display.update()
        clock.tick(60)


def attack_func():
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        Aggressive_Ada(display_width * 0.63, display_height * 0.26, 650, 550)
        Glada_Gunnar(display_width * 0.03, display_height * 0.24, 122, 45)
        screen.blit(sword, (315, 170))
        mouse = pg.mouse.get_pos()

        quit_button_rect = pg.Rect(650, 30, 140, 40)
        quit_button(mouse)

        back_button_rect = pg.Rect(30, 540, 140, 40)
        back_button(mouse)

        attack_button_rect = pg.Rect(200, 430, 150, 50)
        attack_button(mouse)

        block_button_rect = pg.Rect(445, 430, 150, 50)
        block_button(mouse)
        atk = True
        display_text = False
        click = False
        mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if back_button_rect.collidepoint((mx, my)):
                    battle_menu()

                if quit_button_rect.collidepoint((mx, my)):
                    pg.quit()
                if block_button_rect.collidepoint((mx, my)):
                    sound_click_block_button("cartoon_cymbal_hit.mp3")
                    block_func()

                if attack_button_rect.collidepoint((mx, my)):
                    sound_attack_dino("dinosaur_growl.mp3")
                    temp = gunnar.attack_fnc(ada)
                    print(temp)


                    # while atk:
                    #     if click:
                    #         display_text = True
                    #         if display_text:
                    #             gunnar.attack_fnc(ada)
                    #             if click:
                    #                 atk = False
        pg.display.update()
        clock.tick(60)
if __name__ == '__main__':

    battle_menu()
