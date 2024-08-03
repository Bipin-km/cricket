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

pygame.init()

#Game Objects
wiki = Wiki()
stumps = Stumps()
batters = [Batter(player["name"], player["type"], player["orientation"], player["batting_power"], "non-striker") for player in Team1]
bowlers = [Bowler(player["name"], player["type"], player["bowling"], player["swing_strength"], player["speed"]) for player in Team2 if player["bowling"] != "none"]

# Game Variables
batter_1 = batters[0]
batter_2 = batters[1]
batter_1.change_role()
striker, non_striker = batter_1, batter_2
ball = Ball()
current_bowler = random.choice(bowlers)
total_score = total_wickets = total_balls = over_count = 0
current_batter_index  = 2
ball_thrown = False


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (8,7,85)

#fonts
font_small = pygame.font.Font(None, 32)
font_medium = pygame.font.Font(None, 48)
font_large = pygame.font.Font(None, 64)

# screen setup 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("RETRO_CRICKET")
pygame.display.set_icon(pygame.image.load("./Images/OIG4.jpeg"))

# Game States
main_menu = True
overs_menu = False
state_game = False
state_resumed = False
state_paused = False
result_active = False


running = True

#other variables
selected_overs = 0
total_overs = 0
message_text = None
how_to_play_dialog = False

# background
background = pygame.transform.scale(pygame.image.load("./Images/ground.png"), (1280, 720))
field = pygame.transform.scale(pygame.image.load("./Images/field_setup.jpg"), (1280, 720))

#audio
hit_sound = pygame.mixer.Sound("./Audio/cricket_bat_sound.mp3")
stump_hit_sound = pygame.mixer.Sound("./Audio/stump crash.mp3")

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_stats():
    overlay = pygame.Surface((600, 80))
    overlay.set_alpha(200)
    overlay.fill(LIGHT_BLUE)
    screen.blit(overlay, (800, 5))

    draw_text(f"{total_score}/{total_wickets} ({total_balls // 6}.{total_balls % 6})", font_medium, WHITE, 1050, 25)
    draw_text(f"*{striker.get_stats()}  |  {non_striker.get_stats()}", font_small, WHITE, 1030, 50)
    draw_text(current_bowler.get_stats(), font_small, WHITE, 1050, 70)

def draw_button(text, font, color, x, y, width, height, hover_color=LIGHT_BLUE):
    mouse = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect  

