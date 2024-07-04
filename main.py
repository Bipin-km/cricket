import pygame
import ctypes
from player import Batter
from bowler import Bowler
from ball import Ball
from players import Team1, Team2

ctypes.windll.user32.SetProcessDPIAware()

batters = [Batter(player["name"], player["type"], player["orientation"], player["batting_power"],"non-striker") for player in Team1]
bowlers = [Bowler(player["name"], player["type"], player["bowling"], player["swing_strength"]) for player in Team2 if player["bowling"] != "none"]

batter_1 = batters[0]
batter_2 = batters[1]
batter_1.change_role()
striker = batter_1

ball = Ball()


pygame.init()


# screen
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("RETRO_CRICKET")
pygame.display.set_icon(pygame.image.load("./Images/OIG4.jpeg"))

current_bowler_index = 0
current_bowler = bowlers[current_bowler_index]
over_count = 0
ball_thrown = False
running = True

#background
background = pygame.transform.scale(pygame.image.load("./Images/ground.jpg"),(1280,720))


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
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not ball_thrown:
        ball_thrown = True
        current_bowler.bowling_in_progress = True
    
    if ball_thrown:
        if ball.y > 150:
            ball.move()
        else:
            ball.reset_position()
            current_bowler.bowling_in_progress = False
            current_bowler.balls_bowled += 1
            striker.balls_faced += 1
            current_bowler.update_over()
            ball_thrown = False

    

    screen.blit(background, (0,0))
    ball.draw(screen)
    striker.draw(screen, ball_thrown)

    #Display Stats
    font = pygame.font.Font(None, 24)
    stats_bowler = current_bowler.get_stats()
    batter_1_stats = batter_1.get_stats()
    batter_2_stats = batter_2.get_stats()
    screen.blit(font.render(batter_1_stats, True, (255,255,255)), (950, 10))
    screen.blit(font.render(batter_2_stats, True, (255,255,255)), (950, 30))
    screen.blit(font.render(stats_bowler, True, (255,255,255)), (950, 50))
    pygame.display.flip()


    clock.tick(60)

pygame.quit()