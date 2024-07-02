from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('test 1')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
