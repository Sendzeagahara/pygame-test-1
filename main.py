from sys import exit
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/Player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/Player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/Jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        y_pos = 0
        if self.name == 'fly':
            fly_surface1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_surface2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_surface1, fly_surface2]
            y_pos = 210
        elif self.name == 'snail':
            snail_surface1 = pygame.image.load('graphics/Snail/Snail1.png').convert_alpha()
            snail_surface2 = pygame.image.load('graphics/Snail/Snail2.png').convert_alpha()
            self.frames = [snail_surface1, snail_surface2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        if self.name == 'fly':
            self.animation_index += 0.1
        elif self.name == 'snail':
            self.animation_index += 0.05
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def collision_sprite():
    global best_score
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        if best_score < (pygame.time.get_ticks() - start_time) // 1000:
            best_score = (pygame.time.get_ticks() - start_time) // 1000
        return False
    else:
        return True


def game_active_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = main_font.render(f'Gitting Gud score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(topleft=(450, 350))
    screen.blit(score_surface, score_rectangle)


def game_best_score():
    best_score_surface = main_font.render(f'Best Gitting Gud score: {best_score}', False, (64, 64, 64))
    best_score_rectangle = best_score_surface.get_rect(topright=(750, 350))
    screen.blit(best_score_surface, best_score_rectangle)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Git Gud')
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
clock = pygame.time.Clock()
game_active = False
start_time = 0
best_score = 0

# player
player = pygame.sprite.GroupSingle()
player.add(Player())

# enemies
obstacle_group = pygame.sprite.Group()

# backgrounds
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# texts
game_over_surface_1 = main_font.render('Git Gud', False, (64, 64, 64))
game_over_rectangle_1 = game_over_surface_1.get_rect(center=(400, 150))

game_over_surface_2 = main_font.render('Press  "SPACE"  to Git Gud', False, (64, 64, 64))
game_over_rectangle_2 = game_over_surface_2.get_rect(center=(400, 250))

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
            if event.type == spawn_timer and game_active:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        # environment
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        game_active_score()

        # player
        player.draw(screen)
        player.update()

        # obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collisions
        game_active = collision_sprite()
    else:
        screen.fill('#c0e8ec')
        screen.blit(game_over_surface_1, game_over_rectangle_1)
        screen.blit(game_over_surface_2, game_over_rectangle_2)
        game_best_score()

    pygame.display.update()
    clock.tick(60)
