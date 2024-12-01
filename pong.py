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

class Paddle():
    pass

class Ball():
    pass

# Create Game Objects
background = Picture(0,0,800,500,"table.PNG")

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

    # Render Frame
    background.draw()
    
    pygame.display.flip()
    clock.tick(fps)