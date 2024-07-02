from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('test-1')
clock = pygame.time.Clock()
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

greet_surface = main_font.render('test 1', False, 'Black')
greet_rectangle = greet_surface.get_rect(center=(400, 80))

player_surface = pygame.image.load('graphics/Player/Player_stand.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))

snail_surface = pygame.image.load('graphics/Snail/Snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(greet_surface, greet_rectangle)

    screen.blit(player_surface, player_rectangle)

    snail_rectangle.x -= 6
    if snail_rectangle.right <= 0:
        snail_rectangle.left = 800
    screen.blit(snail_surface, snail_rectangle)

    if player_rectangle.colliderect(snail_rectangle):
        print(1)

    pygame.display.update()
    clock.tick(60)
