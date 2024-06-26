import pygame
from player import Batter
import random
from players import Team1, Team2

pygame.init()

# variables
spin = random.uniform(1, 3)

# screen
screen = pygame.display.set_mode((800,720))
clock = pygame.time.Clock()
striker_pos = pygame.Vector2(640, 640)
non_striker_pos = pygame.Vector2(640, 640)
pygame.display.set_caption("RETRO_CRICKET")
pygame.display.set_icon(pygame.image.load("./Images/OIG4.jpeg"))


dt = 0
running = True

#background
background = pygame.transform.scale(pygame.image.load("./Images/ground.png"),(800,720))

#player
striker = pygame.transform.scale(pygame.image.load("./Images/batter_neutral.gif"),(90,90))

def draw ():
    screen.blit(background, (0,0))
    screen.blit(striker, (350,85))
    pygame.display.flip()

while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            print(x,y)
    draw()

    clock.tick(60)

pygame.quit()