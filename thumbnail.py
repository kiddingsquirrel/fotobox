from PIL import Image, ImageOps, ImageFont, ImageColor, ImageDraw
class Thumbnail:
    def __init__(self,location,size,fontsize=50,font="Oswald/Oswald-VariableFont_wght.ttf"):
        self.size= size
        self.location = [location[0],location[1]]
        self.img=Image.new(mode="RGBA",size=self.size)   
    def update(self,text,fontsize=50,font="Oswald/Oswald-VariableFont_wght.ttf"):
        font = ImageFont.truetype(font,fontsize)   
        self.draw = ImageDraw.Draw(self.img)
        self.draw.multiline_text((self.size[0]/2,self.size[1]/2),text,anchor="mm",align="center",font=font)
    def save(self,path):
        self.img.save(path)