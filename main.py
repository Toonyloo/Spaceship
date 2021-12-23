import pygame
from constants import Const, Colours, Images, Sfx, Fonts
import players

pygame.init()
screen = pygame.display.set_mode([Const.WIDTH, Const.HEIGHT])

pygame.display.set_caption('Spaceship')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

clock = pygame.time.Clock()


def draw_game():
    screen.fill(Colours.BLACK)
    screen.blit(Images.BACKGROUND, (0, 0))
    pygame.draw.line(screen, Colours.WHITE, (0, Const.HEIGHT/2), (Const.WIDTH, Const.HEIGHT/2))
    hp_section = Const.WIDTH * p1.health / 100
    remaining_hp = pygame.Rect(0, Const.HEIGHT - Const.HP_BAR_HEIGHT, hp_section, Const.HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, Const.HEIGHT - Const.HP_BAR_HEIGHT, Const.WIDTH - hp_section, Const.HP_BAR_HEIGHT)
    pygame.draw.rect(screen, Colours.GREEN, remaining_hp)
    pygame.draw.rect(screen, Colours.RED, missing_hp)

    hp_section = Const.WIDTH * p2.health / 100
    remaining_hp = pygame.Rect(0, 0, hp_section, Const.HP_BAR_HEIGHT)
    missing_hp = pygame.Rect(hp_section, 0, Const.WIDTH - hp_section, Const.HP_BAR_HEIGHT)
    pygame.draw.rect(screen, Colours.GREEN, remaining_hp)
    pygame.draw.rect(screen, Colours.RED, missing_hp)

    p1_ammo_txt = Fonts.FONT.render(f'Ammo:{p1.ammo}', True, Colours.WHITE)
    p2_ammo_txt = Fonts.FONT.render(f'Ammo:{p2.ammo}', True, Colours.WHITE)
    p1_ammo_width, p1_ammo_height = Fonts.FONT.size(f'Ammo:{p1.ammo}')
    p2_ammo_width, p2_ammo_height = Fonts.FONT.size(f'Ammo:{p2.ammo}')
    screen.blit(p1_ammo_txt, (Const.WIDTH - p1_ammo_width, Const.HEIGHT - Const.HP_BAR_HEIGHT - p1_ammo_height))
    screen.blit(p2_ammo_txt, (Const.WIDTH - p2_ammo_width, Const.HP_BAR_HEIGHT))

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


def handle_collisions():
    for attacker, defender in ((p1, p2), (p2, p1)):
        for count, bullet in enumerate(attacker.bullets):
            if pygame.sprite.collide_mask(bullet, defender):
                Sfx.DAMAGE.play()
                defender.health -= Const.LASER_DMG
                del attacker.bullets[count]

        if attacker.bomb is not None:
            if attacker.bomb.detonation is None:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    attacker.bomb.trigger_explosion()
            else:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    defender.health -= Const.BOMB_DMG


running = True
p1 = players.Player1()
p2 = players.Player2()
ammo_timer = 0
loser = None

while running:
    clock.tick(60)
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
            p1.bomb = None
            p2.bomb = None
            p1.bullets = []
            p2.bullets = []
            Sfx.EXPLOSION.play()
            continue
        if p2.health <= 0:
            loser = p2
            animation_timer = 0
            p1.bomb = None
            p2.bomb = None
            p1.bullets = []
            p2.bullets = []
            Sfx.EXPLOSION.play()
            continue

        p1.handle_all_logic(keys, events)
        p2.handle_all_logic(keys, events)

        handle_collisions()
        draw_game()

    else:
        if animation_timer < 150:
            frame = animation_timer // 6
            animation_timer += 1
            draw_game()
            screen.blit(Images.EXPLOSION[frame], (loser.x, loser.y))
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        p1 = players.Player1()
                        p2 = players.Player2()
                        loser = None
            screen.blit(Images.BACKGROUND, (0, 0))
            msg = 'PLAY AGAIN?'
            msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
            text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
            screen.blit(text, ((Const.WIDTH - msg_width) // 2, Const.HEIGHT // 2 - msg_height - 20))

            msg = '(Press Space)'
            msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
            text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
            screen.blit(text, ((Const.WIDTH - msg_width) // 2, Const.HEIGHT // 2 + 20))

    pygame.display.flip()
