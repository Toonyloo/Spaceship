import pygame
from constants import Const, Images, Sfx
pygame.init()


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet1, self).__init__()
        self.image = Images.LASER1
        self.x = coords[0] + (Const.SHIP_WIDTH - Const.BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.image = Images.LASER1
        Sfx.LASER.play()

    def handle_movement(self):
        self.y -= 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet2, self).__init__()
        self.image = Images.LASER2
        self.x = coords[0] + (Const.SHIP_WIDTH - Const.BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        Sfx.LASER.play()

    def handle_movement(self):
        self.y += 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bomb1(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bomb1, self).__init__()
        self.image = Images.BOMB1
        self.x = coords[0] + (Const.SHIP_WIDTH - Const.BOMB_WIDTH) / 2
        self.y = coords[1]
        self.detonation = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        Sfx.BOMB_SHOOT.play()

    def handle_movement(self):
        self.y -= 8
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def explosion(self):
        self.detonation -= 1
        frame = (self.detonation % 4) + 11
        image = Images.EXPLOSION[frame]
        image = pygame.transform.scale(image, (Const.EXPLOSION_SIZE, Const.EXPLOSION_SIZE))
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def trigger_explosion(self):
        if self.detonation is None:
            self.image = Images.EXPLOSION[13]
            self.x -= (Const.EXPLOSION_SIZE - Const.BOMB_WIDTH) / 2
            self.y -= (Const.EXPLOSION_SIZE - Const.BOMB_HEIGHT) / 2
            self.detonation = Const.DETONATION_TIME
            Sfx.BOMB_DETONATE.play()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Bomb2(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bomb2, self).__init__()
        self.image = Images.BOMB2
        self.x = coords[0] + (Const.SHIP_WIDTH - Const.BOMB_WIDTH) / 2
        self.y = coords[1]
        self.detonation = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        Sfx.BOMB_SHOOT.play()

    def handle_movement(self):
        self.y += 8
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def explosion(self):
        self.detonation -= 1
        frame = (self.detonation % 4) + 11
        image = Images.EXPLOSION[frame]
        image = pygame.transform.scale(image, (Const.EXPLOSION_SIZE, Const.EXPLOSION_SIZE))
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def trigger_explosion(self):
        if self.detonation is None:
            self.image = Images.EXPLOSION[13]
            self.x -= (Const.EXPLOSION_SIZE - Const.BOMB_WIDTH) / 2
            self.y -= (Const.EXPLOSION_SIZE - Const.BOMB_HEIGHT) / 2
            self.detonation = Const.DETONATION_TIME
            Sfx.BOMB_DETONATE.play()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
