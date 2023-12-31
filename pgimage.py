import pygame
from PIL import Image, ImageOps, ImageFont, ImageColor, ImageDraw
class Image:
    def __init__(self,path,location,size):
        self.img = pygame.image.load(path)
        self.size= size
        self.location = [location[0],location[1]]
    def update(self,path):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,(self.size[0],self.size[1]))
        print("Updated image to path:" + path)
    def text_to_image(self,text,font="Oswald/Oswald-VariableFont_wght.ttf",fontsize=50):
        self.font= ImageFont.truetype(font,fontsize)
        self.img=Image.new(mode="RGBA",size=self.size)
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(())

        pass