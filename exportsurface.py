import pygame
pygame.init()
import pginputbox
current_surface = pygame.Surface((120,30))
screen = pygame.display.set_mode((640,480))
def main():
    print("main")
    clock = pygame.time.Clock()
    input_box1=pginputbox.InputBox((0,0),(200,30),"Zeile 1 - Press Enter to start")
    input_box2=pginputbox.InputBox((0,40),(200,30),"Zeile 2 - Press Enter to starts")
    input_boxes=[input_box1,input_box2]
    done= False
    while not done:
        #print("loop")
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                done=True
            for box in input_boxes:
                box.handle_event(event)
        screen.fill((30,30,30))
        for box in input_boxes:
            box.draw(screen)        
        pygame.display.flip()
        clock.tick(30)
print("start")
main()
pygame.quit()