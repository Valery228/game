from sounds import *
from effects import *
from parameters import display


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (137, 102, 64)
        self.active_clr = (110, 90, 205)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_clr, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(click_sound)
                click_sound.set_volume(0.4)
                pygame.time.delay(100)
                if action is not None:
                    if action == quit:
                        quit()
                    else:
                        menu_sound.set_volume(0)
                        action()
        else:
            pygame.draw.rect(display, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message=message, x=x+10, y=y+5, font_size=font_size)
