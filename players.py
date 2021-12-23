import pygame
from constants import *
import projectiles

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.image = SHIP1
        self.x = WIDTH / 2 - SHIP_WIDTH / 2
        self.y = (HEIGHT - HEIGHT // 4) - SHIP_HEIGHT
        self.x_speed = 0
        self.y_speed = 0
        self.health = 100
        self.ammo = 10
        self.bullets = []
        self.bomb = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_input(self, keys, events):
        self.x_speed = 0
        self.y_speed = 0
        if keys[pygame.K_w]:
            self.y_speed -= 10
        if keys[pygame.K_s]:
            self.y_speed += 10
        if keys[pygame.K_a]:
            self.x_speed -= 10
        if keys[pygame.K_d]:
            self.x_speed += 10

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.ammo > 0:
                        self.ammo -= 1
                        self.bullets.append(projectiles.Bullet1((self.x, self.y)))
                if event.key == pygame.K_f:
                    if self.bomb is None:
                        self.bomb = projectiles.Bomb1((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= WIDTH - SHIP_WIDTH:
            self.x += self.x_speed
        if HEIGHT / 2 <= (self.y_speed + self.y) <= HEIGHT - SHIP_HEIGHT - HP_BAR_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if bullet.y < 0:
                del self.bullets[count]
                continue

    def handle_bomb(self):
        if self.bomb is None:
            return
        if self.bomb.y < 0 - BOMB_HEIGHT:
            self.bomb = None
            return

        if self.bomb.detonation is None:
            self.bomb.handle_movement()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
        elif self.bomb.detonation == 0:
            self.bomb = None

    def handle_all_logic(self, keys, events):
        self.handle_input(keys, events)
        self.handle_movement()
        self.handle_bullets()
        self.handle_bomb()


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.image = SHIP2
        self.x = WIDTH / 2 - SHIP_WIDTH / 2
        self.y = HEIGHT // 4
        self.x_speed = 0
        self.y_speed = 0
        self.health = 100
        self.ammo = 10
        self.bullets = []
        self.bomb = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_input(self, keys, events):
        self.x_speed = 0
        self.y_speed = 0
        if keys[pygame.K_UP]:
            self.y_speed -= 10
        if keys[pygame.K_DOWN]:
            self.y_speed += 10
        if keys[pygame.K_LEFT]:
            self.x_speed -= 10
        if keys[pygame.K_RIGHT]:
            self.x_speed += 10

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    if self.ammo > 0:
                        self.ammo -= 1
                        self.bullets.append(projectiles.Bullet2((self.x, self.y)))
                if event.key == pygame.K_SLASH:
                    if self.bomb is None:
                        self.bomb = projectiles.Bomb2((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= WIDTH - SHIP_WIDTH:
            self.x += self.x_speed
        if HP_BAR_HEIGHT <= (self.y_speed + self.y) <= (HEIGHT / 2) - SHIP_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if bullet.y > HEIGHT + BULLET_HEIGHT:
                del self.bullets[count]

    def handle_bomb(self):
        if self.bomb is None:
            return
        if self.bomb.y > HEIGHT:
            self.bomb = None
            return

        if self.bomb.detonation is None:
            self.bomb.handle_movement()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
        elif self.bomb.detonation == 0:
            self.bomb = None

    def handle_all_logic(self, keys, events):
        self.handle_input(keys, events)
        self.handle_movement()
        self.handle_bullets()
        self.handle_bomb()
