#Створи власний Шутер!
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = scale(load(player_image), (player_width,player_height))
        self.speed = player_speed
        self.player_width = player_width
        self.player_height = player_height

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed, ammunition):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
        self.ammunition = ammunition

    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= win_width - self.player_width - 10:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x+30, win_height-140, 20, 20, 15)
        bullets.add(bullet)
        self.ammunition -= 1


class Enemy(GameSprite):
    def update(self, pass_counted):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height + 100:
            self.rect.y = -100
            self.rect.x = randint(0, win_width - 100)
            if pass_counted:
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

background = scale(load("galaxy.jpg"), (win_width, win_height))
ship = Player("rocket.png", 320, win_height-120, 80, 100, 5, 10)

menu_background = scale(load("menu/bg_menu.png"), (win_width, win_height))
btn_play = GameSprite('menu/play.png', 280,170,145, 50,0)
btn_setting = scale(load("menu/setting.png"), (145, 40))
btn_quit = scale(load("menu/quit.png"), (145, 50))

monsters = sprite.Group()
for i in range(4):
    en = Enemy("ufo.png", randint(0, win_width-100), -100, 100, 60, randint(1,3))
    monsters.add(en)

asteroids = sprite.Group()
for i in range(4):
    ast = Enemy("asteroid.png", randint(0, win_width-100), -100, 50, 50, randint(1,5))
    asteroids.add(ast)

finish = False
game = True
reload = False

screen = 'menu'

clock = time.Clock()
FPS = 60

mixer.init()

# mixer.music.load("space.ogg")
# mixer.music.play(-1)
# mixer.music.set_volume(0.05)

bg_misic = mixer.Sound("space.ogg")
bg_misic.set_volume(0.05)

bg_misic_menu = mixer.Sound("bg_music.mp3")
bg_misic_menu.set_volume(0.05)

bg_misic.play(-1)
mixer.pause()
bg_misic_menu.play(-1)

reload_sound = mixer.Sound("recharge.ogg")

skip_sound = mixer.Sound("menu/skip.mp3")

font.init()
font1 = font.SysFont('Aria', 30)

txt_gameover = font1.render("GAME OVER", True, (255, 20, 20))

while game:
    if screen == 'game':
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_f:
                    if ship.ammunition > 0 and not reload:
                        ship.fire()

                    if ship.ammunition == 0 and not reload:
                        reload = True
                        start_reload = timer()

        if not finish:

            txt_lose = font1.render(f"Пропущено :{lost}", True, (255, 255, 255))
            txt_score = font1.render(f"Рахунок :{score}", True, (255, 255, 255))
            txt_ammo = font1.render(f"ammo : {ship.ammunition}", True, (230, 230, 230))

            window.blit(background,(0,0))
            window.blit(txt_lose, (0,0))
            window.blit(txt_score, (0,40))
            window.blit(txt_ammo, (600,0))
            monsters.draw(window)
            asteroids.draw(window)
            bullets.draw(window)
            ship.reset()


            monsters.update(True)
            asteroids.update(False)
            bullets.update()
            ship.update()

            if sprite.groupcollide(bullets, monsters, True, True):
                score += 1
                en = Enemy("ufo.png", randint(0, win_width - 100), -100, 100, 60, randint(1, 3))
                monsters.add(en)

            if sprite.spritecollide(ship, asteroids, False) or lost == 5:
                finish = True
                window.blit(txt_gameover, (280, 250))

            if reload:
                now_time = timer()
                delta = now_time - start_reload
                if delta <= 2:
                    txt_reload = font1.render("Зачекайте йде перезарядка", True, (255, 40, 40))
                    window.blit(txt_reload, (200, 350))
                    reload_sound.play()
                else:
                    ship.ammunition = 10
                    reload = False

        else:
            pass

    if screen == 'menu':
        for e in event.get():
            if e.type == QUIT:
                game = False

        window.blit(menu_background, (0, 0))

        btn_play.reset()
        window.blit(btn_setting, (280, 240))
        window.blit(btn_quit, (280, 300))

        if e.type == MOUSEBUTTONDOWN:
            mouse_click = e.pos
            if btn_play.rect.collidepoint(mouse_click):
                bg_misic_menu.stop()
                skip_sound.play()
                mixer.unpause()

                screen = 'game'

    display.update()
    clock.tick(FPS)