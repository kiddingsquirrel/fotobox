import pygame


class Button:
    def __init__(self, path, location, event, y_align='top', x_align='left'):            
        self.img = pygame.image.load(path)
        self.location = [location[0], location[1]]
        if y_align == 'center':
            self.location[1] = location[1]-self.img.get_size()[1]/2
        if x_align == 'center':
            self.location[0] = location[0]-self.img.get_size()[0]/2
        self.event = event

    def over_button(self, pos):
        if self.location[0] <= pos[0] <= self.location[0]+self.img.get_size()[0]:
            if self.location[1] <= pos[1] <= self.location[1]+self.img.get_size()[1]:
                return True
        return False
