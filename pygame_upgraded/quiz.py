import math
import textwrap

from pygame_upgraded.quiz_api import get_quiz, quiz_categories
import pygame
from pygame import mixer

from Pygame.constants import BLACK, WHITE

# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
import common

QUIZ_TRANSP_GREEN_LIGHT = (14, 213, 41, 210)
QUIZ_TRANSP_GREEN_HIGHL = (14, 213, 41, 150)
QUIZ_TRANSP_GREEN = (5, 85, 15, 150)
QUIZ_TRANSP_RED = (215, 2, 30, 210)
QUIZ_DARKGREEN = (10, 150, 25)

FONT_ROBOTO = "fonts/RobotoSlab-Medium.ttf"
screen_size = (800, 600)

return_screen = None
poketer = None


def rel_to_pix(rel_pos):
    x = rel_pos[0] * screen_size[0]
    y = rel_pos[1] * screen_size[1]
    pix_pos = (x, y)
    return pix_pos


def pix_to_rel(pix_pos):
    rel_x = pix_pos[0] / screen_size[0]
    rel_y = pix_pos[1] / screen_size[1]
    rel_pos = (rel_x, rel_y)
    return rel_pos

def music(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

def sound(filename):
    sound = mixer.Sound(filename)
    sound.play()
    sound.set_volume(0.2)


class TextBox:
    def __init__(self, rel_pos, font_name, font_size, font_bold, color, text, line_width=100):
        self.position = (screen_size[0] * rel_pos[0], screen_size[1] * rel_pos[1])
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)
        self.font.set_bold(font_bold)
        self.color = color
        self.text_lines = []
        self.text_lines_shadow = []
        self.line_width = line_width
        self.set_text(text)

    def set_text(self, text):
        lines_specified_width = textwrap.fill(text, self.line_width)
        chopped_lines = lines_specified_width.split('\n')
        self.text_lines = []
        self.text_lines_shadow = []
        for line in chopped_lines:
            line_surface = self.font.render(line, True, self.color)
            self.text_lines.append(line_surface)
            line_surface_shadow = self.font.render(line, True, BLACK)
            self.text_lines_shadow.append(line_surface_shadow)

    def render(self, screen):
        # time = pygame.time.get_ticks()
        # x_off = 2 * math.cos(time*3.14/1000)
        # y_off = 2 * math.sin(time*3.14/1000)

        # shadow
        for idx, text_surface_shadow in enumerate(self.text_lines_shadow):
            text_rect_shadow = text_surface_shadow.get_rect()
            text_rect_shadow.center = self.position[0] + 1, self.position[1] + 2 + idx * (self.font_size + 15)
            screen.blit(text_surface_shadow, text_rect_shadow)

        for idx, text_surface in enumerate(self.text_lines):
            text_rect = text_surface.get_rect()
            text_rect.center = self.position[0], self.position[1] + idx * (self.font_size + 15)
            screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, rel_pos, rel_size, color, highlight, font_size, font_color, text):
        self.position = (screen_size[0] * rel_pos[0], screen_size[1] * rel_pos[1])
        self.size = (screen_size[0] * rel_size[0], screen_size[1] * rel_size[1])
        self.color = color
        self.highlight = highlight
        self.text = TextBox(rel_pos=rel_pos, font_name=FONT_ROBOTO,
                            font_size=font_size, font_bold=False, color=font_color, text=text, line_width=28)
        self.button_rect = pygame.Rect(self.position[0], self.position[1], self.size[0] - 3, self.size[1] - 3)
        self.button_rect.center = self.position[0], self.position[1]
        self.button_frame_rect = pygame.Rect(0, 0, self.size[0], self.size[1])  # x, y, width, height
        self.button_frame_rect.center = self.position[0], self.position[1]
        self.enabled = True

    def handle_keydown(self, key):
        pass

    def handle_mouse_button(self, mouse_button):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and mouse_button == 1 and self.enabled:
            return True
        else:
            return False

    def render(self, screen):
        pygame.draw.rect(screen, QUIZ_DARKGREEN, self.button_frame_rect, 4)  # button frame

        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and self.enabled:  # If mouse on button - highlight button
            if len(self.highlight) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.highlight)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.highlight, self.button_rect)
        else:
            if len(self.color) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.color)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.color, self.button_rect)

        self.text.render(screen)


