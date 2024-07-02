from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('test-1')
clock = pygame.time.Clock()
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

greet_surface = main_font.render('Runner?', False, (64, 64, 64))
greet_rectangle = greet_surface.get_rect(center=(400, 50))

player_surface = pygame.image.load('graphics/Player/Player_stand.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

snail_surface = pygame.image.load('graphics/Snail/Snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))

fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_rectangle = fly_surface.get_rect(midbottom=(1000, 200))

while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                player_gravity = -20

    #environment
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, '#c0e8ec', greet_rectangle, border_radius=3)
    screen.blit(greet_surface, greet_rectangle)

    #player
    player_gravity += 1
    player_rectangle.y += player_gravity
    if player_rectangle.bottom > 300:
        player_rectangle.bottom = 300
    screen.blit(player_surface, player_rectangle)

    #snail
    snail_rectangle.x -= 6
    if snail_rectangle.right <= 0:
        snail_rectangle.left = 800
    screen.blit(snail_surface, snail_rectangle)

    #fly
    fly_rectangle.x -= 6
    if fly_rectangle.right <= 0:
        fly_rectangle.left = 800
    screen.blit(fly_surface, fly_rectangle)

    #collisions

    pygame.display.update()
    clock.tick(60)
