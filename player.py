import pygame
class Batter:
    def __init__(self,name,type,orientation,batting_power,role):
        self.x = 350
        self.y = 85
        self.playing = False
        self.name = name
        self.score = 0
        self.role = role
        self.hit = False # True if the player has hit the ball
        self.batting_power = batting_power
        self.type = type
        self.neutral_img = pygame.transform.scale(pygame.image.load("./Images/batter_neutral.gif"),(90,90))
        self.orientation = orientation # 0 for right, 1 for left
        if self.orientation:
            self.neutral_image = pygame.transform.flip(self.neutral_img, True, False)
        self.current_image = self.neutral_image

    def add_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def get_playing(self):
        self.playing = True
    
    def hit(self):
        self.hit = True

    def get_name(self):
        return self.name
    
    def get_role(self):
        return self.role
    
    def change_role(self,role):
        self.role = role
    
    def increase_score(self,runs):
        self.score += runs
    
    def move(self, userInput):
        if userInput[pygame.K_a] and self.orientation == 1 and self.role == "striker" and self.x > 340:
            self.x -= 2
        elif userInput[pygame.K_d] and self.orientation == 1 and self.role == "striker" and self.x < 350:
            self.x += 2
        if userInput[pygame.K_d] and self.orientation == 0 and self.role == "striker" and self.x < 360:
                self.x += 2
        elif userInput[pygame.K_a] and self.orientation == 0 and self.role == "striker" and self.x > 350:
            self.x -= 2
    
    def draw(self,screen):
        if self.role == "striker":
            screen.blit(self.current_image, (self.x, self.y))



