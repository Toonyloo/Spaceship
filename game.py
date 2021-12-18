import pygame
pygame.init()

WIDTH = 600
HEIGHT = 800
SHIPWIDTH = 70
SHIPHEIGHT = 70
BULLETWIDTH = 10
BULLETHEIGHT = 30
HPBARHEIGHT = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode([WIDTH, HEIGHT])


SHIP1 = pygame.image.load('assets/ship1.png').convert_alpha()
SHIP1 = pygame.transform.scale(SHIP1, (SHIPWIDTH, SHIPHEIGHT))

SHIP2 = pygame.image.load('assets/ship2.png').convert_alpha()
SHIP2 = pygame.transform.scale(SHIP2, (SHIPWIDTH, SHIPHEIGHT))

LASER1 = pygame.image.load('assets/laser1.png').convert_alpha()
LASER1 = pygame.transform.scale(LASER1, (BULLETWIDTH, BULLETHEIGHT))

LASER2 = pygame.image.load('assets/laser2.png').convert_alpha()
LASER2 = pygame.transform.scale(LASER2, (BULLETWIDTH, BULLETHEIGHT))

BACKGROUND = pygame.image.load('assets/background.jpg').convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
BACKGROUND.set_alpha(75)

LASERSHOOT = pygame.mixer.Sound('assets/lasershoot.wav')
LASERSHOOT.set_volume(0.2)

pygame.display.set_caption('Spaceships')
pygame.display.set_icon(SHIP1)


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = SHIP1
        self.x = WIDTH / 2 - SHIPWIDTH / 2
        self.y = HEIGHT - SHIPHEIGHT
        self.xspeed = 0
        self.yspeed = 0
        self.health = 100
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
    
    def handle_input(self, keys):
        self.xspeed = 0
        self.yspeed = 0
        if keys[pygame.K_w]:
            self.yspeed -= 10
        if keys[pygame.K_s]:
            self.yspeed += 10
        if keys[pygame.K_a]:
            self.xspeed -= 10
        if keys[pygame.K_d]:
            self.xspeed += 10
    
    def handle_movement(self):
        if 0 <= (self.xspeed + self.x) <= WIDTH - SHIPWIDTH:
            self.x += self.xspeed
        if HEIGHT / 2 <= (self.yspeed + self.y) <= HEIGHT - SHIPHEIGHT:
            self.y += self.yspeed
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
    
    def draw(self):
        screen.blit(self.surf, (self.x, self.y))
    
    def draw_healthbar(self):
        hpsection = WIDTH * self.health / 100
        remaininghp = pygame.Rect(0, HEIGHT - HPBARHEIGHT, hpsection, HPBARHEIGHT)
        missinghp = pygame.Rect(hpsection, HEIGHT - HPBARHEIGHT, WIDTH - hpsection, HPBARHEIGHT)
        pygame.draw.rect(screen, GREEN, remaininghp)
        pygame.draw.rect(screen, RED, missinghp)


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = SHIP2
        self.x = WIDTH / 2 - SHIPWIDTH / 2
        self.y = 0
        self.xspeed = 0
        self.yspeed = 0
        self.health = 100
    
    def handle_input(self, keys):
        self.xspeed = 0
        self.yspeed = 0
        if keys[pygame.K_UP]:
            self.yspeed -= 10
        if keys[pygame.K_DOWN]:
            self.yspeed += 10
        if keys[pygame.K_LEFT]:
            self.xspeed -= 10
        if keys[pygame.K_RIGHT]:
            self.xspeed += 10

    def handle_movement(self):
        if 0 <= (self.xspeed + self.x) <= WIDTH - SHIPWIDTH:
            self.x += self.xspeed
        if 0 <= (self.yspeed + self.y) <= (HEIGHT / 2) - SHIPHEIGHT:
            self.y += self.yspeed
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))

    def draw(self):
        screen.blit(self.surf, (self.x, self.y))
    
    def draw_healthbar(self):
        hpsection = WIDTH * self.health / 100
        remaininghp = pygame.Rect(0, 0, hpsection, HPBARHEIGHT)
        missinghp = pygame.Rect(hpsection, 0, WIDTH - hpsection, HPBARHEIGHT)
        pygame.draw.rect(screen, GREEN, remaininghp)
        pygame.draw.rect(screen, RED, missinghp)


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, ship):
        super(Bullet1, self).__init__()
        self.surf = LASER1
        self.x = ship.x + (SHIPWIDTH - BULLETWIDTH) / 2
        self.y = ship.y
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
    
    def handle_movement(self):
        bullet.y -= 15
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, ship):
        super(Bullet2, self).__init__()
        self.surf = LASER2
        self.x = ship.x + (SHIPWIDTH - BULLETWIDTH) / 2
        self.y = ship.y
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))

    def handle_movement(self):
        bullet.y += 15
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))


running = True
p1 = Player1()
p2 = Player2()
clock = pygame.time.Clock()
p1bullets = []
p2bullets = []

while running:
    screen.fill(BLACK)
    screen.blit(BACKGROUND, (0, 0))
    pygame.draw.line(screen, WHITE, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
    clock.tick(60)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                LASERSHOOT.play()
                p1bullets.append(Bullet1(p1))
            if event.key == pygame.K_RSHIFT:
                LASERSHOOT.play()
                p2bullets.append(Bullet2(p2))

    p1.handle_input(keys)
    p2.handle_input(keys)
    p1.handle_movement()
    p2.handle_movement()

    for count, bullet in enumerate(p1bullets):
        bullet.handle_movement()
        if pygame.sprite.collide_rect(bullet, p2):
            p2.health -= 10
            del p1bullets[count]
            continue
        if bullet.y < 0:
            del p1bullets[count]
            continue
        screen.blit(bullet.surf, (bullet.x, bullet.y))

    for count, bullet in enumerate(p2bullets):
        bullet.handle_movement()
        if pygame.sprite.collide_rect(bullet, p1):
            p1.health -= 10
            del p2bullets[count]
            continue
        screen.blit(bullet.surf, (bullet.x, bullet.y))
        if bullet.y < 0:
            del p2bullets[count]

    p1.draw_healthbar()
    p2.draw_healthbar()
    p1.draw()
    p2.draw()
    pygame.display.flip()