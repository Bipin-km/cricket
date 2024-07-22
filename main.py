import pygame
import ctypes
from player import Batter
from bowler import Bowler
from ball import Ball
from players import Team1, Team2
from stumps import Stumps
from wiki import Wiki
import random

ctypes.windll.user32.SetProcessDPIAware()

wiki = Wiki()
stumps = Stumps()
batters = [Batter(player["name"], player["type"], player["orientation"], player["batting_power"], "non-striker") for player in Team1]
bowlers = [Bowler(player["name"], player["type"], player["bowling"], player["swing_strength"], player["speed"]) for player in Team2 if player["bowling"] != "none"]

batter_1 = batters[0]
batter_2 = batters[1]
batter_1.change_role()
striker = batter_1
non_striker = batter_2

ball = Ball()
total_score = 0
total_wickets = 0
total_balls = 0

pygame.init()

# screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("RETRO_CRICKET")
pygame.display.set_icon(pygame.image.load("./Images/OIG4.jpeg"))

current_bowler = random.choice(bowlers)
over_count = 0
ball_thrown = False
running = True
menu = True
game_active = False
result_active = False
selected_overs = 0
total_overs = 0
message_text = None
current_batter_index  = 2

# background
background = pygame.transform.scale(pygame.image.load("./Images/ground.png"), (1280, 720))
field = pygame.transform.scale(pygame.image.load("./Images/field_setup.jpg"), (1280, 720))

#audio
hit_sound = pygame.mixer.Sound("./Audio/cricket_bat_sound.mp3")
stump_hit_sound = pygame.mixer.Sound("./Audio/stump crash.mp3")

def draw_stats():
    font = pygame.font.Font(None, 30)
    stats_bowler = current_bowler.get_stats()
    batter_1_stats = striker.get_stats()
    batter_2_stats = non_striker.get_stats()

    # Define the position and dimensions of the rectangle
    rect_x, rect_y = 800, 5  # Starting position of the rectangle
    rect_width = 600  # Width of the rectangle
    rect_height = 70  # Height of the rectangle to cover all text lines

    # Draw a blue rectangle
    pygame.draw.rect(screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))

    # Blit the text over the rectangle
    screen.blit(font.render(f"Total Score : {total_score} - {total_wickets} ({total_balls // 6}.{total_balls % 6})", True, (255, 255, 255)), (920, 10))
    screen.blit(font.render(f"*{batter_1_stats}    |    {batter_2_stats}", True, (255, 255, 255)), (810, 30))
    screen.blit(font.render(stats_bowler, True, (255, 255, 255)), (920, 50))
    screen.blit(font.render(stats_bowler, True, (255, 255, 255)), (920, 50))


def draw_menu():
    screen.blit(pygame.transform.scale(pygame.image.load("./Images/menu_bg.jpg"), (1280, 720)), (0, 0))
    font = pygame.font.Font(None, 50)
    title = font.render("Select Overs", True, (255, 255, 255))
    screen.blit(title, (540, 200))
    for i, overs in enumerate([1, 5, 10]):
        text = font.render(f"{overs}", True, (255, 255, 255))
        screen.blit(text, (580, 300 + i * 100))
    pygame.display.flip()

def draw_result(result):
    screen.blit(pygame.transform.scale(pygame.image.load("./Images/ground.jpg"), (1280, 720)), (0, 0))
    font = pygame.font.Font(None, 50)
    message = font.render(result, True, (255, 255, 255))
    screen.blit(message, (450, 360))
    pygame.display.flip()


