import pygame
import random
from collections import deque
from constants import Const, Images, Fonts, Colours
import projectiles


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.image = Images.SHIP1
        self.x = Const.WIDTH / 2 - Const.SHIP_WIDTH / 2
        self.y = (Const.HEIGHT - Const.HEIGHT // 4) - Const.SHIP_HEIGHT
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
                    if self.health < 20:
                        self.bullets.append(projectiles.Bullet1((self.x, self.y)))
                    elif self.ammo > 0:
                        self.ammo -= 1
                        self.bullets.append(projectiles.Bullet1((self.x, self.y)))
                if event.key == pygame.K_f:
                    if self.bomb is None:
                        self.bomb = projectiles.Bomb1((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= Const.WIDTH - Const.SHIP_WIDTH:
            self.x += self.x_speed
        if Const.HEIGHT / 2 <= (self.y_speed + self.y) <= Const.HEIGHT - Const.SHIP_HEIGHT - Const.HP_BAR_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def draw_ammo_txt(self, screen):
        if self.health < 20:
            msg = 'Ammo:OVERLOADED!!'
            txt = Fonts.FONT.render(msg, True, Colours.RED)
        else:
            msg = f'Ammo:{self.ammo}'
            txt = Fonts.FONT.render(msg, True, Colours.WHITE)
        txt_width, txt_height = Fonts.FONT.size(msg)
        screen.blit(txt, (Const.WIDTH - txt_width, Const.HEIGHT - Const.HP_BAR_HEIGHT - txt_height))

    def draw_hpbar(self, screen):
        pygame.draw.line(screen, Colours.WHITE, (0, Const.HEIGHT/2), (Const.WIDTH, Const.HEIGHT/2))
        hp_section = Const.WIDTH * self.health / 100
        remaining_hp = pygame.Rect(0, Const.HEIGHT - Const.HP_BAR_HEIGHT, hp_section, Const.HP_BAR_HEIGHT)
        missing_hp = pygame.Rect(hp_section, Const.HEIGHT - Const.HP_BAR_HEIGHT, Const.WIDTH - hp_section, Const.HP_BAR_HEIGHT)
        pygame.draw.rect(screen, Colours.GREEN, remaining_hp)
        pygame.draw.rect(screen, Colours.RED, missing_hp)

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if bullet.y < 0:
                del self.bullets[count]
                continue

    def handle_bomb(self):
        if self.bomb is None:
            return
        if self.bomb.y < 0 - Const.BOMB_HEIGHT:
            self.bomb = None
            return

        if self.bomb.detonation is None:
            self.bomb.handle_movement()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
        elif self.bomb.detonation == 0:
            self.bomb = None

    def handle_all_logic(self):
        self.handle_movement()
        self.handle_bullets()
        self.handle_bomb()


class Player2(pygame.sprite.Sprite):
    def __init__(self, cpu=False):
        super(Player2, self).__init__()
        self.image = Images.SHIP2
        self.x = Const.WIDTH / 2 - Const.SHIP_WIDTH / 2
        self.y = Const.HEIGHT // 4
        self.x_speed = 0
        self.y_speed = 0
        self.health = 100
        self.ammo = 10
        self.bullets = []
        self.bomb = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        if cpu:
            self.ai_move_delay = deque()
            self.shoot_cd = 0
            self.start_delay = 40

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
                    if self.health < 20:
                        self.bullets.append(projectiles.Bullet2((self.x, self.y)))
                    elif self.ammo > 0:
                        self.ammo -= 1
                        self.bullets.append(projectiles.Bullet2((self.x, self.y)))
                if event.key == pygame.K_SLASH:
                    if self.bomb is None:
                        self.bomb = projectiles.Bomb2((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_ai_input(self, player):
        rand = random.random()
        if self.start_delay > 0:
            self.start_delay -= 1
            return
        
        if rand > 0.9:
            self.ai_move_delay.append(random.choice((-10, 0, 10)))
        elif self.x < player.x:
            self.ai_move_delay.append(10)
        elif self.x > player.x:
            self.ai_move_delay.append(-10)
        else:
            self.ai_move_delay.append(0)
        
        if len(self.ai_move_delay) > 15:
            self.x_speed = self.ai_move_delay.popleft()
        
        if self.y_speed == 0:
            self.y_speed = 10
        else:
            if rand > 0.98:
                self.y_speed = -self.y_speed
        
        if self.ammo > 0:
            if self.shoot_cd == 0:
                self.bullets.append(projectiles.Bullet2((self.x, self.y)))
                self.ammo -= 1
                self.shoot_cd = rand * 25 + 5
            else:
                self.shoot_cd -= 1
        
        if self.bomb is None:
            self.bomb = projectiles.Bomb2((self.x, self.y))
        elif self.bomb.detonation is None:
            if self.bomb.y > player.y:
                self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= Const.WIDTH - Const.SHIP_WIDTH:
            self.x += self.x_speed
        if Const.HP_BAR_HEIGHT <= (self.y_speed + self.y) <= (Const.HEIGHT / 2) - Const.SHIP_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def draw_ammo_txt(self, screen):
        if self.health < 20:
            msg = 'Ammo:OVERLOADED!!'
            txt = Fonts.FONT.render(msg, True, Colours.RED)
        else:
            msg = f'Ammo:{self.ammo}'
            txt = Fonts.FONT.render(msg, True, Colours.WHITE)
        txt_width, txt_height = Fonts.FONT.size(msg)
        screen.blit(txt, (Const.WIDTH - txt_width, Const.HP_BAR_HEIGHT))

    def draw_hpbar(self, screen):
        hp_section = Const.WIDTH * self.health / 100
        remaining_hp = pygame.Rect(0, 0, hp_section, Const.HP_BAR_HEIGHT)
        missing_hp = pygame.Rect(hp_section, 0, Const.WIDTH - hp_section, Const.HP_BAR_HEIGHT)
        pygame.draw.rect(screen, Colours.GREEN, remaining_hp)
        pygame.draw.rect(screen, Colours.RED, missing_hp)

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if bullet.y > Const.HEIGHT + Const.BULLET_HEIGHT:
                del self.bullets[count]

    def handle_bomb(self):
        if self.bomb is None:
            return
        if self.bomb.y > Const.HEIGHT:
            self.bomb = None
            return

        if self.bomb.detonation is None:
            self.bomb.handle_movement()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
        elif self.bomb.detonation == 0:
            self.bomb = None

    def handle_all_logic(self):
        self.handle_movement()
        self.handle_bullets()
        self.handle_bomb()

