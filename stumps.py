import pygame

class Stumps:
    def __init__(self):
        self.x = 605
        self.y = 180
        self.rect = pygame.Rect(615, 188, 28,85)  # top left x, top left y, width, height
        self.collapse_frames = [
            pygame.transform.scale(pygame.image.load(f"./Images/Stump{i+1}.png"), (70, 100))
            for i in range(6)
        ]
        self.image_index = 0
        self.current_image = self.collapse_frames[int(self.image_index)]
        self.collapse_started = False

    def draw(self, screen):
        if self.collapse_started:
            if self.image_index < 5:
                self.image_index += 0.1
        self.current_image = self.collapse_frames[int(self.image_index)]
        screen.blit(self.current_image, (self.x, self.y))


    def reset(self):
        self.image_index = 0
        self.collapse_started = False
        self.collision = False
