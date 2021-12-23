import pygame
from constants import *
import players

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('Spaceship')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

clock = pygame.time.Clock()


def draw_game():
    screen.fill(BLACK)
    screen.blit(BACKGROUND, (0, 0))
    pygame.draw.line(screen, WHITE, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
    hp_section = WIDTH * p1.health / 100
    remaining_hp = pygame.Rect(0, HEIGHT - HP_BAR_HEIGHT, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, HEIGHT -HP_BAR_HEIGHT, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    hp_section = WIDTH * p2.health / 100
    remaining_hp = pygame.Rect(0, 0, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, 0, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    p1_ammo_txt = FONT.render(f'Ammo:{p1.ammo}', True, WHITE)
    p2_ammo_txt = FONT.render(f'Ammo:{p2.ammo}', True, WHITE)
    p1_ammo_width, p1_ammo_height = FONT.size(f'Ammo:{p1.ammo}')
    p2_ammo_width, p2_ammo_height = FONT.size(f'Ammo:{p2.ammo}')
    screen.blit(p1_ammo_txt, (WIDTH - p1_ammo_width, HEIGHT - HP_BAR_HEIGHT - p1_ammo_height))
    screen.blit(p2_ammo_txt, (WIDTH - p2_ammo_width, HP_BAR_HEIGHT))

    for bullet in p1.bullets:
        bullet.draw(screen)
    for bullet in p2.bullets:
        bullet.draw(screen)

    if p1.bomb is not None:
        p1.bomb.draw(screen)
    if p2.bomb is not None:
        p2.bomb.draw(screen)

    p1.draw(screen)
    p2.draw(screen)


def draw_explosion_animation(frame):
    screen.fill(BLACK)
    screen.blit(BACKGROUND, (0, 0))
    pygame.draw.line(screen, WHITE, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
    hp_section = WIDTH * p1.health / 100
    remaining_hp = pygame.Rect(0, HEIGHT - HP_BAR_HEIGHT, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, HEIGHT - HP_BAR_HEIGHT, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    hp_section = WIDTH * p2.health / 100
    remaining_hp = pygame.Rect(0, 0, hp_section, HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, 0, WIDTH - hp_section, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, remaining_hp)
    pygame.draw.rect(screen, RED, missing_hp)

    p1.draw(screen)
    p2.draw(screen)

    screen.blit(EXPLOSION[frame], (loser.x, loser.y))


def handle_collisions():
    for attacker, defender in ((p1, p2), (p2, p1)):
        for count, bullet in enumerate(attacker.bullets):
            if pygame.sprite.collide_mask(bullet, defender):
                DAMAGE_SFX.play()
                defender.health -= LASER_DMG
                del attacker.bullets[count]

        if attacker.bomb is not None:
            if attacker.bomb.detonation is None:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    attacker.bomb.trigger_explosion()
            else:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    defender.health -= BOMB_DMG


running = True
p1 = players.Player1()
p2 = players.Player2()
ammo_timer = 0
loser = None

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if loser is None:
        if ammo_timer < 30:
            ammo_timer += 1
        else:
            ammo_timer = 0
            if p1.ammo < 10:
                p1.ammo += 1
            if p2.ammo < 10:
                p2.ammo += 1

        if p1.health <= 0:
            loser = p1
            animation_timer = 0
            EXPLOSION_SFX.play()
            continue
        if p2.health <= 0:
            loser = p2
            animation_timer = 0
            EXPLOSION_SFX.play()
            continue

        p1.handle_all_logic(keys, events)
        p2.handle_all_logic(keys, events)

        handle_collisions()
        draw_game()

    else:
        if animation_timer < 150:
            frame = animation_timer // 6
            draw_explosion_animation(frame)
            animation_timer += 1
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        p1 = players.Player1()
                        p2 = players.Player2()
                        loser = None
            screen.blit(BACKGROUND, (0, 0))
            msg = 'PLAY AGAIN?'
            msg_width, msg_height = TITLE_FONT.size(msg)
            text = TITLE_FONT.render(msg, True, WHITE)
            screen.blit(text, ((WIDTH - msg_width) // 2, HEIGHT // 2 - msg_height - 20))

            msg = '(Press Space)'
            msg_width, msg_height = TITLE_FONT.size(msg)
            text = TITLE_FONT.render(msg, True, WHITE)
            screen.blit(text, ((WIDTH - msg_width) // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
