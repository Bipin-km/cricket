import pygame
import random
from player import Batter

class Bowler:
    def __init__(self, name, type,bowling, swing_strength, speed):
        self.bowling_in_progress = False
        self.name = name
        self.type = type
        self.speed = speed
        self.bowling = bowling
        self.swing_strength = swing_strength
        self.runs_conceded = 0
        self.wickets = 0
        self.balls_bowled = 0
        self.count = 0
        self.overs = 0
        self.run = False # True after space bar is pressed to bowl next ball


    def bowl_ball(self):
        self.balls_bowled += 1

    def update_over(self,st1: Batter,st2: Batter, arr):
        if self.balls_bowled %6 == 0:
            st1.change_role()
            st2.change_role()
            self.overs +=1
            return random.choice(arr)
        else:
            return self

    def get_stats(self):
        return f"{self.name} : {self.runs_conceded} - {self.wickets} ({self.overs}.{self.balls_bowled % 6})"


    



    

