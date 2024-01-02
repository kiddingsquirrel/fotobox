import pygame

class Text:
    def __init__(self,text,location,fontsize=16,color="white",font= None):
        self.text=text
        self.location = location
        self.font=font
        self.fontsize = fontsize
        self.fontcolor= pygame.Color(color)
        self.font=pygame.font.Font(self.font,self.fontsize)
        self.txt_surface = self.font.render(self.text,True,self.fontcolor)
    def draw(self,surface):
        # Blit the text
        surface.blit(self.txt_surface,self.location)


