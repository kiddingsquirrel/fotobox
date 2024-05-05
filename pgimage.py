import pygame
class Image:
    def __init__(self,path,location,size, visibility=True):
        self.path=path
        self.visibility=visibility
        self.img = pygame.image.load(path)
        self.size= size
        self.img = pygame.transform.scale(self.img,(self.size[0],self.size[1]))
        self.location = [location[0],location[1]]
    def update(self,path):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,(self.size[0],self.size[1]))
        print("Updated image to path:" + path)