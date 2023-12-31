from PIL import Image, ImageOps, ImageFont, ImageColor, ImageDraw

# Image size 4x1 Montage 600x135 pixel
# Image size 2x2 Monate 1725x129 pixel

    
font = ImageFont.truetype("Oswald/Oswald-VariableFont_wght.ttf",50)

thumb_4x1 = Image.new(mode="RGBA",size=(600,135),color="gray")
draw_4x1=ImageDraw.Draw(thumb_4x1)
text="Eillen & Ronny"
font_width,font_heigth =font.getsize(text)
draw_4x1.text(((thumb_4x1.width-font_width)/2,thumb_4x1.height/2-1.1*font_heigth),text,font=font,fill="black")
text="10.10.2023"
font_width,font_heigth =font.getsize(text)
draw_4x1.text(((thumb_4x1.width-font_width)/2,thumb_4x1.height/2),text,font=font,fill="black")
#thumb_4x1.show()


font = ImageFont.truetype("Oswald/Oswald-VariableFont_wght.ttf",50)
thumb_2x2 = Image.new(mode="RGBA",size=(1725,129),color="gray")
draw_2x2=ImageDraw.Draw(thumb_2x2)
font
text="Eillen & Ronny 11.11.2023"
font_width,font_heigth =font.getsize(text)
draw_2x2.text(((thumb_2x2.width-font_width)/2,(thumb_2x2.height-font_heigth)/2),text,font=font,fill="black")
#thumb_2x2.show()

test = Image.new(mode="RGBA",size=(600,129),color="gray")
draw=ImageDraw.Draw(test)
draw.multiline_text((test.width/2,test.height/2),"Guten Morgen",anchor="mm",align="center",font=font)
test.show()