# Pong game by Evan

import pygame

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
        self.speed_x = 0
        self.speed_y = 0
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Create Game Objects
background = Picture(0,0,800,500,"table.PNG")
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

    # Update Game Objects
    player_a.move()
    player_b.move()
    puck.move()

    # Render Frame
    background.draw()
    player_a.draw()
    player_b.draw()
    puck.draw()

    pygame.display.flip()
    clock.tick(fps)