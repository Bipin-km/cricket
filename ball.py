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
        self.bounce_point = self.get_random_bounce_point()
        self.bounced = False

    def reset_position(self, st: Batter, stump: Stumps, wiki: Wiki):
        self.x = 640
        self.y = 722
        self.bounce_point = self.get_random_bounce_point()
        self.bounced = False
        self.image_index = 0
        self.target_index = 0  # Reset target index
        self.swing_strength = random.uniform(0, 0.2)
        self.direction = random.choice(['straight', 'left', 'right'])
        st.hit = False
        st.bat_movement = False
        st.movement_index = 0
        st.input = None
        stump.reset()
        wiki.reset()

    def get_random_bounce_point(self):
        x_min, x_max = 500, 660
        y_min, y_max = 328, 470
        return (int(random.uniform(x_min, x_max)), int(random.uniform(y_min, y_max)))

    def change_orientation(self, st: Batter):
        self.batter_orientation = st.orientation
    
    def move(self, bowler: Bowler, stump: Stumps, wiki: Wiki):
        speed = bowler.speed
        if not self.bounced:
            # Calculate direction vector to bounce point
            dx = self.bounce_point[0] - self.x
            dy = self.bounce_point[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx /= distance
                dy /= distance

            # Move ball towards bounce point with consistent speed
            self.x += dx * speed
            self.y += dy * speed

            # Move wiki towards bounce point
            if self.bounce_point[0] > (wiki.x+40):
                diff = self.bounce_point[0] - (wiki.x+45)
                if diff > 2:
                    wiki.x += 2
                else:
                    wiki.x += 1
            elif self.bounce_point[0] < (wiki.x+40):
                diff = abs((wiki.x+45) - self.bounce_point[0])
                if diff >2:
                    wiki.x -= 2
                else:
                    wiki.x -= 1
            # Check if ball reached the bounce point
            if abs(self.x - self.bounce_point[0]) < speed and abs(self.y - self.bounce_point[1]) < speed:
                self.bounced = True  # Ball has reached the bounce point
        else:
            self.y -= speed + 3
            if self.direction == 'left':
                self.x += self.swing_strength  # Change direction after bounce
                wiki.x += self.swing_strength   # Move wiki in the same direction
            elif self.direction == 'right':
                self.x -= self.swing_strength  # Change direction after bounce
                wiki.x -= self.swing_strength  # Move wiki in the same direction
        

        # Update image index for rolling effect
        self.image_index = (self.image_index + 1) % len(self.images)
        self.current_image = self.images[self.image_index]

        if stump.rect.collidepoint(self.x, self.y):
            stump.collapse_started = True

    def draw(self, screen, ball_thrown):
        screen.blit(self.current_image, (self.x, self.y))
        if ball_thrown:
            target_image = self.target_images[int(self.target_index)]
            screen.blit(target_image, (self.bounce_point[0] - target_image.get_width() // 2, self.bounce_point[1] - target_image.get_height() // 2))
            if self.target_index < 3 and not self.bounced:
                self.target_index += 0.5  # Adjust this value for smoother animation
