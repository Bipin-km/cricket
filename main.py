import pygame
import ctypes
from player import Batter
from bowler import Bowler
from ball import Ball
import random
from players import Team1, Team2

ctypes.windll.user32.SetProcessDPIAware()

# batters = [Batter(player["name"], player["type"], player["orientation"], player["batting_power"],"non-striker") for player in Team2]
bowlers = [Bowler(player["name"], player["type"], player["bowling"], player["swing_strength"]) for player in Team1 if player["bowling"] != "none"]

ball = Ball()

pygame.init()


# screen
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
striker_pos = pygame.Vector2(640, 640)
non_striker_pos = pygame.Vector2(640, 640)
pygame.display.set_caption("RETRO_CRICKET")
pygame.display.set_icon(pygame.image.load("./Images/OIG4.jpeg"))

current_bowler_index = 0
current_bowler = bowlers[current_bowler_index]
running = True

#background
background = pygame.transform.scale(pygame.image.load("./Images/ground.jpg"),(1280,720))

#player
# striker = pygame.transform.scale(pygame.image.load("./Images/batter_neutral.png"),(90,90))

# def draw ():
#     screen.blit(background, (0,0))
#     screen.blit(striker, (350,85))
#     pygame.display.flip()

while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            print(x,y)
        elif event.type == pygame.KEYDOWN:
            if event.key== pygame.K_SPACE:
                ball = current_bowler.bowl_ball(ball)
                current_bowler.update_over()
                if current_bowler.balls_bowled %6 == 0:
                    current_bowler_index += 1
                    current_bowler = bowlers[current_bowler_index % len(bowlers)]

    ball.move()
    screen.blit(background, (0,0))
    ball.draw(screen)

    #Display Stats
    font = pygame.font.Font(None, 36)
    stats = current_bowler.get_stats()
    y_pos = 10
    for stat in stats:
        text = font.render(stat, True, (255,255,255))
        screen.blit(text, (1000, y_pos))
        y_pos += 20
    y_pos = 10
    pygame.display.flip()


    clock.tick(60)

pygame.quit()