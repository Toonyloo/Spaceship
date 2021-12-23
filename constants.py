import pygame
pygame.init()

WIDTH = 600
HEIGHT = 800
SHIP_WIDTH = 80
SHIP_HEIGHT = 80
BULLET_WIDTH = 15
BULLET_HEIGHT = 30
HP_BAR_HEIGHT = 20
BOMB_WIDTH = 35
BOMB_HEIGHT = 50
EXPLOSION_SIZE = 175
DETONATION_TIME = 120
BOMB_DMG = 0.3
LASER_DMG = 5

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

pygame.display.set_mode([WIDTH, HEIGHT])
SHIP1 = pygame.image.load('assets/ship1.png').convert_alpha()
SHIP1 = pygame.transform.scale(SHIP1, (SHIP_WIDTH, SHIP_HEIGHT))

SHIP2 = pygame.image.load('assets/ship2.png').convert_alpha()
SHIP2 = pygame.transform.scale(SHIP2, (SHIP_WIDTH, SHIP_HEIGHT))

LASER1 = pygame.image.load('assets/laser1.png').convert_alpha()
LASER1 = pygame.transform.scale(LASER1, (BULLET_WIDTH, BULLET_HEIGHT))

LASER2 = pygame.image.load('assets/laser2.png').convert_alpha()
LASER2 = pygame.transform.scale(LASER2, (BULLET_WIDTH, BULLET_HEIGHT))

BOMB1 = pygame.image.load('assets/bomb1.png').convert_alpha()
BOMB1 = pygame.transform.scale(BOMB1, (BOMB_WIDTH, BOMB_HEIGHT))

BOMB2 = pygame.image.load('assets/bomb2.png').convert_alpha()
BOMB2 = pygame.transform.scale(BOMB2, (BOMB_WIDTH, BOMB_HEIGHT))

BACKGROUND = pygame.image.load('assets/background.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
BACKGROUND.set_alpha(75)

EXPLOSION = []
for i in range(1, 26):
    explosion = pygame.image.load(f'assets/explosion/{i}.png').convert_alpha()
    explosion = pygame.transform.scale(explosion, (SHIP_WIDTH, SHIP_WIDTH))
    EXPLOSION.append(explosion)

LASER_SFX = pygame.mixer.Sound('assets/lasershoot.wav')
LASER_SFX.set_volume(0.2)

EXPLOSION_SFX = pygame.mixer.Sound('assets/explosion.wav')
EXPLOSION_SFX.set_volume(0.2)

DAMAGE_SFX = pygame.mixer.Sound('assets/damage.wav')
DAMAGE_SFX.set_volume(0.2)

BOMB_SHOOT_SFX = pygame.mixer.Sound('assets/bombshoot.wav')
BOMB_SHOOT_SFX.set_volume(0.2)

BOMB_DETONATE_SFX = pygame.mixer.Sound('assets/bombdetonate.wav')
BOMB_DETONATE_SFX.set_volume(0.2)

FONT = pygame.font.Font('assets/PressStart2P.ttf', 20)
TITLE_FONT = pygame.font.Font('assets/PressStart2P.ttf', 40)
