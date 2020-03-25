import pygame
import time
import os
import random as r
pygame.font.init()

WIN_W = 550
WIN_H = 800
win = pygame.display.set_mode((WIN_W, WIN_H))

frank_imgs = [pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'frank1.png'))), (100, 100)), 
             pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'frank2.png'))), (100, 100)),
             pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'frank3.png'))), (100, 100))]
back_img = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'background.png'))), (600, 800))
can_img = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'can.png'))), (150, 600))
base_img = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'base.png'))), (600, 100))
frank_start_img = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'frank1.png'))), (175, 175))

font = pygame.font.SysFont('comicsans', 50)

def start_screen():
    start = True 

    while start:
        clock.tick(30)
        win.blit(back_img, (0,0))
        base = Base(700)
        base.draw(win)
        win.blit(frank_start_img, (190, 170))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
        
class Frank:
    IMGS = frank_imgs
    max_rotation = 25
    rotation_vel = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        dis = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        
        if dis >= 16:
            dis = 16
        
        if dis < 0:
            dis -= 2
        
        self.y = self.y + dis  

        if dis < 0 or self.y < self.height + 50:
            self.tilt = 0
        else:
            if self.tilt > -90:
                self.tilt -= self.rotation_vel
    
    def draw(self, win):
        self.img_count += 1

        if self.img_count <= self.animation_time:
            self.img = self.IMGS[0]
        elif self.img_count <= self.animation_time*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.animation_time*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.animation_time*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.animation_time*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.animation_time*2

        rotate(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Trashcan:
    GAP = 250
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.can_top = pygame.transform.flip(can_img, False, True)
        self.can_bottom = can_img
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = r.randrange(50,450)
        self.top = self.height - self.can_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.can_top, (self.x, self.top))
        win.blit(self.can_bottom, (self.x, self.bottom))

    def collide(self, frank):
        frank_mask = frank.get_mask()
        top_mask = pygame.mask.from_surface(self.can_top)
        bottom_mask = pygame.mask.from_surface(self.can_bottom)

        top_offset = (self.x - frank.x, self.top - round(frank.y))
        bottom_offset = (self.x - frank.x, self.bottom - round(frank.y))

        b_point = frank_mask.overlap(bottom_mask, bottom_offset)
        t_point = frank_mask.overlap(top_mask, top_offset)
        
        if b_point or t_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1, self.y))
        win.blit(self.IMG,(self.x2, self.y))



def rotate(surf, image, topleft, angle):
    rotated_img = pygame.transform.rotate(image, angle)
    new_rect = rotated_img.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_img, new_rect.topleft)

def draw_win(win,frank, trashcans, base, score):
    win.blit(back_img, (0,0))

    for can in trashcans:
        can.draw(win)

    text = font.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (WIN_W - 10 - text.get_width(), 10))

    base.draw(win)
    frank.draw(win)
    pygame.display.update()

def run():
    score = 0
    run = True

    frank = Frank(230,350)
    base = Base(700)
    cans = [Trashcan(700)]

    while run:
        clock.tick(30)
        frank.move()
        base.move()
        rem = []
        add_can = False

        for can in cans:
            if can.collide(frank):
                pygame.quit()
                quit()
                break

            if can.x + can.can_top.get_width() < 0:
                rem.append(can)

            if not can.passed and can.x + 100 < frank.x:
                can.passed = True
                add_can = True

            can.move()

        if add_can:
            score += 1
            cans.append(Trashcan(WIN_W))

        for i in rem:
            cans.remove(i)

        if frank.y + frank.img.get_height() >= 710:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                frank.jump()
    
        draw_win(win, frank, cans, base, score)

def main():
    global clock 
    clock = pygame.time.Clock()
    
    start_screen()
    run()
    
    

main()