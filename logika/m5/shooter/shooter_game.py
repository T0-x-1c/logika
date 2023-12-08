#Створи власний Шутер!
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint

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
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= win_width - self.player_width - 10:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

    def fire(self):
        pass

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

background = scale(load("galaxy.jpg"), (win_width, win_height))
ship = Player("rocket.png", 320, win_height-120, 80, 100, 5)

finish = False
game = True

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)
mixer.music.set_volume(0.05)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background,(0,0))

        ship.reset()
        ship.update()

    display.update()
    clock.tick(FPS)