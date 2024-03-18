import pygame
import os
import random

WIDTH=600
HEIGHT=700
FPS=60

WHITE=(255,255,255)
BLUE=(0,0,255)
GREEN=(0,255,0)

#遊戲初始化
pygame.init()
pygame.mixer.init()

#創建視窗
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
pygame.display.set_caption("Spaceship")

#載入圖片
background_img=pygame.image.load(os.path.join("背景.png")).convert()
spaceship_img=pygame.image.load(os.path.join("小飛船.png")).convert()
spaceship_lives_img=pygame.transform.scale(spaceship_img,(25,25))
spaceship_lives_img.set_colorkey(WHITE)
pygame.display.set_icon(spaceship_img)
meteorite_imgs=[]
for i in range(6):
    meteorite_imgs.append(pygame.image.load(os.path.join(f"隕石{i}.png")).convert())
explode_imgs={}
explode_imgs['large']=[]
explode_imgs['small']=[]
explode_imgs['spaceship']=[]
for i in range(8):
    explode_img = pygame.image.load(os.path.join(f"爆炸{i}.png")).convert()
    explode_img.set_colorkey(WHITE)
    explode_imgs['large'].append(pygame.transform.scale(explode_img,(75,75)))
    explode_imgs['small'].append(pygame.transform.scale(explode_img, (30, 30)))
    explode_imgs['spaceship'].append(pygame.transform.scale(explode_img, (80, 80)))
bullet_img=pygame.image.load(os.path.join("子彈.png")).convert()
power_imgs={}
power_imgs['shield'] = pygame.image.load(os.path.join("盾牌.png")).convert()
power_imgs['flash'] = pygame.image.load(os.path.join("閃電.png")).convert()
font_name=pygame.font.match_font("arial")
#載入音樂
shoot_sound=pygame.mixer.Sound(os.path.join("子彈.mp3"))
explode_sound=pygame.mixer.Sound(os.path.join("爆炸.mp3"))
pygame.mixer.music.load(os.path.join("BGM.mp3"))
pygame.mixer.music.set_volume(0.2)
die_sound=pygame.mixer.Sound(os.path.join("飛船爆炸.mp3"))

def new_meteorite():
    m=Meteorite()
    all_sprites.add(m)
    meteorites.add(m)

#打擊分數
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,BLUE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

#血量
def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=(hp/100)*BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,BLUE,outline_rect,2)

#剩幾條命
def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)

#遊戲初始畫面
def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,"Spaceship",70,WIDTH/2,HEIGHT/4)
    draw_text(screen, "← →Mobile spaceship  ↑Fire Bullets", 30, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press Enter to start the game", 25, WIDTH / 2, HEIGHT*3/ 4)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting=False
                return  False

#小飛船
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=spaceship_img
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=20
        self.rect.center=(WIDTH/2,HEIGHT-50)
        self.health=100
        self.lives=3
        self.hidden = False
        self.hide_time = 0
        self.flash = 1
        self.flash_time =0

    def update(self):
        now = pygame.time.get_ticks()
        if self.flash > 1 and now - self.flash_time > 5000:
            self.flash -= 1
            self.flash_time = now

        if self.hidden and now-self.hide_time > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 50)

        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 5
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 5

        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH

    def shoot(self):
        if not(self. hidden):
            if self.flash == 1:
                bullet=Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.flash >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time= pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+500)

    def flashup(self):
        self.flash += 1
        self.flash_time = pygame.time.get_ticks()

#隕石
class Meteorite(pygame. sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori =random.choice(meteorite_imgs)
        self.image_ori.set_colorkey(WHITE)
        self.image=self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x =random.randrange (0, WIDTH-30)
        self.rect.y = random.randrange(-100, -40)
        self.speedx=random.randrange(-2,2)
        self.speedy = random.randrange(2, 6)
        self.total_degree=0
        self.rot_degree=random.randrange(-5,5)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center

    def update(self):
        self.rotate()
        self.rect.x +=self.speedx
        self.rect.y +=self.speedy
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x = random.randrange(0, WIDTH - 30)
            self.rect.y = random.randrange(-180, -40)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(2, 6)

#子彈
class Bullet(pygame. sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(30,30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx =x
        self.rect.bottom=y
        self.speedy = -10

    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom<0:
            self.kill()

#爆炸動畫
class Explosion(pygame. sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explode_imgs[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explode_imgs[self.size]):
                self.kill()
            else:
                self.image = explode_imgs[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#掉寶
class Power(pygame. sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['shield','flash'])
        self.image=power_imgs[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()

#sprite群
all_sprites=pygame.sprite.Group()
meteorites=pygame.sprite.Group()
bullets=pygame.sprite.Group()
powers=pygame.sprite.Group()
spaceship=Spaceship()
all_sprites.add(spaceship)
score=0
for i in range(8):
    new_meteorite()
pygame.mixer.music.play(-1)

#遊戲迴圈
show_init=True
running=True
while running:
    if show_init:
        close=draw_init()
        if close:
            break
        show_init=False
        # sprite群
        all_sprites = pygame.sprite.Group()
        meteorites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        spaceship = Spaceship()
        all_sprites.add(spaceship)
        score = 0
        for i in range(8):
            new_meteorite()

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                spaceship.shoot()

    #更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(meteorites,bullets,True,True)
    for hit in hits:
        explode_sound.play()
        score += hit.radius
        explode = Explosion(hit.rect.center, 'large')
        all_sprites.add(explode)
        if random.random()>0.4:
            power=Power(hit.rect.center)
            all_sprites.add(power)
            powers.add(power)
        new_meteorite()

    hits=pygame.sprite.spritecollide(spaceship,meteorites,True,pygame.sprite.collide_circle)
    for hit in hits:
        new_meteorite()
        spaceship.health-=hit.radius
        explode = Explosion(hit.rect.center, 'small')
        all_sprites.add(explode)
        if spaceship.health<=0:
            die=Explosion(hit.rect.center, 'spaceship')
            all_sprites.add(die)
            die_sound.play()
            spaceship.lives -= 1
            spaceship.health = 100
            spaceship.hide()

    hits = pygame.sprite.spritecollide(spaceship, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            spaceship.health += 20
            if spaceship.health > 100:
                spaceship.health =100
        elif hit.type == 'flash':
            spaceship.flashup()

    if spaceship.lives == 0 and not(die.alive()):
        running=False

    #畫面顯示
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,spaceship.health,5,15)
    draw_lives(screen,spaceship.lives,spaceship_lives_img,WIDTH-100,15)
    pygame.display.update()