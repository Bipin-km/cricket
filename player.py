import pygame
class Batter:
    def __init__(self,name,type,orientation,batting_power,role):
        self.x = 600
        self.y = 25
        self.playing = False
        self.name = name
        self.score = 0
        self.balls_faced = 0
        self.role = role
        self.bat_movement = False # True if the player has moved the bat for hitting the ball
        self.hit = False # True if the player has hit the ball for collision
        self.batting_power = batting_power
        self.type = type
        self.initial_stance = [pygame.transform.scale(pygame.image.load("./Images/initialstance2.png"),(150,250)),
                               pygame.transform.scale(pygame.image.load("./Images/initialstance1.png"),(150,250))
                               ]
        self.orientation = orientation # 0 for right, 1 for left
        if self.orientation:
            self.initial_stance = [pygame.transform.flip(image, True, False) for image in self.initial_stance]
        
        self.current_index = 0
        self.current_image = self.initial_stance[self.current_index]

    def add_score(self, score):
        self.score += score


    def get_playing(self):
        self.playing = True
    

    def get_name(self):
        return self.name
    
    def get_role(self):
        return self.role

    def get_stats(self):
        return f"{self.name} : {self.score} ({self.balls_faced})"
    
    def change_role(self):
        if self.role == "striker":
            self.role = "non-striker"
        else:
            self.role = "striker"
    
    def increase_score(self,runs):
        self.score += runs
    
    
    def draw(self, screen, ball_thrown):
        if ball_thrown:
            if self.current_index < len(self.initial_stance) - 1:  # Assuming self.images holds the animation frames
                self.current_index += 0.5
        else:
            self.current_index = 0
    
        self.current_image = self.initial_stance[round(self.current_index)]  # Update the current image based on the current index
        screen.blit(self.current_image, (self.x, self.y))


