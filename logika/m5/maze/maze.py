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
        self.image = scale(load(player_image), (60,60))
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
    def __init__(self, player_image, player_x, player_y, player_speed, min_x, max_x):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.min_x = min_x
        self.max_x = max_x

    direction = 'left'
    def run(self):
        if self.rect.x <= self.min_x:
            self.direction = 'right'

        elif self.rect.x >= self.max_x:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed

        if self.direction == 'right':
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.color = (51,255,181)

        self.image = Surface((width, height))

        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))

background = scale(image.load("background.jpg"), (win_w, win_h))

font.init()
f = font.Font(None, 40)
win = f.render("Win!!!", True, (255,255,0))
lose = f.render("Lose!!!", True, (255,0,0))

player = Player('hero.png', 5, win_h - 70, 3)
cyborg = Enemy('cyborg.png', win_w - 100, win_h - 300, 2, min_x = 480, max_x = 600)
money = GameSprite('treasure.png', win_w - 150, win_h - 90, 0)

clock = time.Clock()
FPS = 60
game = True
finish = False

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play(-1)

money_sound = mixer.Sound("money.ogg")
kick_sound = mixer.Sound("kick.ogg")

wall1 = Wall(100, 330, 110, 6)
wall2 = Wall(100, 420, 190, 6)
wall3 = Wall(206, 35, 6, 300)
wall4 = Wall(286, 115, 6, 369)
wall5 = Wall(206, 35, 450, 6)
wall6 = Wall(286, 115, 100, 6)
wall7 = Wall(386, 115, 6, 140)
wall8 = Wall(302, 255, 90, 6)
wall9 = Wall(456, 115, 6, 215)
wall10 = Wall(382, 325, 80, 6)
wall11 = Wall(302, 255, 6, 215)

all_wall = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11]

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0,0))

        player.reset()
        cyborg.reset()
        money.reset()

        for wall in all_wall:
            wall.reset()

        cyborg.run()
        player.run()

        if sprite.collide_rect(player, money):
            window.blit(win, (300,250))
            finish = True
            money_sound.play()

        for wall in all_wall:
            if sprite.collide_rect(player, wall):
                window.blit(lose, (300, 250))
                finish = True
                kick_sound.play()

        if sprite.collide_rect(player, cyborg):
            window.blit(lose, (300,250))
            finish = True
            kick_sound.play()

    display.update()
    clock.tick(FPS)