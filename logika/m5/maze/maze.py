#створи гру "Лабіринт"!
import time

from pygame import *
from pygame.sprite import collide_rect
from pygame.transform import scale, flip
from pygame.image import load
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = scale(load(player_image), (70,70))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def run(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed

        if key_pressed[K_s] and self.rect.y <= win_h - 75:
            self.rect.y += self.speed

        if key_pressed[K_d] and self.rect.x <= win_w - 75:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed


class Enemy(GameSprite):
    direction = 'left'
    def run(self):
        if self.rect.x <= 450:
            self.direction = 'right'

        elif self.rect.x >= 600:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed

        if self.direction == 'right':
            self.rect.x += self.speed



win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))

background = scale(image.load("background.jpg"), (win_w, win_h))

player = Player('hero.png', 5, win_h - 70, 4)
cyborg = Enemy('cyborg.png', win_w - 100, win_h - 300, 2)
money = GameSprite('treasure.png', win_w - 150, win_h - 90, 0)

clock = time.Clock()
FPS = 60
game = True
finish = False

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play(-1)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0,0))

        player.reset()
        cyborg.reset()
        money.reset()

        cyborg.run()
        player.run()

    else:
        window.blit(background, (0, 0))

        player.reset()
        cyborg.reset()

    display.update()
    clock.tick(FPS)