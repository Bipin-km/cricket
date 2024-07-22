import pygame
import random
import math
from player import Batter
from bowler import Bowler
from stumps import Stumps
from wiki import Wiki

class Ball:
    def __init__(self):
        self.x = 640
        self.y = 722
        self.swing_strength = random.uniform(0, 0.5)
        self.direction = random.choice(['straight', 'left', 'right'])
        self.images = [
            pygame.transform.scale(pygame.image.load("./Images/ball.png"), (20, 20)),
            pygame.transform.scale(pygame.image.load("./Images/ball_left.png"), (20, 20)),
            pygame.transform.scale(pygame.image.load("./Images/ball_right.png"), (20, 20))
        ]
        self.target_images = [
            pygame.transform.scale(pygame.image.load("./Images/target4.png"), (40, 40)),
            pygame.transform.scale(pygame.image.load("./Images/target3.png"), (40, 40)),
            pygame.transform.scale(pygame.image.load("./Images/target2.png"), (40, 40)),
            pygame.transform.scale(pygame.image.load("./Images/target1.png"), (40, 40)),
        ]
        self.image_index = 0
        self.target_index = 0
        self.current_image = self.images[self.image_index]
        self.bounce_point = (610, 400)
        self.bounced = False
        self.def_y = 1
        self.movement_distance = 150
        self.movement_distance_checked = False

    def reset_position(self, st: Batter, stump: Stumps, wiki: Wiki):
        self.x = 640
        self.y = 722
        self.bounce_point = self.get_random_bounce_point(st)
        self.bounced = False
        self.image_index = 0
        self.target_index = 0  # Reset target index
        self.swing_strength = random.uniform(0, 0.2)
        self.direction = random.choice(['straight', 'left', 'right'])
        st.hit = False
        st.bat_movement = False
        st.movement_index = 0
        st.input = None
        st.run = 0
        st.rect_to_check = (0, 0, 0, 0)
        self.def_y = 1
        stump.reset()
        wiki.reset()
        self.movement_distance = 150
        self.movement_distance_checked = False
        stump.collapsable = True

    def get_random_bounce_point(self, st: Batter):
        if st.orientation:
            x_min, x_max = 650, 720
            y_min, y_max = 328, 430
        else:
            x_min, x_max = 557, 652
            y_min, y_max = 328, 430
        return (int(random.uniform(x_min, x_max)), int(random.uniform(y_min, y_max)))

    def change_orientation(self, st: Batter):
        self.batter_orientation = st.orientation

    def check_collision_with_bat(self, bat_rect, st: Batter):
        if st.bat_movement and not self.movement_distance_checked:
                self.movement_distance = self.y - st.y
                self.movement_distance_checked = True
        elif st.input == 'a':
            if 250 < self.movement_distance < 350:
                ball_rect = pygame.Rect(self.x, self.y, self.current_image.get_width(), self.current_image.get_height())
                return ball_rect.colliderect(bat_rect)
        elif st.input == 's':
            if self.movement_distance > 250:
                ball_rect = pygame.Rect(self.x, self.y, self.current_image.get_width(), self.current_image.get_height())
                return ball_rect.colliderect(bat_rect)
        return False

    def handle_collision_with_bat(self, batter: Batter):
        if batter.input == 's':
            if self.def_y >10:
                pygame.time.wait(250)
                self.x = 1300
                self.y = 722
            else:
                self.y += self.def_y
                self.def_y += 0.5
        elif batter.input == 'a':
            self.y += 0.5
            if batter.orientation:
                self.x += 1 * batter.batting_power
            else:
                self.x -= 1 * batter.batting_power
        batter.determine_runs()

    def move(self, bowler: Bowler, stump: Stumps, wiki: Wiki):
        speed = bowler.speed
        if not self.bounced:
            dx = self.bounce_point[0] - self.x
            dy = self.bounce_point[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx /= distance
                dy /= distance
            self.x += dx * speed
            self.y += dy * speed
            if self.bounce_point[0] > (wiki.x + 40):
                diff = self.bounce_point[0] - (wiki.x + 45)
                wiki.x += 2 if diff > 2 else 1
            elif self.bounce_point[0] < (wiki.x + 40):
                diff = abs((wiki.x + 45) - self.bounce_point[0])
                wiki.x -= 2 if diff > 2 else 1
            if abs(self.x - self.bounce_point[0]) < speed and abs(self.y - self.bounce_point[1]) < speed:
                self.bounced = True
        else:
            self.y -= speed + 3
            if self.direction == 'left':
                self.x += self.swing_strength
                wiki.x += self.swing_strength
            elif self.direction == 'right':
                self.x -= self.swing_strength
                wiki.x -= self.swing_strength
        self.image_index = (self.image_index + 1) % len(self.images)
        self.current_image = self.images[self.image_index]
        if stump.rect.collidepoint(self.x, self.y):
            stump.collapse_started = True

    def draw(self, screen, ball_thrown):
        screen.blit(self.current_image, (self.x, self.y))
        if ball_thrown and not self.movement_distance_checked:
            target_image = self.target_images[int(self.target_index)]
            screen.blit(target_image, (self.bounce_point[0] - target_image.get_width() // 2, self.bounce_point[1] - target_image.get_height() // 2))
            if self.target_index < 3 and not self.bounced:
                self.target_index += 0.5
