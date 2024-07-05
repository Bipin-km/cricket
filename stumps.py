import pygame

class Stumps:
    def __init__(self):
        self.x = 600
        self.y = 80
        self.collapse_frames = [
            pygame.transform.scale(pygame.image.load(f"./Images/Stump{i+1}.png"), (80, 120))
            for i in range(6)
        ]
        self.image_index = 0
        self.current_image = self.collapse_frames[self.image_index]
        self.animation_speed = 10  # Higher is slower
        self.animation_counter = 0
        self.collapse_started = False

    def draw(self, screen):
        screen.blit(self.current_image, (self.x, self.y))

    

    def start_collapse(self):
        self.collapse_started = True
        self.image_index = 0
        self.animation_counter = 0

    def update(self):
        if self.collapse_started:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.image_index += 1
                if self.image_index >= len(self.collapse_frames):
                    self.collapse_started = False
                    self.reset()  # Reset to the first frame automatically
                else:
                    self.current_image = self.collapse_frames[self.image_index]

    def reset(self):
        self.image_index = 0
        self.current_image = self.collapse_frames[self.image_index]
        self.collapse_started = False
