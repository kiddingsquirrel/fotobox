#! booth-env/bin/python3

import pygame
import cevent
import pgwindow
import pgbutton
import pgimage
import PhotoBooth
import time
import os

working_dictonary= "/home/fotobox/github/fotobox" #Dictonary in which all files are located(images and other classes)
class App(cevent.CEvent):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 1024
        self._start_window = pgwindow.Window(self.size)
        self._capture_window = pgwindow.Window(self.size)
        self._print_window = pgwindow.Window(self.size)
        self._settings_window = pgwindow.Window(self.size)
        self._current_window = self._start_window
        self.booth = None
        self.last_montage_path = "temps/collage.jpg"
        self.booth = PhotoBooth.PhotoBooth()
        
        self.settings = {"printing":True, "usb":True, "FULLSCREEN":True}  # all settings should reside in this dict

    def on_init(self):
        os.chdir(working_dictonary)
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)  # pygame.RESIZABLE FULLSCREEN | 
        self._running = True
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))  # setting a invisible cursor
        #
        # Adding button to Start Screen
        #
        self._start_window.add_button(pgbutton.Button("Images/Start_Button.png",
                                                      (self.size[0]/2, self.size[1]/2),
                                                      self.set_capture,
                                                      y_align='center', x_align='center'), 
                                                      "start")
        self._start_window.add_button(pgbutton.Button("Images/settings/OpenSet.png",
                                                      (0, 0),
                                                      self.open_settings),
                                                      "settings")
        #s
        # Adding button to Print Screen
        #
        rely = 45
        self._print_window.add_image(pgimage.Image(self.last_montage_path,(140,55),(1000,667)),"Montage")
        self._print_window.add_button(pgbutton.Button("Images/Print_b1.png",
                                                      (667,785), self.printone,),
                                                      "print once")
        #self._print_window.add_button(pgbutton.Button("Images/Print_b2.png",
        #                                              (1045,592), self.printtwo,
        #                                              y_align='center', x_align='center'),
        #                                              "print twice")
        self._print_window.add_button(pgbutton.Button("Images/Print_bWeiter.png",
                                                      (140,785),
                                                      self.set_start),
                                                      "weiter")
        
        #
        # Adding buttons to Settings 
        self._settings_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (300, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "back")
        self._settings_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (660, 30),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        self._settings_window.add_button(pgbutton.Button("Images/settings/USB.png",
                                                         (300,180),  # (x, y) position
                                                         self.change_usb), #
                                                         "usb")
        self._settings_window.add_button(pgbutton.Button("Images/settings/preview.png",
                                                         (660, 180),  # (x, y) position
                                                         self.cam_preview), 
                                                         "preview")  
        self._settings_window.add_button(pgbutton.Button("Images/settings/restart.png",
                                                         (300, 320),  # (x, y) position
                                                         self.printer_restart), 
                                                         "restart")
        self._settings_window.add_button(pgbutton.Button("Images/settings/style_1.png",
                                                         (90, 580),  # (x, y) position
                                                         self.style_1), 
                                                         "style_1")
        self._settings_window.add_button(pgbutton.Button("Images/settings/style_2_active.png",
                                                         (500, 580),  # (x, y) position
                                                         self.style_2), 
                                                         "style_2")
        self._settings_window.add_button(pgbutton.Button("Images/settings/style_3.png",
                                                         (900, 580),  # (x, y) position
                                                         self.style_3), 
                                                         "style_3")
        

    # def on_event(self, event):
    #     if event.type == pygame.QUIT:
    #         self._running = False
   
    def printone(self):
        self.set_start()
        self.booth.print_montage("temps/collage.jpg")

    def printtwo(self):
        self.set_start()
        self.booth.print_file("temps/collage.jpg")
        self.booth.print_file("temps/collage.jpg")
    def printer_restart(self):
        self.booth.printer_restart()
        self._current_window = self._start_window
    def style_1(self):
        self.booth.style_set(1)
        self._settings_window.buttons["style_1"] = pgbutton.Button("Images/settings/style_1_active.png",
                                                         (90, 580),  # (x, y) position
                                                         self.style_1)
        self._settings_window.buttons["style_2"] = pgbutton.Button("Images/settings/style_2.png",
                                                         (500, 580),  # (x, y) position
                                                         self.style_2)
        self._settings_window.buttons["style_3"] = pgbutton.Button("Images/settings/style_3.png",
                                                         (900, 580),  # (x, y) position
                                                         self.style_3)
        self._print_window.images["Montage"]=pgimage.Image(self.last_montage_path,(140,55),(1000,667))
        self._current_window = self._settings_window
    def style_2(self):
        self.booth.style_set(2)
        self._settings_window.buttons["style_1"] = pgbutton.Button("Images/settings/style_1.png",
                                                         (90, 580),  # (x, y) position
                                                         self.style_1)
        self._settings_window.buttons["style_2"] = pgbutton.Button("Images/settings/style_2_active.png",
                                                         (500, 580),  # (x, y) position
                                                         self.style_2)
        self._settings_window.buttons["style_3"] = pgbutton.Button("Images/settings/style_3.png",
                                                         (900, 580),  # (x, y) position
                                                         self.style_3)
        self._print_window.images["Montage"]=pgimage.Image(self.last_montage_path,(140,55),(1000,667))
        self._current_window = self._settings_window
    def style_3(self):
        self.booth.style_set(3)
        self._settings_window.buttons["style_1"] = pgbutton.Button("Images/settings/style_1.png",
                                                         (90, 580),  # (x, y) position
                                                         self.style_1)
        self._settings_window.buttons["style_2"] = pgbutton.Button("Images/settings/style_2.png",
                                                         (500, 580),  # (x, y) position
                                                         self.style_2)
        self._settings_window.buttons["style_3"] = pgbutton.Button("Images/settings/style_3_active.png",
                                                         (900, 580),  # (x, y) position
                                                         self.style_3)
        self._print_window.images["Montage"]=pgimage.Image(self.last_montage_path,(540,55),(222,667))
        self._current_window = self._settings_window
    def change_usb(self):
        oldb = self._settings_window.buttons["usb"]
        if self.settings["usb"]:
            self.settings["usb"] = False
            self._settings_window.buttons["usb"] = pgbutton.Button("Images/settings/Desktop.png",
                                                         oldb.location,  # (x, y) position
                                                         self.change_usb)
            self.booth.save_path = "/home/pi/Desktop/Pics/"
        else:
            self.settings["usb"] = True
            self._settings_window.buttons["usb"] = pgbutton.Button("Images/settings/USB.png",
                                                         oldb.location,  # (x, y) position
                                                         self.change_usb)
            usb_name = os.listdir("/media/pi/")[1]
            try:
                os.mkdir("/media/pi/{}/Pics".format(usb_name))
                self.booth.save_path = "/media/pi/{}/Pics/".format(usb_name)
            except OSError:
                self.booth.save_path = "/media/pi/{}/Pics/".format(usb_name)
                None
        self._current_window = self._start_window
    
    def cam_preview(self):
        self.booth.cam_preview()
        self._current_window = self._settings_window
    def change_printing(self):
        oldb = self._settings_window.buttons["printing"]
        
        if self.settings["printing"]:
            self.settings["printing"] = False
            self._settings_window.buttons["printing"] = pgbutton.Button("Images/settings/PrintingOn.png",
                                                         oldb.location,  # (x, y) position
                                                         self.change_usb)
        else:
            self.settings["printing"] = True
            self._settings_window.buttons["printing"] = pgbutton.Button("Images/settings/PrintingOff.png",
                                                         oldb.location,  # (x, y) position
                                                         self.change_usb)
        self._current_window = self._start_window

    
    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))  # clear all img
        for image in self._current_window.images.values():
            self._display_surf.blit(image.img, image.location)        
        for button in self._current_window.buttons.values():
            self._display_surf.blit(button.img, button.location)

        pygame.display.flip()
    def on_exit(self):
        self._running = False    
    def on_cleanup(self):
        pygame.quit()
        self.on_exit()

    def execute(self):
        self.on_init()
        if __name__ == '__main__':
            while self._running:
                for event in pygame.event.get():
                    self.on_event(event)
                    self.on_loop()
                    self.on_render()
            self.on_cleanup()



    def set_print(self):
        self._current_window = self._print_window

    def set_capture(self):
        self._current_window = self._capture_window
        self.on_render()
        self.booth.capture()
        self.last_pic_path = self.booth.make_collage()
        self._print_window.images["Montage"].update(self.last_pic_path)
        if self.settings["printing"]:
            self._current_window = self._print_window
            print(self.last_pic_path)
        else:
            self._current_window = self._start_window

    def set_start(self):
        self._current_window = self._start_window
    
    def open_settings(self):
        self._current_window = self._settings_window
        self.on_render()



if __name__ == "__main__":
    theApp = App()
    theApp.execute()
