from sys import exit
import pygame
from random import randint


def game_active_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = main_font.render(f'Gitting Gud score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(topleft=(450, 350))
    screen.blit(score_surface, score_rectangle)


def game_best_score():
    best_score_surface = main_font.render(f'Best Gitting Gud score: {best_score}', False, (64, 64, 64))
    best_score_rectangle = best_score_surface.get_rect(topright=(750, 350))
    screen.blit(best_score_surface, best_score_rectangle)


def enemy_movement(enemies):
    if enemies:
        for enemy in enemies:
            enemy.x -= 6
            if enemy.bottom == 300:
                screen.blit(snail_surface, enemy)
            else:
                screen.blit(fly_surface, enemy)
        enemies = [enemy for enemy in enemies if enemy.right > 0]
        return enemies
    else:
        return []


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Git Gud')
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
clock = pygame.time.Clock()
game_active = False
start_time = 0
best_score = 0

# backgrounds
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# texts
game_over_surface_1 = main_font.render('Git Gud', False, (64, 64, 64))
game_over_rectangle_1 = game_over_surface_1.get_rect(center=(400, 150))

game_over_surface_2 = main_font.render('Press  "SPACE"  to Git Gud', False, (64, 64, 64))
game_over_rectangle_2 = game_over_surface_2.get_rect(center=(400, 250))

# player
player_surface = pygame.image.load('graphics/Player/Player_stand.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# snail
snail_surface = pygame.image.load('graphics/Snail/Snail1.png').convert_alpha()

# fly
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

enemies_rect_list = []

# timers
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1500)

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

        if event.type == spawn_timer and game_active:
            if randint(0, 1):
                enemies_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
            else:
                enemies_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 200)))

    if game_active:
        # environment
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        game_active_score()

        # player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom > 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # enemy movement
        enemies_rect_list = enemy_movement(enemies_rect_list)

        # collisions
        for enemy_rect in enemies_rect_list:
            if player_rectangle.colliderect(enemy_rect):
                if best_score < (pygame.time.get_ticks() - start_time) // 1000:
                    best_score = (pygame.time.get_ticks() - start_time) // 1000
                player_rectangle.bottom = 300
                enemies_rect_list = []
                game_active = False
    else:
        screen.fill('#c0e8ec')
        screen.blit(game_over_surface_1, game_over_rectangle_1)
        screen.blit(game_over_surface_2, game_over_rectangle_2)
        game_best_score()

    pygame.display.update()
    clock.tick(60)
