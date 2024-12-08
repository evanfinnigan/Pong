# Pong game by Evan

import pygame
import math
from random import randint

pygame.init()

screen = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()
fps = 60

pygame.font.init()
my_font = pygame.font.Font("BowlbyOneSC-Regular.ttf", 24)
score_a = my_font.render("0", True, "white")
score_b = my_font.render("0", True, "white")

def distance(a, b):
    return math.sqrt((b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y))

class Picture():
    def __init__(self,x,y,w,h,filename):
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.transform.scale(pygame.image.load(filename), (w,h))
    def draw(self, shift=0):
        # pygame.draw.rect(screen,'red',self.rect,width=1) # debug
        screen.blit(self.image, (self.rect.x + shift, self.rect.y))

class Paddle(Picture):
    def __init__(self,x,y,radius,filename,k_up,k_down):
        super().__init__(x,y,radius*2,radius*2,filename)
        self.radius = radius
        self.k_up = k_up
        self.k_down = k_down
        self.score = 0
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.k_up]:
            self.rect.y -= 5
        if keys[self.k_down]:
            self.rect.y += 5

class Puck(Picture):
    def __init__(self,x,y,radius,filename):
        super().__init__(x,y,radius*2,radius*2,filename)
        self.radius = radius
        self.drop_puck()
    def drop_puck(self):
        self.speed = 4
        self.rect.x = 385
        self.rect.y = 235
        self.angle = randint(0,360)
        self.speed_x = self.speed * math.cos(self.angle * 180 / math.pi)
        self.speed_y = self.speed * math.sin(self.angle * 180 / math.pi)
    def move(self):
        # collide wall top
        if self.speed_y < 0 and self.rect.y < 10:
            self.speed_y = abs(self.speed_y)
        # collide wall bottom
        if self.speed_y > 0 and self.rect.y > 430:
            self.speed_y = -1 * abs(self.speed_y)
        # collide wall left
        if self.speed_x < 0 and self.rect.x < 30 and (self.rect.y < 180 or self.rect.y > 300):
            self.speed_x = abs(self.speed_x)
        # collide wall right
        if self.speed_x > 0 and self.rect.x > 700 and (self.rect.y < 180 or self.rect.y > 300):
            self.speed_x = -1 * abs(self.speed_x)
        # collide net left
        if self.rect.x < 15:
            print("GOAL PLAYER 2!")
            player_b.score += 1
            global score_b
            score_b = my_font.render(str(player_b.score), True, "white")
            self.drop_puck()
        # collide net right
        if self.rect.x > 725:
            print("GOAL PLAYER 1!")
            player_a.score += 1
            global score_a
            score_a = my_font.render(str(player_a.score), True, "white")
            self.drop_puck()

        # collide paddles
        d1 = distance(player_a.rect, puck.rect)
        d2 = distance(player_b.rect, puck.rect)

        if d1 < (player_a.radius + puck.radius - 5): # collision!
            vec_dir = [puck.rect.x - player_a.rect.x, puck.rect.y - player_a.rect.y]
            puck.angle = math.atan2(vec_dir[1], vec_dir[0]) * math.pi / 180
            puck.speed_x = puck.speed * math.cos(puck.angle * 180 / math.pi)
            puck.speed_y = puck.speed * math.sin(puck.angle * 180 / math.pi)
        if d2 < (player_b.radius + puck.radius - 5): # collision!
            vec_dir = [puck.rect.x - player_b.rect.x, puck.rect.y - player_b.rect.y]
            puck.angle = math.atan2(vec_dir[1], vec_dir[0]) * math.pi / 180
            puck.speed_x = puck.speed * math.cos(puck.angle * 180 / math.pi)
            puck.speed_y = puck.speed * math.sin(puck.angle * 180 / math.pi)


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Create Game Objects
background = Picture(0,0,800,500,"table.PNG")
foreground = Picture(0,0,800,500,"table_fg.png")
table_shift = 0

player_a = Paddle(100, 200, 35, "paddle.png", pygame.K_w, pygame.K_s)
player_b = Paddle(650, 200, 35, "paddle.png", pygame.K_UP, pygame.K_DOWN)
puck = Puck(385,235,30,"puck.png")


running = True
while running:

    # Process Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                table_shift = 2*(randint(0,1)-0.5)
                puck.speed_x += table_shift
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                table_shift = 0

    # Update Game Objects
    player_a.move()
    player_b.move()
    puck.move()

    # Render Frame
    background.draw(table_shift*3)
    player_a.draw()
    player_b.draw()
    puck.draw()
    foreground.draw(table_shift*3)

    screen.blit(score_a, (10,0))
    screen.blit(score_b, (770,0))

    pygame.display.flip()
    clock.tick(fps)