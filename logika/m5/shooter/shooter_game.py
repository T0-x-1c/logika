#Створи власний Шутер!
import pygame
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import json

with open('settings.json', 'r', encoding='utf-8') as set_file:
    settings = json.load(set_file)

pygame.init()
mixer.init()

'''змінні'''
lost = 0
score = 0

win_width = 700
win_height = 500

finish = False
game = True
reload = False
shop_open = False

screen = 'menu'

FPS = 60

def save_setting():
    with open('settings.json', 'w', encoding='utf-8') as set_file:
        json.dump(settings, set_file, ensure_ascii=False, sort_keys=True, indent=4)

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
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 100)
            if pass_counted:
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((win_width, win_height))
bullets = sprite.Group()

'''об'єкти для гри'''
background = scale(load("picture/galaxy.jpg"), (win_width, win_height))
ship = Player("picture/rocket.png", 320, win_height-120, 80, 100, 5, settings["ammunition"], settings["hp"])
bullet = Bullet("picture/bullet.png", 1, 1, 20, 20, 15)

monsters = sprite.Group()
for i in range(4):
    en = Enemy("picture/ufo.png", randint(0, win_width-100), -100, 100, 60, randint(1,3))
    monsters.add(en)

asteroids = sprite.Group()
for i in range(4):
    ast = Enemy("picture/asteroid.png", randint(0, win_width-100), -100, 50, 50, randint(1,5))
    asteroids.add(ast)

'''об'єкти для меню'''
menu_background = scale(load("menu/bg_menu.png"), (win_width, win_height))
btn_play = GameSprite('menu/play.png', 280, 170, 145, 50, 0)
btn_setting = GameSprite('menu/setting.png', 280, 240, 145, 45, 0)
btn_quit = GameSprite('menu/quit.png', 280, 300, 145, 50, 0)

btn_restart = GameSprite('menu/restart.png', 270, 300, 145, 40, 0)
btn_menu = GameSprite('menu/menu.png', 290, 350, 110, 30, 0)

btn_back = GameSprite('menu/back_button.png', 10, 10, 55, 40, 0)
btn_save = GameSprite('menu/save.png', 30, 430, 110, 30, 0)

shop_ico = GameSprite('shop/shop_ico.png', 530, 180, 170, 170, 0)
shop = GameSprite('shop/shop.png', 100, 70, 500, 360, 0)
shop_ammo = GameSprite('shop/ammo.png', 170, 170, 100, 160, 0)
shop_hp = GameSprite('shop/hp.png', 300, 170, 100, 160, 0)

'''об'єкти для налаштувань'''
music_loudness = Slider(window, 470, 100, 150, 5, min=0, max=1, step=0.01, handleColour = (180, 245, 245), handleRadius=8)
music_loudness.setValue(settings["music_loudness"])
music_output = TextBox(window, 460, 130, 50, 30, fontSize=20)
music_output.disable()

game_sound_loudness = Slider(window, 470, 220, 150, 5, min=0, max=1, step=0.01, handleColour = (180, 245, 245), handleRadius=8)
game_sound_loudness.setValue(settings["game_sound_loudness"])
game_sound_output = TextBox(window, 460, 250, 50, 30, fontSize=20)
game_sound_output.disable()

clock = time.Clock()

'''звуки'''
bg_misic = mixer.Sound("sounds\space.ogg")
bg_misic.set_volume(settings["music_loudness"])

bg_misic_menu = mixer.Sound("sounds/bg_music.mp3")
bg_misic_menu.set_volume(settings["music_loudness"])

bg_misic.play(-1)
mixer.pause()
bg_misic_menu.play(-1)

reload_sound = mixer.Sound("sounds/recharge.mp3")
reload_sound.set_volume(settings["game_sound_loudness"])

fire_sound = mixer.Sound("sounds/fire.ogg")
fire_sound.set_volume(settings["game_sound_loudness"])

damage_sound = mixer.Sound("sounds/damage.mp3")
damage_sound.set_volume(settings["game_sound_loudness"])

skip_sound = mixer.Sound("sounds/skip.mp3")
skip_sound.set_volume(0.8)
skip_sound2 = mixer.Sound("sounds/skip_2.mp3")
skip_sound2.set_volume(0.05)

fail_sound = mixer.Sound("sounds/fail.mp3")
fail_sound.set_volume(0.3)

'''тексти'''
font.init()
font1 = font.SysFont('Aria', 30)

