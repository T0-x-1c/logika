import pygame
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer
import json

win_width = 700
win_height = 500

lost = 0
score = 0

with open('settings.json', 'r', encoding='utf-8') as set_file:
    settings = json.load(set_file)

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

ship = Player("picture/rocket.png", 320, win_height-120, 80, 100, 5, 10, 3)
bullet = Bullet("picture/bullet.png", 1, 1, 20, 20, 15)
window = display.set_mode((win_width, win_height))