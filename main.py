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

    p1.draw_hpbar(screen)
    p2.draw_hpbar(screen)
    p1.draw_ammo_txt(screen)
    p2.draw_ammo_txt(screen)

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
            if defender.bomb is not None:
                if pygame.sprite.collide_mask(bullet, defender.bomb):
                    defender.bomb.trigger_explosion()
                    del attacker.bullets[count]

        if attacker.bomb is not None:
            if attacker.bomb.detonation is None:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    attacker.bomb.trigger_explosion()
            else:
                if pygame.sprite.collide_mask(attacker.bomb, defender):
                    defender.health -= Const.BOMB_DMG
                if pygame.sprite.collide_mask(attacker.bomb, attacker):
                    attacker.health -= Const.BOMB_DMG
            if defender.bomb is not None:
                if pygame.sprite.collide_mask(attacker.bomb, defender.bomb):
                    attacker.bomb.trigger_explosion()
                    defender.bomb.trigger_explosion()


running = True
p1 = players.Player1()
p2 = players.Player2()
ammo_timer = 0
loser = None
mode = None

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if mode == None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                    p1 = players.Player1()
                    p2 = players.Player2(cpu=True)
                if event.key == pygame.K_2:
                    mode = 2
                    p1 = players.Player1()
                    p2 = players.Player2()

        screen.blit(Images.BACKGROUND, (0, 0))
        msg = '1 Player Mode'
        msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
        text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
        screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 - msg_height - 50))
        msg = '(Press 1)'
        msg_width, msg_height = Fonts.FONT.size(msg)
        text = Fonts.FONT.render(msg, True, Colours.WHITE)
        screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 - msg_height - 20))
        msg = '2 Player Mode'
        msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
        text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
        screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 + 20))
        msg = '(Press 2)'
        msg_width, msg_height = Fonts.FONT.size(msg)
        text = Fonts.FONT.render(msg, True, Colours.WHITE)
        screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 - msg_height + 90))
        
    elif loser is None:
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

        p1.handle_input(keys, events)
        if mode == 1:
            p2.handle_ai_input(p1)
        if mode == 2:
            p2.handle_input(keys, events)
        p1.handle_all_logic()
        p2.handle_all_logic()

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
                        loser = None
                        mode = None
            screen.blit(Images.BACKGROUND, (0, 0))
            msg = 'PLAY AGAIN?'
            msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
            text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
            screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 - msg_height - 20))

            msg = '(Press Space)'
            msg_width, msg_height = Fonts.TITLE_FONT.size(msg)
            text = Fonts.TITLE_FONT.render(msg, True, Colours.WHITE)
            screen.blit(text, ((Const.WIDTH - msg_width) / 2, Const.HEIGHT / 2 + 20))

    pygame.display.flip()
