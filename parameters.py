import pygame

display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height))

usr_width = 200
usr_height = 212
usr_x = display_width//10
usr_y = display_height-usr_height-110

clock = pygame.time.Clock()