class QuizStartScreen:
    def __init__(self, number_of_quiz_questions, quiz_categories, return_screen_, poketer_):
        global poketer
        #self.music = music_battle() #cl
        poketer = poketer_

        global return_screen
        return_screen = return_screen_
        music("quizz_music.mp3")
        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)
        self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                             font_size=30, font_bold=False, color=WHITE, text="It's quiz time!")

        quiz_start_text = f"""You will now get to try your luck with {number_of_quiz_questions} tricky questions. If you get at least
{number_of_quiz_questions - 1} correct answers you win a health bonus. Which category do you choose?"""

        self.info_text = TextBox(rel_pos=(0.5, 0.25), font_name=FONT_ROBOTO,
                                 font_size=25, font_bold=False, color=WHITE, text=quiz_start_text, line_width=55)
        self.category_buttons = []
        self.button_positions = [(0.3, 0.6),
                                 (0.7, 0.6),
                                 (0.3, 0.8),
                                 (0.7, 0.8)]

        self.categories = list(quiz_categories.keys())
        for idx, category in enumerate(self.categories):
            quiz_button = Button(rel_pos=self.button_positions[idx], rel_size=(0.4, 0.2),
                                 color=QUIZ_TRANSP_GREEN, highlight=QUIZ_TRANSP_GREEN_HIGHL,
                                 font_size=22, font_color=WHITE, text=category)
            self.category_buttons.append(quiz_button)

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            return QuizScreen()
        return self

    def handle_mouse_button(self, mouse_button):
        clicked_button_idx = None

        for category_button in self.category_buttons:
            if category_button.handle_mouse_button(mouse_button):
                clicked_button_idx = self.category_buttons.index(category_button)
                print(clicked_button_idx, "the_clicked_button")
                sound("music/cartoon_cymbal_hit.mp3")
                break

        if clicked_button_idx is not None:
            for category_button in self.category_buttons:
                category_button.enabled = False
            common.next_screen = QuizScreen(self.categories[clicked_button_idx])

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))
        self.title.render(screen)
        self.info_text.render(screen)

        for category_button in self.category_buttons:
            category_button.render(screen)


class QuizScreen:

    def __init__(self, quiz_category):
        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)
        self.title = None
        self.question_text = None
        self.quiz_answer_buttons = []
        self.current_question = 0

        self.number_of_quiz_questions = 5

        category, questions, correct_answers, answer_options = get_quiz(self.number_of_quiz_questions, quiz_category)
        self.category = category
        self.questions = questions
        self.correct_answers = correct_answers
        self.answer_options = answer_options
        self.correct_answer_idx = None
        self.num_of_correct_ans = 0
        self.button_positions = [(0.3, 0.6),
                                 (0.7, 0.6),
                                 (0.3, 0.8),
                                 (0.7, 0.8)]
        self.set_question()
        self.next_question_timeout = 0

    def set_question(self):

        self.next_question_timeout = 0
        self.current_question += 1

        if self.current_question == self.number_of_quiz_questions + 1:
            common.next_screen = QuizFinishedScreen(self.num_of_correct_ans, self.number_of_quiz_questions)
            return

        self.correct_answer_idx = self.answer_options[self.current_question - 1].index(
            self.correct_answers[self.current_question - 1])

        self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                             font_size=25, font_bold=False, color=WHITE,
                             text=f"{self.category} - Question {self.current_question}")

        self.question_text = TextBox(rel_pos=(0.5, 0.25), font_name=FONT_ROBOTO,
                                     font_size=25, font_bold=False, color=WHITE,
                                     text=self.questions[self.current_question - 1], line_width=55)
        self.quiz_answer_buttons = []
        for idx, answer_option in enumerate(self.answer_options[self.current_question - 1]):
            quiz_button = Button(rel_pos=self.button_positions[idx], rel_size=(0.4, 0.2),
                                 color=QUIZ_TRANSP_GREEN, highlight=QUIZ_TRANSP_GREEN_HIGHL,
                                 font_size=22, font_color=WHITE, text=answer_option)
            self.quiz_answer_buttons.append(quiz_button)

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            pass
            #self.set_question()
        return self

    def handle_timer(self):
        return self

    def handle_mouse_button(self, mouse_button):
        clicked_button_idx = None
        quiz_button = None
        for quiz_button in self.quiz_answer_buttons:
            if quiz_button.handle_mouse_button(mouse_button):
                clicked_button_idx = self.quiz_answer_buttons.index(quiz_button)
                print(clicked_button_idx, "the_clicked_button")
                break

        if clicked_button_idx is not None:

            self.next_question_timeout = pygame.time.get_ticks()

            print("correct_answer_idx", self.correct_answer_idx)
            if clicked_button_idx == self.correct_answer_idx:
                print("Rätt svar!")
                quiz_button.color = QUIZ_TRANSP_GREEN_LIGHT
                self.num_of_correct_ans += 1
                sound("music/kids_cheering.mp3")
            else:
                quiz_button.color = QUIZ_TRANSP_RED
                self.quiz_answer_buttons[self.correct_answer_idx].color = QUIZ_TRANSP_GREEN_LIGHT
                print("Det var fel, rätt svar var knapp", self.correct_answer_idx)
                sound("music/dinosaur_growl.mp3")

            for quiz_button in self.quiz_answer_buttons:
                quiz_button.enabled = False

    def handle_timer(self):
        return self

    def render(self, screen):
        time_now = pygame.time.get_ticks()
        if time_now - self.next_question_timeout > 2000 and self.next_question_timeout != 0:
            self.set_question()

        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))

        self.title.render(screen)

        self.question_text.render(screen)

        for quiz_answer_button in self.quiz_answer_buttons:
            quiz_answer_button.render(screen)