def draw_main_menu():
    screen.blit(pygame.transform.scale(pygame.image.load("./Images/menu_bg.jpg"), (1280, 720)), (0, 0))
    draw_text("RETRO CRICKET", font_large, WHITE, SCREEN_WIDTH // 2, 100)
    
def show_how_to_play():
    if how_to_play_dialog:
        dialog = pygame.Surface((600, 300))
        dialog.fill(WHITE)
        screen.blit(dialog, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 100))
        
        draw_text("How to Play", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
        draw_text("Press 'A' for cover drive", font_small, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text("Press 'S' for defense", font_small, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press 'Space' for initiating ball throw", font_small, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    

def draw_pause_menu():
    screen.blit(pygame.transform.scale(pygame.image.load("./Images/ground.jpg"), (1280, 720)), (0, 0))
    
    draw_text("PAUSED", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    

def draw_overs_menu():
    screen.blit(pygame.transform.scale(pygame.image.load("./Images/menu_bg.jpg"), (1280, 720)), (0, 0))
    draw_text("Select Overs", font_large, WHITE, SCREEN_WIDTH // 2, 100)
    

def draw_result():
    # Table settings
    table_width = SCREEN_WIDTH
    batters_table_height = SCREEN_HEIGHT * 0.4
    bowlers_table_height = SCREEN_HEIGHT * 0.4
    row_height = batters_table_height / 12  # 11 rows + 1 header
    col_width = table_width / 4
    
    # Colors
    table_bg_color = (200, 220, 255)  # Light blue
    border_color = (100, 100, 100)  # Dark gray
    
    # Draw batters table
    batters_surface = pygame.Surface((table_width, batters_table_height))
    batters_surface.fill(table_bg_color)
    
    # Draw bowlers table
    bowlers_surface = pygame.Surface((table_width, bowlers_table_height))
    bowlers_surface.fill(table_bg_color)
    
    def draw_table(surface, headers, data, row_count):
        # Draw headers
        for col, header in enumerate(headers):
            pygame.draw.rect(surface, border_color, (col * col_width, 0, col_width, row_height), 1)
            text_surface = font_small.render(header, True, BLACK)
            text_rect = text_surface.get_rect(center=(col * col_width + col_width // 2, row_height // 2))
            surface.blit(text_surface, text_rect)
        
        # Draw data
        for row, item in enumerate(data[:row_count]):
            for col, value in enumerate(item):
                pygame.draw.rect(surface, border_color, (col * col_width, (row + 1) * row_height, col_width, row_height), 1)
                text_surface = font_small.render(str(value), True, BLACK)
                text_rect = text_surface.get_rect(center=(col * col_width + col_width // 2, (row + 1.5) * row_height))
                surface.blit(text_surface, text_rect)
    
    # Batters table
    headers_batters = ["Batter", "Balls Faced", "Runs Scored", "Score Rate"]
    batters_data = [(batter.name, batter.balls_faced, batter.score, 
                     round((batter.score / batter.balls_faced) * 100, 2) if batter.balls_faced > 0 else 0) 
                    for batter in batters]
    draw_table(batters_surface, headers_batters, batters_data, len(batters))
    
    # Bowlers table
    headers_bowlers = ["Bowler", "Overs Bowled", "Runs Conceded", "Economy"]
    bowlers_data = [(bowler.name, 
                     f"{bowler.balls_bowled // 6}.{bowler.balls_bowled % 6}", 
                     bowler.runs_conceded,
                     round(bowler.runs_conceded / (bowler.balls_bowled / 6), 2) if bowler.balls_bowled > 0 else 0)
                    for bowler in bowlers]
    draw_table(bowlers_surface, headers_bowlers, bowlers_data, len(bowlers))
    
    # Blit tables to screen
    screen.blit(batters_surface, (0, 0))
    screen.blit(bowlers_surface, (0, SCREEN_HEIGHT * 0.5))
    
    # Draw total score
    overlay = pygame.Surface((1280, 130))
    overlay.set_alpha(220)
    overlay.fill(DARK_BLUE)
    screen.blit(overlay, (0, 650))
    total_score_text = f"Final Score: {total_score}/{total_wickets} ({total_balls // 6}.{total_balls % 6})"
    draw_text(total_score_text, font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.93)
    


def draw_win_loss_message():
    overlay = pygame.Surface((1280, 70))
    overlay.set_alpha(220)
    overlay.fill(DARK_BLUE)
    screen.blit(overlay, (0, 288))
    runs_per_over = total_score / selected_overs
    font = pygame.font.Font(None, 50)
    if runs_per_over > 10:
        message = f"Congratulations! You Won!"
    else:
        message = f"You Lost!! Better Luck Next Time!"
    draw_text(message,font_large, WHITE, 550, 330)

def reset_game():
    global total_score, total_wickets, total_balls, ball_thrown, ball, current_bowler, batter_1, batter_2, striker, non_striker, result_active, main_menu, overs_menu, state_game, state_paused, how_to_play_dialog
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
    main_menu = True
    overs_menu, state_game, state_paused, how_to_play_dialog, result_active = False, False, False, False, False


while running:
    dt = clock.tick(60) / 1000
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
            x, y = event.pos

    if main_menu:
        selected = draw_main_menu()
        start_button = draw_button("Start Game", font_medium, GRAY, SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        how_to_play_button = draw_button("How to Play", font_medium, GRAY, SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        exit_button = draw_button("Exit", font_medium, GRAY, SCREEN_WIDTH // 2 - 100, 450, 200, 50)

        if mouse_clicked:
            if start_button.collidepoint(x, y):
                overs_menu = True
                main_menu = False
            elif how_to_play_button.collidepoint(x, y):
                how_to_play_dialog = True
            elif exit_button.collidepoint(x, y):
                running = False 
        show_how_to_play()
        if how_to_play_dialog:
            how_to = draw_button("Close", font_small, GRAY, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150, 100, 40)
            if mouse_clicked:
                if how_to.collidepoint(x, y):
                    how_to_play_dialog = False
        pygame.display.flip()
        continue

    elif overs_menu:
        draw_overs_menu()
        overs = [1, 5, 10, 20]
        over_buttons = []
        for i, over in enumerate(overs):
            button = draw_button(f"{over} Overs", font_medium, GRAY, SCREEN_WIDTH // 2 - 100, 250 + i * 75, 200, 50)
            over_buttons.append((button, over))
        
        if mouse_clicked:
            for button, over in over_buttons:
                if button.collidepoint(x,y):
                    selected_overs = over
                    total_overs = selected_overs
                    state_game = True
                    state_resumed = True
                    overs_menu = False
        pygame.display.flip()

    elif state_game:
        if state_paused:
            draw_pause_menu()
            resume_button = draw_button("Resume", font_medium, GRAY, SCREEN_WIDTH // 2 - 100, 500, 200, 100)
            if mouse_clicked:
                if resume_button.collidepoint(x, y):
                    state_paused = False
                    state_resumed = True

        if state_resumed and not result_active:
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
                            result_active = True
                            state_resumed = False
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
                        result_active = True
                        state_resumed = False
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
            pause_button = draw_button("Pause", font_medium, GRAY, 0, 0, 100, 50)
            if mouse_clicked:
                if pause_button.collidepoint(x, y):
                    state_paused = True
                    state_resumed = False
        
        if result_active:
            screen.blit(pygame.transform.scale(pygame.image.load("./Images/ground.jpg"), (1280, 720)), (0, 0))
            draw_result()
            draw_win_loss_message()
            menu_button = draw_button("Main Menu", font_large, GRAY,920, 288, 350, 69)
            if mouse_clicked:
                if menu_button.collidepoint(x, y):
                    reset_game()
        pygame.display.flip()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
