from pygame import *
from random import randint
from time import time as timer
 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOST', True, (180, 0, 0))
font2 = font.Font(None, 36)
 
img_back = "galaxy.jpg"
img_enemy = "ufo.png"
img_hero = "rocket.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
 
score = 0
goal = 10
lost = 0
max_lost = 3
life = 3
num_fire = 0
rel_time = False
 
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
        keys  = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
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
            self.rect.x = randint(70, win_width - 70)
            self.rect.y = 0
            lost = lost + 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 
win_width = 1280
win_height = 740
window = display.set_mode((win_width, win_height))
display.set_caption('Стрелка')
background = transform.scale(image.load(img_back), (win_width, win_height))
 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 10):
    monster = Enemy(img_enemy,randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast,randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)
 
bullets = sprite.Group()
finish = False
run = True
 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 8 and rel_time ==  False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True 
            
 
    if not finish:
        window.blit(background,(0, 0))  
 
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render('Пропущенно: ' + str(lost), 1,  (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        text_life = font2.render('Жизни ' + str(life), 1,  (255, 255, 255))
        window.blit(text_life, (10, 80))
 
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
 
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
 
        if rel_time == True:
            now_time = timer()
 
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...',1,(150, 0, 0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False
 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
 
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True) 
            life = life -1
 
            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))
 
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
 
        if life == 3:
            life_color = (0,150,0)
            if life == 2:
                life_color = (150,150,0)
            if life == 1:
                life_color = (150, 0, 0)
 
            text_life = font1.render(str(life), 3, life_color)
            window.blit(text_life, (650, 30))
        display.update()
 
    time.delay(50)