txt_gameover = font1.render("GAME OVER", True, (255, 20, 20))

txt_loudness_music = font1.render("гучність музики :", True, (180, 245, 245))
txt_game_sound = font1.render("гучність звуків гри :", True, (180, 245, 245))

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
        txt_score = font1.render(f'Рахунок :{settings["score"]}', True, (255, 255, 255))
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
            settings["score"] += 1
            save_setting()
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

                    lost = 0

                if btn_menu.rect.collidepoint(mouse_click):
                    restart(monsters, asteroids)
                    lost = 0

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
                ship.ammunition = settings["ammunition"]
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

        shop_ico.reset()

        mouse_pos = mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if shop_open:
            shop.reset()
            shop_ammo.reset()
            shop_hp.reset()

            txt_ammo_price = font1.render(f'{settings["ammo_price"]}', True, (255,255,255))
            txt_hp_price = font1.render(f'{settings["hp_price"]}', True, (255,255,255))
            txt_score = font1.render(f'{settings["score"]}', True, (255,255,255))

            window.blit(txt_ammo_price, (210, 302))
            window.blit(txt_hp_price, (340, 302))
            window.blit(txt_score, (230, 387))
            if e.type == MOUSEBUTTONDOWN:
                mouse_click = e.pos
                if shop_ammo.rect.collidepoint(mouse_click):
                    if settings["score"] >= settings["ammo_price"]:
                        settings["score"] -= settings["ammo_price"]
                        settings["ammunition"] += 1
                        settings["ammo_price"] = round(settings["ammo_price"] * 1.2)
                        ship.ammunition = settings["ammunition"]
                        save_setting()
                        skip_sound2.play()
                    else:
                        fail_sound.play()

                if shop_hp.rect.collidepoint(mouse_click):
                    if settings["score"] >= settings["hp_price"]:
                        settings["score"] -= settings["hp_price"]
                        settings["hp"] += 1
                        settings["hp_price"] = round(settings["hp_price"] * 1.2)
                        ship.hp = settings["hp"]
                        save_setting()
                        skip_sound2.play()
                    else:
                        fail_sound.play()

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

        if shop_ico.rect.collidepoint(mouse_pos):
            shop_ico = GameSprite('shop/shop_ico_2.png', 530, 180, 170, 170, 0)
        else:
            shop_ico = GameSprite('shop/shop_ico.png', 530, 180, 170, 170, 0)


        if e.type == MOUSEBUTTONDOWN and not shop_open:
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

            if shop_ico.rect.collidepoint(mouse_click):
                shop_open = True


    if screen == 'setting':
        for e in event.get():
            if e.type == QUIT:
                game = False

        window.blit(menu_background, (0, 0))
        window.blit(txt_loudness_music, (460, 40))
        window.blit(txt_game_sound, (460, 180))

        btn_back.reset()
        btn_save.reset()

        music_output.setText(round(music_loudness.getValue(), 2))
        game_sound_output.setText(round(game_sound_loudness.getValue(), 2))

        pygame_widgets.update(e)

        if e.type == MOUSEBUTTONDOWN:
            mouse_click = e.pos
            if btn_back.rect.collidepoint(mouse_click):
                screen = 'menu'
                skip_sound.play()

            if btn_save.rect.collidepoint(mouse_click):
                bg_misic_menu.set_volume(round(music_loudness.getValue(), 2))
                bg_misic.set_volume(round(music_loudness.getValue(), 2))
                skip_sound2.play()

                reload_sound.set_volume(round(game_sound_loudness.getValue(), 2))
                fire_sound.set_volume(round(game_sound_loudness.getValue(), 2))
                damage_sound.set_volume(round(game_sound_loudness.getValue(), 2))

                settings["game_sound_loudness"] = round(game_sound_loudness.getValue(), 2)
                settings["music_loudness"] = round(music_loudness.getValue(), 2)
                save_setting()

        mouse_pos = mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if btn_save.rect.collidepoint(mouse_pos):
            btn_save = GameSprite('menu/save_2.png', 30, 430, 110, 30, 0)
        else:
            btn_save = GameSprite('menu/save.png', 30, 430, 110, 30, 0)

        if btn_back.rect.collidepoint(mouse_pos):
            btn_back = GameSprite('menu/back_button_2.png', 10, 10, 55, 40, 0)
        else:
            btn_back = GameSprite('menu/back_button.png', 10, 10, 55, 40, 0)

    display.update()
    clock.tick(FPS)