class QuizFinishedScreen:
    def __init__(self, num_of_correct_ans, number_of_quiz_questions):

        pygame.mixer.music.stop()
        if num_of_correct_ans >= number_of_quiz_questions - 1:
            info_text = "WOW you're awesome! You get 10 health points as an award! "
            sound("music/kids_cheering.mp3")
            poketer.add_health(10)
        else:
            info_text = f"You need at least {number_of_quiz_questions - 1} correct answers to get a bonus. " \
                        f"Better luck next time!"
            sound("music/booing_crowd.mp3")

        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)

        self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                             font_size=30, font_bold=False, color=WHITE,
                             text=f"You answered {num_of_correct_ans} out of {number_of_quiz_questions} questions correctly.")

        self.info_text = TextBox(rel_pos=(0.5, 0.25), font_name=FONT_ROBOTO,
                                     font_size=25, font_bold=False, color=WHITE, text=info_text, line_width=55)

        self.poketer_image = pygame.image.load("Green_monster_resized.png").convert_alpha()
        self.poketer_image = pygame.transform.smoothscale(self.poketer_image, (207, 207))

        self.quiz_finished_button = Button(rel_pos=(0.5, 0.85), rel_size=(0.3, 0.15),
                                           color=QUIZ_TRANSP_GREEN, highlight=QUIZ_TRANSP_GREEN_HIGHL,
                                           font_size=22, font_color=WHITE, text="CONTINUE")

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            return QuizScreen()
        return self

    def handle_mouse_button(self, mouse_button):
        if self.quiz_finished_button.handle_mouse_button(mouse_button):
            #common.next_screen = QuizStartScreen(5, quiz_categories)
            common.next_screen = return_screen
            music("music/battle_time_1.mp3")

    def handle_timer(self):
        return self

    def render(self, screen):
        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))
        self.title.render(screen)
        self.info_text.render(screen)

        time = pygame.time.get_ticks()
        y_off = 5 * math.sin(time*3.14/1000)

        pixel_pos = rel_to_pix((0.5, 0.55))
        poketer_image_rect = self.poketer_image.get_rect()
        poketer_image_rect.center = pixel_pos[0], pixel_pos[1] + y_off
        screen.blit(self.poketer_image, poketer_image_rect)

        self.quiz_finished_button.render(screen)


def mainloop(screen, font):
    # Initial state
    current_screen = QuizStartScreen(5, quiz_categories, None, None)

    clock = pygame.time.Clock()
    while True:

        # Event handling
        ev = pygame.event.poll()

        if ev.type == pygame.KEYDOWN:
            current_screen = current_screen.handle_keydown(ev.key)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            current_screen.handle_mouse_button(ev.button)

        elif ev.type == pygame.QUIT:
            break

        if common.next_screen is not None:
            print("changing frames to", type(common.next_screen))
            current_screen = common.next_screen
            common.next_screen = None

        current_screen.handle_timer()

        # Render
        current_screen.render(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    common.common_init()

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("PokeMood")
    font = FONT_ROBOTO
    mainloop(screen, font)
    pygame.quit()
