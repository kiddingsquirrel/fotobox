import pygame
#pygame.init()
#screen = pygame.display.set_mode((640,480))
class InputBox:
    def __init__(self,location,size,text,
                 COLOR_INACTIVE=pygame.Color('lightskyblue3'),
                 COLOR_ACTIVE=pygame.Color('dodgerblue2'),
                 FONT= pygame.font.Font(None,16)):
        self.location=location
        self.size=size
        self.rect=pygame.Rect(location[0],location[1],size[0],size[1])
        self.COLOR_INACTIVE=COLOR_INACTIVE
        self.COLOR_ACTIVE=COLOR_ACTIVE
        self.FONT=FONT
        self.color=self.COLOR_INACTIVE
        self.text=text
        self.txt_surface = self.FONT.render(text,True,self.color)
        self.active=False
    def over_box(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
    def status(self,status):
        print("Change status of", self.text)
        print(" to",status)

        self.active= status
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
    def input_text(self,event):
        # print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # print(self.text)
                self.text= ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = self.FONT.render(self.text,True,self.color)
    def draw(self,screen):
        # Blit the text
        screen.blit(self.txt_surface,(self.rect.x+5,self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(screen,self.color,self.rect,2)
    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(even.pos):
                self.active= not self.active
            else:
                self.active=False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type ==  pygame.KEYDOWN:
            if self.active:
                if event.key== pygame.K_RETURN:
                    print(self.text)
                    self.text=""
                elif event.key == pygame.K_BACKSPACE:
                    self.text= self.text[:-1]
                else:
                    self.text += event.unicode
            # rerender text
            self.txt_surface =  self.FONT.render(self.text,True,self.color)            




#def main():
#    print("main")
#    clock = pygame.time.Clock()
#    input_box1=InputBox((0,0),(200,30),"Zeile 1 - Press Enter to start")
#   input_box2=InputBox((0,40),(200,30),"Zeile 2 - Press Enter to starts")
#    input_boxes=[input_box1,input_box2]
#    done= False
#    while not done:
#        #print("loop")
#        for event in pygame.event.get():
#            if event.type== pygame.QUIT:
#                done=True
#            for box in input_boxes:
#                box.handle_event(event)
#        screen.fill((30,30,30))
#        for box in input_boxes:
#            box.draw(screen)        
#        pygame.display.flip()
#        clock.tick(30)
#print("start")
#main()
#pygame.quit()