import pygame
from constants import *
pygame.init()

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet1, self).__init__()
        self.image = LASER1
        self.x = coords[0] + (SHIP_WIDTH - BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.image = LASER1
        LASER_SFX.play()

    def handle_movement(self):
        self.y -= 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet2, self).__init__()
        self.image = LASER2
        self.x = coords[0] + (SHIP_WIDTH - BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        LASER_SFX.play()

    def handle_movement(self):
        self.y += 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bomb1(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bomb1, self).__init__()
        self.image = BOMB1
        self.x = coords[0] + (SHIP_WIDTH - BOMB_WIDTH) / 2
        self.y = coords[1]
        self.detonation = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        BOMB_SHOOT_SFX.play()

    def handle_movement(self):
        self.y -= 8
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def explosion(self):
        self.detonation -= 1
        frame = (self.detonation % 4) + 11
        image = EXPLOSION[frame]
        image = pygame.transform.scale(image, (EXPLOSION_SIZE, EXPLOSION_SIZE))
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def trigger_explosion(self):
        if self.detonation is None:
            BOMB_DETONATE_SFX.play()
            self.x -= EXPLOSION_SIZE / 2
            self.y -= EXPLOSION_SIZE / 2
            self.detonation = DETONATION_TIME

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bomb2(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bomb2, self).__init__()
        self.image = BOMB2
        self.x = coords[0] + (SHIP_WIDTH - BOMB_WIDTH) / 2
        self.y = coords[1]
        self.detonation = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        BOMB_SHOOT_SFX.play()

    def handle_movement(self):
        self.y += 8
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def explosion(self):
        self.detonation -= 1
        frame = (self.detonation % 4) + 11
        image = EXPLOSION[frame]
        image = pygame.transform.scale(image, (EXPLOSION_SIZE, EXPLOSION_SIZE))
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def trigger_explosion(self):
        if self.detonation is None:
            BOMB_DETONATE_SFX.play()
            self.x -= EXPLOSION_SIZE / 2
            self.y -= EXPLOSION_SIZE / 2
            self.detonation = DETONATION_TIME

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
