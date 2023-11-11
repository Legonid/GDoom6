from pygame import *
from random import randint
import pygame
pygame.init()

score = 0
lost = 0

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (0, 0, 0))

font.init()
font2 = font.SysFont('Arial', 36)

mixer.init()
mixer.music.load('Doomus.ogg')
mixer.music.play()
fire_sound = mixer.Sound('Domlaser.ogg')

img_back = 'Hell.png'
img_hero = 'Doom_Slayer.png'
img_enemy = 'Demon.png'
img_bullet = 'BFG.png'
score = 0
goal = 10
lost = 0
max_lost = 10
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y) 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

win_width = 600
win_height = 600
display.set_caption("DOOM 6")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("Hell.png"), (win_width, win_height))

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 6))
    monsters.add(monster)

finish = False
run = True
x = -10
y = -10

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:         
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 90))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.update()
        bullets.update()

        monsters.draw(window)

        for m in monsters:

            if m.collidepoint(x,y):
                m.kill()
                score = score + 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 6))
                monsters.add(monster)

        if score >= goal:
            finish = True
            window.blit(win, (150, 200))

        if lost >= max_lost:
            finish = True
            window.blit(lose, (150, 200))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 6))
            monsters.add(monster)


    time.delay(7)