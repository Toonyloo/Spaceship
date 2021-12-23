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

screen = pygame.display.set_mode([WIDTH, HEIGHT])

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

pygame.display.set_caption('Spaceships')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

clock = pygame.time.Clock()


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

    def handle_input(self):
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
                        LASER_SFX.play()
                        self.bullets.append(Bullet1((self.x, self.y)))
                if event.key == pygame.K_f:
                    if self.bomb is None:
                        self.bomb = Bomb1((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= WIDTH - SHIP_WIDTH:
            self.x += self.x_speed
        if HEIGHT / 2 <= (self.y_speed + self.y) <= HEIGHT - SHIP_HEIGHT - HP_BAR_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if pygame.sprite.collide_mask(bullet, p2):
                DAMAGE_SFX.play()
                p2.health -= LASER_DMG
                del self.bullets[count]
                continue
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
            if pygame.sprite.collide_mask(self.bomb, p2):
                self.bomb.trigger_explosion()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
            if pygame.sprite.collide_mask(self.bomb, p1):
                p1.health -= BOMB_DMG
            if pygame.sprite.collide_mask(self.bomb, p2):
                p2.health -= BOMB_DMG
        elif self.bomb.detonation == 0:
            self.bomb = None


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

    def handle_input(self):
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
                        LASER_SFX.play()
                        self.bullets.append(Bullet2((self.x, self.y)))
                if event.key == pygame.K_SLASH:
                    if self.bomb is None:
                        self.bomb = Bomb2((self.x, self.y))
                    else:
                        self.bomb.trigger_explosion()

    def handle_movement(self):
        if 0 <= (self.x_speed + self.x) <= WIDTH - SHIP_WIDTH:
            self.x += self.x_speed
        if HP_BAR_HEIGHT <= (self.y_speed + self.y) <= (HEIGHT / 2) - SHIP_HEIGHT:
            self.y += self.y_speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def handle_bullets(self):
        for count, bullet in enumerate(self.bullets):
            bullet.handle_movement()
            if pygame.sprite.collide_mask(bullet, p1):
                DAMAGE_SFX.play()
                p1.health -= LASER_DMG
                del self.bullets[count]
                continue
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
            if pygame.sprite.collide_mask(self.bomb, p1):
                self.bomb.trigger_explosion()
        elif self.bomb.detonation > 0:
            self.bomb.explosion()
            if pygame.sprite.collide_mask(self.bomb, p1):
                p1.health -= BOMB_DMG
            if pygame.sprite.collide_mask(self.bomb, p2):
                p2.health -= BOMB_DMG
        elif self.bomb.detonation == 0:
            self.bomb = None


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet1, self).__init__()
        self.image = LASER1
        self.x = coords[0] + (SHIP_WIDTH - BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_movement(self):
        self.y -= 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, coords):
        super(Bullet2, self).__init__()
        self.image = LASER2
        self.x = coords[0] + (SHIP_WIDTH - BULLET_WIDTH) / 2
        self.y = coords[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_movement(self):
        self.y += 15
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def draw_game():
    screen.fill(BLACK)
    screen.blit(BACKGROUND, (0, 0))
    pygame.draw.line(screen, WHITE, (0, HEIGHT/2), (WIDTH, HEIGHT/2))

    hp_section = WIDTH * p1.health / 100
    remaining_hp = pygame.Rect(
        0, HEIGHT - HP_BAR_HEIGHT, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, HEIGHT -
                             HP_BAR_HEIGHT, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    hp_section = WIDTH * p2.health / 100
    remaining_hp = pygame.Rect(0, 0, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(
        hp_section, 0, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    p1_ammo_txt = FONT.render(f'Ammo:{p1.ammo}', True, WHITE)
    p2_ammo_txt = FONT.render(f'Ammo:{p2.ammo}', True, WHITE)
    p1_ammo_width, p1_ammo_height = FONT.size(f'Ammo:{p1.ammo}')
    p2_ammo_width, p2_ammo_height = FONT.size(f'Ammo:{p2.ammo}')
    screen.blit(p1_ammo_txt, (WIDTH - p1_ammo_width,
                HEIGHT - HP_BAR_HEIGHT - p1_ammo_height))
    screen.blit(p2_ammo_txt, (WIDTH - p2_ammo_width, HP_BAR_HEIGHT))

    for bullet in p1.bullets:
        bullet.draw()
    for bullet in p2.bullets:
        bullet.draw()

    if p1.bomb is not None:
        p1.bomb.draw()
    if p2.bomb is not None:
        p2.bomb.draw()

    p1.draw()
    p2.draw()


def explosion_animation(ship):
    EXPLOSION_SFX.play()
    for frame in EXPLOSION:
        clock.tick(FPS//5)
        draw_game()
        screen.blit(frame, (ship.x, ship.y))
        pygame.display.flip()


running = True
p1 = Player1()
p2 = Player2()
ammo_timer = 0

while running:
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if ammo_timer < 30:
        ammo_timer += 1
    else:
        ammo_timer = 0
        if p1.ammo < 10:
            p1.ammo += 1
        if p2.ammo < 10:
            p2.ammo += 1

    for player in (p1, p2):
        if player.health <= 0:
            explosion_animation(player)
            p1 = Player1()
            p2 = Player2()
            continue

        player.handle_input()
        player.handle_movement()
        player.handle_bullets()
        player.handle_bomb()

    draw_game()

    pygame.display.flip()
