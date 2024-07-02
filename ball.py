import pygame
import random
from player import Batter

class Ball:
    def __init__(self):
        self.reset_position()
        self.speed = 5
        # self.swing = random.choice(['in', 'out'])
        self.batter_orientaion = "right"
        self.swing_strength = random.uniform(0, 0.5)
        self.direction = random.choice(['straight', 'left', 'right'])
        self.images = [ pygame.transform.scale(pygame.image.load("./Images/ball.png"), (20, 20)),pygame.transform.scale(pygame.image.load("./Images/ball_left.png"), (20, 20)),pygame.transform.scale(pygame.image.load("./Images/ball_right.png"), (20, 20))
        ]
        self.image_index = 0
        self.current_image = self.images[self.image_index]
        self.bounced = False
    
    def reset_position(self):
        self.x = 640
        self.y = 722
        self.bounce_point = self.get_random_bounce_point()
        self.bounced = False
        self.image_index = 0
        self.swing_strength = random.uniform(0, 0.5)
        self.direction = random.choice(['straight', 'left', 'right'])

    def get_random_bounce_point(self):
        # if self.batter_orientation == 'right':
        x_min, x_max = 480, 580
        y_min, y_max = 325, 430
        # else:
        #     x_min, x_max = 700, 805
        #     y_min, y_max = 325, 430
        return (random.uniform(x_min, x_max), random.uniform(y_min, y_max))

    def change_orientation(self, st: Batter):
        self.batter_orientation = st.orientation
    
    def move(self):
        if not self.bounced:
            if self.y > self.bounce_point[1]:
                self.y -= self.speed
                if self.direction == 'left':
                    self.x -= self.speed * self.swing_strength
                elif self.direction == 'right':
                    self.x += self.speed * self.swing_strength
            else:
                self.bounced = True  # Ball has reached the bounce point
        else:
            self.y -= self.speed
            if self.direction == 'left':
                self.x += self.speed * self.swing_strength  # Change direction after bounce
            elif self.direction == 'right':
                self.x -= self.speed * self.swing_strength  # Change direction after bounce

        # Reset ball position if it goes off screen
        if self.y < 150:
            self.reset_position()
        
        # Update image index for rolling effect
        self.image_index = (self.image_index + 1) % len(self.images)
        self.current_image = self.images[self.image_index]

    def draw(self, screen):
        screen.blit(self.current_image, (self.x, self.y))
