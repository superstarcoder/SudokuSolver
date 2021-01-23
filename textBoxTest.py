import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((480, 360))
name = ""
font = pygame.font.Font(None, 50)
done = False
while not done:
    for evt in pygame.event.get():
        if evt.type == KEYDOWN:
            if evt.unicode.isalpha():
                name += evt.unicode
            elif evt.key == K_BACKSPACE:
                name = name[:-1]
            elif evt.key == K_RETURN:
                name = ""
        elif evt.type == QUIT:
            done = True
    screen.fill((0, 0, 0))
    block = font.render(name, True, (255, 255, 255))
    rect = block.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(block, rect)
    pygame.display.flip()
