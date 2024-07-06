import math
import random
import pygame

class Fielder:
    def __init__(self, position):
        self.position = position
        self.speed = random.uniform(2, 5)

    def move_towards(self, target):
        tx, ty = target
        fx, fy = self.position
        angle = math.atan2(ty - fy, tx - fx)
        fx += self.speed * math.cos(angle)
        fy += self.speed * math.sin(angle)
        self.position = (fx, fy)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position[0]), int(self.position[1])), 5)
