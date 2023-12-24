#Створи власний Шутер!
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer

global lost
global score
lost = 0
score = 0

# def button_illumination(btn,standart_image, custom_image, x, y, width, hight, btn_illumination):
#     if btn_illumination == True:
#         btn = GameSprite(f'{custom_image}', x, y, width, hight, 0)
#     else:
#         btn = GameSprite(f'{standart_image}', x, y, width, hight, 0)
#
#     return btn

def restart(monsters, asteroids):
    monsters.empty()
    asteroids.empty()

    for i in range(4):
        en = Enemy("picture/ufo.png", randint(0, win_width - 100), -100, 100, 60, randint(1, 3))
        monsters.add(en)

    for i in range(4):
        ast = Enemy("picture/asteroid.png", randint(0, win_width - 100), -100, 50, 50, randint(1, 5))
        asteroids.add(ast)

    ship.rect.x = 320
    ship.hp = 3
    ship.ammunition = 10
    score = 0
    lost = 0




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
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed, ammunition, hp):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
        self.ammunition = ammunition
        self.hp = hp

    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= win_width - self.player_width - 10:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("picture/bullet.png", self.rect.x+30, win_height-140, 20, 20, 15)
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

background = scale(load("picture/galaxy.jpg"), (win_width, win_height))
ship = Player("picture/rocket.png", 320, win_height-120, 80, 100, 5, 10, 3)

menu_background = scale(load("menu/bg_menu.png"), (win_width, win_height))
btn_play = GameSprite('menu/play.png', 280, 170, 145, 50, 0)
btn_setting = GameSprite('menu/setting.png', 280, 240, 145, 45, 0)
btn_quit = GameSprite('menu/quit.png', 280, 300, 145, 50, 0)

btn_restart = GameSprite('menu/restart.png', 270, 300, 145, 40, 0)
btn_menu = GameSprite('menu/menu.png', 290, 350, 110, 30, 0)
btn_back = GameSprite('menu/back_button.png', 10, 10, 55, 40, 0)


monsters = sprite.Group()
for i in range(4):
    en = Enemy("picture/ufo.png", randint(0, win_width-100), -100, 100, 60, randint(1,3))
    monsters.add(en)

asteroids = sprite.Group()
for i in range(4):
    ast = Enemy("picture/asteroid.png", randint(0, win_width-100), -100, 50, 50, randint(1,5))
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

bg_misic = mixer.Sound("sounds\space.ogg")
bg_misic.set_volume(0.05)

bg_misic_menu = mixer.Sound("sounds/bg_music.mp3")
bg_misic_menu.set_volume(0.05)

bg_misic.play(-1)
mixer.pause()
bg_misic_menu.play(-1)

reload_sound = mixer.Sound("sounds/recharge.ogg")

fire_sound = mixer.Sound("sounds/fire.ogg")
fire_sound.set_volume(0.1)

damage_sound = mixer.Sound("sounds/damage.mp3")
damage_sound.set_volume(0.5)

skip_sound = mixer.Sound("sounds/skip.mp3")

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
                        fire_sound.play()

                    if ship.ammunition == 0 and not reload:
                        reload = True
                        start_reload = timer()


        txt_lose = font1.render(f"Пропущено :{lost}", True, (255, 255, 255))
        txt_score = font1.render(f"Рахунок :{score}", True, (255, 255, 255))
        txt_ammo = font1.render(f"ammo : {ship.ammunition}", True, (230, 230, 230))
        txt_hp = font1.render(f"hp : {ship.hp}", True, (230, 230, 230))

        window.blit(background,(0,0))
        window.blit(txt_lose, (0,0))
        window.blit(txt_score, (0,40))
        window.blit(txt_ammo, (600,0))
        window.blit(txt_hp, (600,40))
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
            en = Enemy("picture/ufo.png", randint(0, win_width - 100), -100, 100, 60, randint(1, 3))
            monsters.add(en)

        if sprite.spritecollide(ship, asteroids, True):
            ship.hp -= 1
            damage_sound.play()

        if ship.hp <= 0 or lost >= 5:
            monsters.empty()
            asteroids.empty()

            window.blit(txt_gameover, (280, 250))
            btn_restart.reset()
            btn_menu.reset()

            if e.type == MOUSEBUTTONDOWN:
                mouse_click = e.pos
                if btn_restart.rect.collidepoint(mouse_click):
                    restart(monsters, asteroids)

                if btn_menu.rect.collidepoint(mouse_click):
                    restart(monsters, asteroids)
                    screen = 'menu'
                    mixer.pause()
                    bg_misic_menu.play()

        if reload:
            now_time = timer()
            delta = now_time - start_reload
            if delta <= 2:
                txt_reload = font1.render("Зачекайте йде перезарядка", True, (255, 40, 40))
                window.blit(txt_reload, (200, 350))

            else:
                ship.ammunition = 10
                reload = False
                reload_sound.play(1)


    if screen == 'menu':
        for e in event.get():
            if e.type == QUIT:
                game = False

        window.blit(menu_background, (0, 0))

        btn_play.reset()
        btn_setting.reset()
        btn_quit.reset()

        mouse_pos = mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]


        if btn_play.rect.collidepoint(mouse_pos):
            btn_play = GameSprite('menu/play_2.png', 280,170,145, 50,0)
        else:
            btn_play = GameSprite('menu/play.png', 280, 170, 145, 50, 0)

        if btn_setting.rect.collidepoint(mouse_pos):
            btn_setting = GameSprite('menu/setting_2.png', 280, 240,145, 45,0)
        else:
            btn_setting = GameSprite('menu/setting.png', 280, 240,145, 45,0)

        if btn_quit.rect.collidepoint(mouse_pos):
            btn_quit = GameSprite('menu/quit_2.png', 280,300,145, 50,0)
        else:
            btn_quit = GameSprite('menu/quit.png', 280,300,145, 50,0)


        if e.type == MOUSEBUTTONDOWN:
            mouse_click = e.pos
            if btn_play.rect.collidepoint(mouse_click):
                bg_misic_menu.stop()
                skip_sound.play()
                mixer.unpause()

                screen = 'game'

            if btn_setting.rect.collidepoint(mouse_click):
                skip_sound.play()

                screen = 'setting'

            if btn_quit.rect.collidepoint(mouse_click):
                game = False


    if screen == 'setting':
        for e in event.get():
            if e.type == QUIT:
                game = False

        window.blit(menu_background, (0, 0))

        btn_back.reset()

        if e.type == MOUSEBUTTONDOWN:
            mouse_click = e.pos
            if btn_back.rect.collidepoint(mouse_click):
                screen = 'menu'



    display.update()
    clock.tick(FPS)