import pygame
import random
class Batter:
    def __init__(self,name,type,orientation,batting_power,role):
        self.x = 570
        self.y = 85
        self.name = name
        self.score = 0
        self.balls_faced = 0
        self.role = role
        self.bat_movement = False # True if the player has moved the bat for hitting the ball
        self.hit = False # True if the player has hit the ball for collision
        self.batting_power = batting_power
        self.type = type
        self.collision_rect = [pygame.Rect(10, 32, 78, 135),
                               pygame.Rect(41,102,117,130)]
        self.defense = [pygame.transform.scale(pygame.image.load("./Images/defence1.png"),(180,250)),
                        pygame.transform.scale(pygame.image.load("./Images/defence2.png"),(180,250)),]
        self.cover_drive = [pygame.transform.scale(pygame.image.load("./Images/coverdrive1.png"),(180,250)),
                            pygame.transform.scale(pygame.image.load("./Images/coverdrive2.png"),(180,250)),
                            pygame.transform.scale(pygame.image.load("./Images/coverdrive3.png"),(180,250)),]       
        self.initial_stance = [pygame.transform.scale(pygame.image.load("./Images/initialstance2.png"),(180,250)),
                               pygame.transform.scale(pygame.image.load("./Images/initialstance1.png"),(180,250))
                               ]
        self.ready_stance = [pygame.transform.scale(pygame.image.load("./Images/triggermoment9.png"),(180,250)),
                             pygame.transform.scale(pygame.image.load("./Images/triggermoment8.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment7.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment6.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment5.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment4.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment3.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment2.png"),(180,250)),
                                pygame.transform.scale(pygame.image.load("./Images/triggermoment1.png"),(180,250)),
                             ]
        self.orientation = orientation # 0 for right, 1 for left
        if self.orientation:
            self.x -= 25
        if self.orientation:
            self.initial_stance = [pygame.transform.flip(image, True, False) for image in self.initial_stance]
            self.ready_stance = [pygame.transform.flip(image, True, False) for image in self.ready_stance]
            self.defense = [pygame.transform.flip(image, True, False) for image in self.defense]
            self.cover_drive = [pygame.transform.flip(image, True, False) for image in self.cover_drive]
            self.collision_rect = [pygame.Rect(180 - rect.x - rect.width - 20, rect.y, rect.width, rect.height) for rect in self.collision_rect]
            self.collision_rect[0][0] += 30
        self.input = None
        self.hit = False
        self.run = 0
        self.current_index = 0
        self.movement_index = 0
        self.current_image = self.initial_stance[self.current_index]
        self.rect_to_check = (0,0,0,0)

    def add_score(self, score):
        self.score += score

    def get_stats(self):
        return f"{self.name} : {self.score} ({self.balls_faced})"
    
    def change_role(self):
        if self.role == "striker":
            self.role = "non-striker"
        else:
            self.role = "striker"
    
    def increase_score(self,runs):
        self.score += runs
    
    def get_bat_collision_rects(self):
        if self.input == 's':
            # Defense collision rect
            self.rect_to_check = self.collision_rect[1].move(self.x, self.y)
        elif self.input == 'a':
            # Cover drive collision rect
            self.rect_to_check = self.collision_rect[0].move(self.x, self.y)
        return self.rect_to_check


    def determine_runs(self):
        if self.input == 's':
            self.run = 0  # Defensive shots usually result in lower runs
        elif self.input == 'a':
            self.run = random.choice([1,2,4,6])  # Cover drive usually results in boundaries

    def draw(self, screen, ball_thrown,userInput):
        if (userInput[pygame.K_a] or userInput[pygame.K_s]) and ball_thrown and not self.bat_movement:
            self.bat_movement = True
            self.input = 'a' if userInput[pygame.K_a] else 's'
        
        if self.bat_movement:
            if self.input == 's':
                if self.movement_index < 1:
                    self.movement_index += 0.1
                self.current_image = self.defense[int(self.movement_index)]
            else :
                if self.movement_index < 2:
                    self.movement_index += 0.1
                self.current_image = self.cover_drive[int(self.movement_index)]

        
        elif ball_thrown and not self.bat_movement:
            if self.current_index < len(self.ready_stance) - 1:  # Assuming self.images holds the animation frames
                self.current_index += 0.5
            self.current_image = self.ready_stance[int(self.current_index)]
        else:
            if self.current_index > 1:
                self.current_index = 0
            self.current_image = self.initial_stance[round(self.current_index)]
        screen.blit(self.current_image, (self.x, self.y))


