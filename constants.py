import pygame
pygame.init()


class Const:
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
    DETONATION_TIME = 60
    BOMB_DMG = 0.5
    LASER_DMG = 5


class Colours:
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)


class Images:
    pygame.display.set_mode([Const.WIDTH, Const.HEIGHT])
    SHIP1 = pygame.image.load('assets/ship1.png').convert_alpha()
    SHIP1 = pygame.transform.scale(SHIP1, (Const.SHIP_WIDTH, Const.SHIP_HEIGHT))

    SHIP2 = pygame.image.load('assets/ship2.png').convert_alpha()
    SHIP2 = pygame.transform.scale(SHIP2, (Const.SHIP_WIDTH, Const.SHIP_HEIGHT))

    LASER1 = pygame.image.load('assets/laser1.png').convert_alpha()
    LASER1 = pygame.transform.scale(LASER1, (Const.BULLET_WIDTH, Const.BULLET_HEIGHT))

    LASER2 = pygame.image.load('assets/laser2.png').convert_alpha()
    LASER2 = pygame.transform.scale(LASER2, (Const.BULLET_WIDTH, Const.BULLET_HEIGHT))

    BOMB1 = pygame.image.load('assets/bomb1.png').convert_alpha()
    BOMB1 = pygame.transform.scale(BOMB1, (Const.BOMB_WIDTH, Const.BOMB_HEIGHT))

    BOMB2 = pygame.image.load('assets/bomb2.png').convert_alpha()
    BOMB2 = pygame.transform.scale(BOMB2, (Const.BOMB_WIDTH, Const.BOMB_HEIGHT))

    BACKGROUND = pygame.image.load('assets/background.png').convert_alpha()
    BACKGROUND = pygame.transform.scale(BACKGROUND, (Const.WIDTH, Const.HEIGHT))
    BACKGROUND.set_alpha(75)

    EXPLOSION = []
    for i in range(1, 26):
        explosion = pygame.image.load(f'assets/explosion/{i}.png').convert_alpha()
        explosion = pygame.transform.scale(explosion, (Const.SHIP_WIDTH, Const.SHIP_WIDTH))
        EXPLOSION.append(explosion)


class Sfx:
    LASER = pygame.mixer.Sound('assets/lasershoot.wav')
    LASER.set_volume(0.2)

    EXPLOSION = pygame.mixer.Sound('assets/explosion.wav')
    EXPLOSION.set_volume(0.2)

    DAMAGE = pygame.mixer.Sound('assets/damage.wav')
    DAMAGE.set_volume(0.2)

    BOMB_SHOOT = pygame.mixer.Sound('assets/bombshoot.wav')
    BOMB_SHOOT.set_volume(0.2)

    BOMB_DETONATE = pygame.mixer.Sound('assets/bombdetonate.wav')
    BOMB_DETONATE.set_volume(0.2)


class Fonts:
    FONT = pygame.font.Font('assets/PressStart2P.ttf', 20)
    TITLE_FONT = pygame.font.Font('assets/PressStart2P.ttf', 40)
