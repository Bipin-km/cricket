import pygame

class Wiki:
    def __init__(self):
        self.x = 550
        self.y = 25
        self.name = "Wiki"
        self.stances = [pygame.transform.scale(pygame.image.load("./Images/wicket_keeper1.png"),(100,150)),
                        pygame.transform.scale(pygame.image.load("./Images/wicket_keeper2.png"),(100,150))
                        ]
        self.current_index = 0
        self.current_image = self.stances[0]

    def draw(self, screen,ball_thrown):
        if  ball_thrown:
            if self.current_index < 1:
                self.current_index += 0.1
        else:
           self.current_index = 0
        self.current_image = self.stances[round(self.current_index)]
        screen.blit(self.current_image, (self.x, self.y))
        