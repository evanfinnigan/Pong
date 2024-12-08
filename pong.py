# Pong game by Evan

import pygame
import math
from random import randint

screen = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()
fps = 60

class Picture():
    def __init__(self,x,y,w,h,filename):
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.transform.scale(pygame.image.load(filename), (w,h))
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Paddle(Picture):
    def __init__(self,x,y,radius,filename,k_up,k_down):
        super().__init__(x,y,radius*2,radius*2,filename)
        self.radius = radius
        self.k_up = k_up
        self.k_down = k_down
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
        if self.speed_x < 0 and self.rect.x < 40 and (self.rect.y < 200 or self.rect.y > 300):
            self.speed_x = abs(self.speed_x)
        # collide wall right
        if self.speed_x > 0 and self.rect.x > 700 and (self.rect.y < 200 or self.rect.y > 300):
            self.speed_x = -1 * abs(self.speed_x)
        # collide net left
        if self.rect.x < 5:
            print("GOAL PLAYER 2!")
            self.drop_puck()
        # collide net right
        if self.rect.x > 715:
            print("GOAL PLAYER 1!")
            self.drop_puck()

        # collide paddles

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Create Game Objects
background = Picture(0,0,800,500,"table.PNG")
foreground = Picture(0,0,800,500,"table_fg.png")

player_a = Paddle(100, 200, 40, "paddle.png", pygame.K_w, pygame.K_s)
player_b = Paddle(650, 200, 40, "paddle.png", pygame.K_UP, pygame.K_DOWN)
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
                puck.speed_x += 2*(randint(0,1)-0.5)

    # Update Game Objects
    player_a.move()
    player_b.move()
    puck.move()

    # Render Frame
    background.draw()
    player_a.draw()
    player_b.draw()
    puck.draw()
    foreground.draw()

    pygame.display.flip()
    clock.tick(fps)