from parameters import *


def print_text(message, x, y, font_color=(0, 0, 0), font_type='text/my.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def print_text0(message, x, y, font_color=(0, 0, 0), font_type='text/my1.otf', font_size=60):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def print_text1(message, x, y, font_color=(255, 0, 0), font_type='text/my1.otf', font_size=35):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))