def draw_win_loss_message():
    runs_per_over = total_score / selected_overs
    font = pygame.font.Font(None, 50)
    if runs_per_over > 10:
        message = font.render(f"Congratulations! You Won!", True, (255, 255, 255))
    else:
        message = font.render(f"You Lost!! \n Better Luck Next Time!", True, (255, 255, 255))
    screen.blit(message, (400, 480))
    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    global total_score, total_wickets, total_balls, ball_thrown, ball, current_bowler, batter_1, batter_2, striker, non_striker, result_active, game_active
    ball.reset_position(striker, stumps, wiki)
    for i in batters:
        i.score = 0
        i.balls_faced = 0
    for i in bowlers:
        i.runs_conceded = 0
        i.balls_bowled = 0
        i.wickets = 0

    total_score = 0
    total_wickets = 0
    total_balls = 0
    total_overs = 0
    ball_thrown = False
    ball = Ball()
    current_bowler = random.choice(bowlers)
    batter_1 = batters[0]
    batter_2 = batters[1]
    batter_1.change_role()
    striker = batter_1
    non_striker = batter_2
    result_active = False
    game_active = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(x, y)
            if menu:
                if 580 < x < 700 and 300 < y < 400:
                    selected_overs = 1
                elif 580 < x < 700 and 400 < y < 500:
                    selected_overs = 10
                elif 580 < x < 700 and 500 < y < 600:
                    selected_overs = 20
                menu = False
                game_active = True
            elif result_active:
                reset_game()

    if game_active:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not ball_thrown:
            ball_thrown = True
            current_bowler.bowling_in_progress = True
        
        if ball_thrown:
            if striker.hit:
                ball.handle_collision_with_bat(striker)
            elif ball.check_collision_with_bat(striker.get_bat_collision_rects(), striker) and not stumps.collapse_started:
                striker.hit = True
                hit_sound.play()
                stumps.collapsable = False
                striker.determine_runs()  # Determine the runs after the hit
            elif ball.y > 110 and not striker.hit:
                ball.move(bowler=current_bowler, stump=stumps, wiki=wiki)
            if ball.y <= 110 or ball.x > 1299 or ball.x < -10:
                if striker.hit:
                    total_score += striker.run
                    striker.score += striker.run
                    current_bowler.runs_conceded += striker.run
                    screen.blit(pygame.font.Font(None, 36).render(f"{striker.run}", True, (0, 0, 255)), (640, 360))
                    pygame.display.flip()
                    if striker.run % 2 != 0:
                        striker.change_role()
                if stumps.collapse_started:
                    stump_hit_sound.play()
                    total_wickets += 1
                    current_bowler.wickets += 1
                    batter_1 = batters[current_batter_index]
                    current_batter_index += 1
                    striker = batter_1
                    screen.blit(pygame.font.Font(None, 36).render(f"OUT", True, (255, 255, 255)), (striker.x - 20, striker.y + 20))
                    pygame.display.flip()
                    if total_wickets == 10:
                        screen.blit(pygame.font.Font(None, 36).render(f"All Out!", True, (255, 255, 255)), (600.460))
                        pygame.time.wait(1000)
                        pygame.display.flip()
                        game_active = False
                        result_active = True
                        ball_thrown = False
                        continue
                pygame.time.wait(1000)

                ball.reset_position(striker, stumps, wiki)
                current_bowler.bowling_in_progress = False
                current_bowler.balls_bowled += 1
                total_balls += 1
                striker.balls_faced += 1

                if total_balls == selected_overs * 6:
                    screen.blit(pygame.font.Font(None, 36).render(f"Overs Finished!", True, (255, 255, 255)), (600, 460))
                    pygame.time.wait(1000)
                    pygame.display.flip()
                    game_active = False
                    result_active = True
                    ball_thrown = False
                    continue
                current_bowler = current_bowler.update_over(batter_1, batter_2, bowlers)
                ball_thrown = False
    
        if batter_1.role == "striker":
            striker = batter_1
            non_striker = batter_2
        else:
            striker = batter_2
            non_striker = batter_1

        screen.blit(background, (0, 0))
        stumps.draw(screen)
        ball.draw(screen, ball_thrown)
        wiki.draw(screen, ball_thrown)
        striker.draw(screen, ball_thrown, keys)

        # Display Stats
        draw_stats()
        


    if result_active and not game_active:
        pygame.time.wait(500)
        pygame.display.flip()
        draw_result(f"Total Score: {total_score} - {total_wickets} ({total_balls // 6}.{total_balls % 6})")
        pygame.time.wait(500)
        pygame.display.flip()
        draw_win_loss_message()
        pygame.time.wait(600)
        pygame.display.flip()
        result_active = False
        reset_game()
        menu = True
    
    if menu:
        draw_menu()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
