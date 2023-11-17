from pygame import *


#створи вікно гри
window = display.set_mode((700, 500))

#задай фон сцени
background = transform.scale(image.load("background.png"), (700,500))

#створи 2 спрайти та розмісти їх на сцені
sprite1 = transform.scale(image.load("sprite1.png"), (70,70))
x1 = 0
y1 = 430
sprite2 = transform.scale(image.load("sprite2.png"), (70,70))
x2 = 630
y2 = 430

#оброби подію «клік за кнопкою "Закрити вікно"»
game = True
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0,0))

    window.blit(sprite1, (x1,y1))
    window.blit(sprite2, (x2,y2))

    key_pressed = key.get_pressed()

    if key_pressed[K_w]:
        if y1 > 0:
            y1 -= 5

    if key_pressed[K_s]:
        if y1 < 430:
            y1 += 5

    if key_pressed[K_d]:
        if x1 < 630:
            x1 += 5

    if key_pressed[K_a]:
        if x1 > 0:
            x1 -= 5


    if key_pressed[K_UP]:
        if y2 > 0:
            y2 -= 5

    if key_pressed[K_DOWN]:
        if y2 < 430:
            y2 += 5

    if key_pressed[K_RIGHT]:
        if x2 < 630:
            x2 += 5

    if key_pressed[K_LEFT]:
        if x2 > 0:
            x2 -= 5


    display.update()
    clock.tick(FPS)