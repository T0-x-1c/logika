#Створи власний Шутер!
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint

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
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= win_width - self.player_width - 10:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x+30, win_height-140, 20, 20, 15)
        bullets.add(bullet)


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


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

background = scale(load("galaxy.jpg"), (win_width, win_height))
ship = Player("rocket.png", 320, win_height-120, 80, 100, 5)


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

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)
mixer.music.set_volume(0.05)

font.init()
font1 = font.SysFont('Aria', 30)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        font_lose = font1.render(f"Пропущено :{lost}", True, (255, 255, 255))
        font_score = font1.render(f"Рахунок :{score}", True, (255, 255, 255))

        window.blit(background,(0,0))
        window.blit(font_lose, (0,0))
        window.blit(font_score, (0,40))
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        ship.reset()


        monsters.update(True)
        asteroids.update(False)
        bullets.update()
        ship.update()

        key_pressed = key.get_pressed()
        if key_pressed[K_f]:
            ship.fire()

    display.update()
    clock.tick(FPS)