import pygame

# A spike class to easily keep track of spikes
class Spike:
    def __init__(self, rect, img, type):
        self.rect = rect
        self.img = img
        self.type = type
pass

def get_frame(img, frame_width, frame_height, frame_number):
    frame = pygame.Surface((frame_width, frame_height))
    frame.set_colorkey((0, 0, 0))
    frame.blit(img, (0, 0),
               (frame_number * frame_width, 0, frame_width, frame_height))
    return frame


pass