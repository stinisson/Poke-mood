import math
import textwrap
import pygame

BLACK = (0, 0, 0)
screen_size = (800, 600)


def common_init():
    global next_screen
    next_screen = None


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


def periodic_movement(frequency, amplitude):
    time = pygame.time.get_ticks()
    x_off = amplitude * math.cos(frequency * time * math.pi / 1000)
    y_off = amplitude * math.sin(time * math.pi / 1000)
    return x_off, y_off
