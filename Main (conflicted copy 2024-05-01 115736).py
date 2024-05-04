#! booth-env/bin/python3
# Importing Standard Libaries 
import platform
import psutil
import time
import os
import subprocess
import time
import pygame
# Importing custom libaries 
import cevent
import pgwindow
import pgbutton
import pgimage
pygame.init() # Necessary to use font libary in class pginputbox
import pginputbox # pygame.init() has to be before import pginputbox !!!!
import pgtext
import PhotoBooth_Dev_Wind



working_dictonary= r"C:\Users\Jonathan\NextCloud_hosted_by_Esra\Maker_Stuff\FotoBox\Local_GitRepo\fotobox" #Dictonary in which all files are located(images and other classes)
class App(cevent.CEvent):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 1024
        # Initialize Screens - Basic Functionality
        self._start_window = pgwindow.Window(self.size)
        self._capture_window = pgwindow.Window(self.size)
        self._after_capture_QR_window = pgwindow.Window(self.size)
        self._after_capture_print_window = pgwindow.Window(self.size)
        self._after_capture_print_QR_window = pgwindow.Window(self.size)
        self._printing_window = pgwindow.Window(self.size)
        self._QR_window = pgwindow.Window(self.size)
        self._printing_QR_window = pgwindow.Window(self.size)
        # Initialize Screens - Handling Erros - but Insure User - Images are Saved
        self._QR_failed_window = pgwindow.Window(self.size)
        self._printing_failed_window = pgwindow.Window(self.size)
        # Optimizing User Experience 
        self._settings_window = pgwindow.Window(self.size)
        self._style1_window = pgwindow.Window(self.size)
        self._style2_window = pgwindow.Window(self.size)
        self._style3_window = pgwindow.Window(self.size)
        # Initializing Start Situation 
        self._current_window = self._start_window
        self.booth = PhotoBooth_Dev_Wind.PhotoBooth(working_dictonary)
        self.NextCloudClient = PhotoBooth_Dev_Wind.NextCloudClient(working_dictonary,"Test","https://nc-8872520695452827614.nextcloud-ionos.com/","boxjoni","FUUhJw0NTnXw")
        self.last_montage_path = "temps/collage.jpg"
        self.last_QR_path ="temps/QR.jpg"
        self.settings = {"printing":True, "Upload":True, "usb":True, "FULLSCREEN": False}  # all settings should reside in this dict

    def on_init(self):
        os.chdir(working_dictonary)
        pygame.init()
        if self.settings["FULLSCREEN"]==True:
            self._display_surf = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)  # pygame.RESIZABLE FULLSCREEN |
        elif self.settings["FULLSCREEN"]==False:
            self._display_surf = pygame.display.set_mode(self.size, pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)  # pygame.RESIZABLE FULLSCREEN
        else:
            print("Error Setting Screen-Settings")
        self._running = True
        # pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))  # setting a invisible cursor
        #
        # Start Screen - Adding buttons
        self._start_window.add_button(pgbutton.Button("Images/Take_Pictures.png",
                                                      (self.size[0]/2, self.size[1]/2),
                                                      self.set_capture,
                                                      y_align='center', x_align='center'), 
                                                      "start")
        self._start_window.add_button(pgbutton.Button("Images/settings/OpenSet.png",
                                                      (0, 0),
                                                      self.open_settings),
                                                      "settings")
        #self._settings_window.add_text(pgtext.Text("Wechsel bitte die Papierrolle und Toner, wenn nur noch {} Bilder gedruckt werden können".format(40),(0,60),28),"Anweisung1")
        #### HIER WEITER ARBEITEN 
        # After Capture Screens - Adding buttons
        ## Printing
        self._after_capture_print_window.add_image(pgimage.Image(self.last_montage_path,(140,55),(1000,667)),"Montage")
        self._after_capture_print_window.add_button(pgbutton.Button("Images/Print_bWeiter.png",
                                                      (140,785),
                                                      self.set_start),
                                                      "weiter")
        self._after_capture_print_window.add_button(pgbutton.Button("Images/Print_b1.png",
                                                      (667,785), self.printone,),
                                                      "print once")
              
        # After Capture QR Screen 
        self._after_capture_QR_window.add_image(pgimage.Image(self.last_montage_path,
                                                              (140,30),
                                                              (1000,667)),
                                                              "Montage")
        self._after_capture_QR_window.add_image(pgimage.Image("Images/Qr_explain.png",
                                                (140,755),
                                                (645,100)),
                                                "Text")
        self._after_capture_QR_window.add_image(pgimage.Image(self.NextCloudClient.current_qr_path,
                                                                    (890,745),
                                                                    (250,250)),
                                                                    "QR")
        self._after_capture_QR_window.add_button(pgbutton.Button("Images/Qr_weiter.png",
                                                      (140,875),
                                                      self.set_start),
                                                      "weiter")
        #  After Capture Printing QR - Screen
        self._after_capture_print_QR_window.add_image(pgimage.Image(self.last_montage_path,
                                                                    (140,55),
                                                                    (1000,667)),
                                                                    "Montage")
        self._after_capture_print_QR_window.add_image(pgimage.Image("Images/Print_Qr_explain.png",
                                                                    (140,750),
                                                                    (650,88)),
                                                                    "Text")
        self._after_capture_print_QR_window.add_image(pgimage.Image(self.NextCloudClient.current_qr_path,
                                                                    (890,745),
                                                                    (250,250)),
                                                                    "QR")
        self._after_capture_print_QR_window.add_button(pgbutton.Button("Images/Print_Qr_bWeiter.png",
                                                      (140,875),
                                                      self.set_start),
                                                      "weiter")
        self._after_capture_print_QR_window.add_button(pgbutton.Button("Images/Print_Qr_b1.png",
                                                      (516,875), self.printone,),
                                                      "print once")
        

        # Printing Screen 
        self._printing_window.add_image(pgimage.Image("Images/Printing.png",
                                                      (400,318),
                                                      (479,326)),
                                                      "Printing")
        # Settings - Adding buttons
        ## Mange Screen 
        self._settings_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (300, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "back")
        self._settings_window.add_button(pgbutton.Button("Images/settings/ShutDown.png",
                                                         (660, 30),  # (x, y) position
                                                         self.shut_down),
                                                         "shutdown")
        ## Manage Camera and Printer
        self._settings_window.add_button(pgbutton.Button("Images/settings/Camera_Preview.png",
                                                         (300, 180),  # (x, y) position
                                                         self.cam_preview), 
                                                         "preview")  
        
        ## Manage USB
        self._settings_window.add_text(pgtext.Text("Speicherort der Aufnahmen ist:",
                                                   (300,310),36),
                                                   "Speicherort")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Save_Desktop.png",
                                                         (300,370),  # (x, y) position
                                                         lambda: self.save_to_usb(False)), #
                                                         "Save Desktop")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Save_USB_active.png",
                                                         (660,370),  # (x, y) position
                                                         lambda: self.save_to_usb(True)), #
                                                         "Save USB")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Set_Layout.png",
                                                         (300, 500),  # (x, y) position
                                                         self.open_style_1_window),
                                                         "Weiter thumbnail")
        self._settings_window.add_button(pgbutton.Button("Images/settings/restart.png",
                                                         (300, 780),  # (x, y) position
                                                         self.printer_restart), 
                                                         "printer restart")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Reset_Counter.png",
                                                         (660, 780),  # (x, y) position
                                                         self.printer_reset_counter), 
                                                         "printer reset counter")
        
        
        # Style1 Screen - Adding Buttond and InputTextboxes
        self._style1_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (90, 30),  # (x, y) position
                                                         self.open_settings), # anchor
                                                         "back")
        self._style1_window.add_button(pgbutton.Button("Images/style/Back_Foto.png",
                                                         (500, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "Set Start")
        self._style1_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (900, 30),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        self._style1_window.add_image(pgimage.Image("Images/style/Drucklayout.png",
                                                        (560,160),
                                                        (156,36)),
                                                        "Drucklayout")
        self._style1_window.add_button(pgbutton.Button("Images/style/style_1_active.png",
                                                         (90, 205),  # (x, y) position
                                                         self.open_style_1_window), 
                                                         "style_1")
        self._style1_window.add_button(pgbutton.Button("Images/style/style_2.png",
                                                         (500, 205),  # (x, y) position
                                                         self.open_style_2_window), 
                                                         "style_2")
        self._style1_window.add_button(pgbutton.Button("Images/style/style_3.png",
                                                         (900, 205),  # (x, y) position
                                                         self.open_style_3_window), 
                                                         "style_3")
        self._style1_window.add_image(pgimage.Image("Images/style/Thumbnaildesign.png",
                                                        (525,615),
                                                        (220,38)),
                                                        "Thumbnaildesign")
        self._style1_window.add_image(pgimage.Image(self.booth.thumb_2x2_path,(205,660),(870,68)),"thumbnail")
        self._style1_window.add_inputbox(pginputbox.InputBox((205,840),(380,50),"",self.create_thumb_from_input),'Zeile 1')
        self._style1_window.add_inputbox(pginputbox.InputBox((205,910),(380,50),"",self.create_thumb_from_input),'Zeile 2')
        self._style1_window.add_image(pgimage.Image("Images/style/Zeile1.png",
                                                    (90,840),
                                                    (95,35)),
                                                    "Text Zeile 1")
        self._style1_window.add_image(pgimage.Image("Images/style/Zeile2.png",
                                                    (90,910),
                                                    (95,35)),
                                                    "Text Zeile 2")
        ## Font Management 
                            
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Up.png",
                                                       (650, 840),  # (x, y) position
                                                       self.set_font_up), 
                                                       "Font Up")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Down.png",
                                                         (650, 910),  # (x, y) position
                                                         self.set_font_down), 
                                                         "Font Down")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Oswald_active.png",
                                                         (740, 840),  # (x, y) position
                                                         lambda: self.set_font("Oswald")), 
                                                         "Oswald")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Bentham.png",
                                                         (920, 840),  # (x, y) position
                                                         lambda: self.set_font("Bentham")), 
                                                         "Bentham")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Flaemisch.png",
                                                         (1100, 840),  # (x, y) position
                                                         lambda: self.set_font("Flaemisch")), 
                                                         "Flaemisch")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Lora.png",
                                                         (740, 910),  # (x, y) position
                                                         lambda: self.set_font("Lora")), 
                                                         "Lora")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Linux.png",
                                                         (920, 910),  # (x, y) position
                                                         lambda: self.set_font("Linux")), 
                                                         "Linux")
        self._style1_window.add_button(pgbutton.Button("Images/style/Font_Great.png",
                                                         (1100, 910),  # (x, y) position
                                                         lambda: self.set_font("Great")), 
                                                         "Great")                                                         
               
        
        # Style2 Screen - Adding Buttond and InputTextboxes
        self._style2_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (90, 30),  # (x, y) position
                                                         self.open_settings), # anchor
                                                         "back")
        self._style2_window.add_button(pgbutton.Button("Images/style/Back_Foto.png",
                                                         (500, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "Set Start")
        self._style2_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (900, 30),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        self._style2_window.add_image(pgimage.Image("Images/style/Drucklayout.png",
                                                        (560,160),
                                                        (156,36)),
                                                        "Drucklayout")
        self._style2_window.add_button(pgbutton.Button("Images/style/style_1.png",
                                                         (90, 205),  # (x, y) position
                                                         self.open_style_1_window), 
                                                         "style_1")
        self._style2_window.add_button(pgbutton.Button("Images/style/style_2_active.png",
                                                         (500, 205),  # (x, y) position
                                                         self.open_style_2_window), 
                                                         "style_2")
        self._style2_window.add_button(pgbutton.Button("Images/style/style_3.png",
                                                         (900, 205),  # (x, y) position
                                                         self.open_style_3_window), 
                                                         "style_3")   
        # Style1 Screen - Adding Buttond and InputTextboxes
        self._style3_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (90, 30),  # (x, y) position
                                                         self.open_settings), # anchor
                                                         "back")
        self._style3_window.add_button(pgbutton.Button("Images/style/Back_Foto.png",
                                                         (500, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "Set Start")
        self._style3_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (900, 30),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        self._style3_window.add_image(pgimage.Image("Images/style/Drucklayout.png",
                                                        (560,160),
                                                        (156,36)),
                                                        "Drucklayout")
        self._style3_window.add_button(pgbutton.Button("Images/style/style_1.png",
                                                         (90, 205),  # (x, y) position
                                                         self.open_style_1_window), 
                                                         "style_1")
        self._style3_window.add_button(pgbutton.Button("Images/style/style_2.png",
                                                         (500, 205),  # (x, y) position
                                                         self.open_style_2_window), 
                                                         "style_2")
        self._style3_window.add_button(pgbutton.Button("Images/style/style_3_active.png",
                                                         (900, 205),  # (x, y) position
                                                         self.open_style_3_window), 
                                                         "style_3")
        self._style3_window.add_image(pgimage.Image("Images/style/Thumbnaildesign.png",
                                                        (525,615),
                                                        (220,38)),
                                                        "Thumbnaildesign")
        self._style3_window.add_image(pgimage.Image(self.booth.thumb_4x1_path,(335,660),self.booth.thumb_4x1_size),"thumbnail")
        self._style3_window.add_inputbox(pginputbox.InputBox((205,840),(380,50),"",self.create_thumb_from_input),"Zeile 1")
        self._style3_window.add_inputbox(pginputbox.InputBox((205,910),(380,50),"",self.create_thumb_from_input),"Zeile 2") 
        self._style3_window.add_image(pgimage.Image("Images/style/Zeile1.png",
                                                    (90,840),
                                                    (95,35)),
                                                    "Zeile 1")
        self._style3_window.add_image(pgimage.Image("Images/style/Zeile2.png",
                                                    (90,910),
                                                    (95,35)),
                                                    "Zeile 2")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Up.png",
                                                       (650, 840),  # (x, y) position
                                                       self.set_font_up), 
                                                       "Font Up")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Down.png",
                                                         (650, 910),  # (x, y) position
                                                         self.set_font_down), 
                                                         "Font Down")
        ## Font Management 
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Up.png",
                                                       (650, 840),  # (x, y) position
                                                       self.set_font_up), 
                                                       "Font Up")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Down.png",
                                                         (650, 910),  # (x, y) position
                                                         self.set_font_down), 
                                                         "Font Down")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Oswald_active.png",
                                                         (740, 840),  # (x, y) position
                                                         lambda: self.set_font("Oswald")), 
                                                         "Oswald")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Bentham.png",
                                                         (920, 840),  # (x, y) position
                                                         lambda: self.set_font("Bentham")), 
                                                         "Bentham")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Flaemisch.png",
                                                         (1100, 840),  # (x, y) position
                                                         lambda: self.set_font("Flaemisch")), 
                                                         "Flaemisch")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Lora.png",
                                                         (740, 910),  # (x, y) position
                                                         lambda: self.set_font("Lora")), 
                                                         "Lora")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Linux.png",
                                                         (920, 910),  # (x, y) position
                                                         lambda: self.set_font("Linux")), 
                                                         "Linux")
        self._style3_window.add_button(pgbutton.Button("Images/style/Font_Great.png",
                                                         (1100, 910),  # (x, y) position
                                                         lambda: self.set_font("Great")), 
                                                         "Great")     
    #def on_event(self, event):
    #     if event.type == pygame.QUIT:
    #         self._running = False
    def shut_down(self):
        pygame.quit()
        self._running=False
        try:
            subprocess.run(["sudo","shutdown","-h","now",],check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")



    def get_free_system_space(self):
        try:
            if platform.system() == "Linux":
                # Use os.statvfs on Linux
                stat_info = os.statvfs("/")
                free_space = stat_info.f_frsize * stat_info.f_bavail
            else:
                # Use psutil for non-Linux systems
                usage = psutil.disk_usage('/')
                free_space = usage.free

        # Convert bytes to gigabytes
            return free_space / (1024**3)
        except Exception as e:
            print(f"Error: {e}")
            return None
    def printone(self):
        self.booth.print_montage("temps/collage.jpg")
        self.booth.save_print_count(self.booth.print_count+1)
        self._current_window = self._printing_window
        self.on_render()
        time.sleep(5)
        self.set_start()
    def printer_restart(self):
        self.booth.printer_restart()
        self._current_window = self._start_window
    def printer_reset_counter(self):
        self.booth.save_print_count(0)
    def open_style_1_window(self):
        self.booth.style_set(1)
        self._current_window = self._style1_window
        self.on_render()
    def open_style_2_window(self):
        self.booth.style_set(2)
        self._current_window = self._style2_window
        self.on_render()
    def open_style_3_window(self):
        self.booth.style_set(3)
        self._current_window = self._style3_window
        self.on_render()
    def open_QR_window(self):
        # tbd.
        pass
    def set_font(self,font_key):
        # Adjust the current thumb_font
        self.booth.thumb_font=os.path.join(working_dictonary,"Fonts",self.booth.thumb_fonts[font_key])
        # Highlight/ activate the current font button on current screen 
        self._current_window.buttons[font_key].update_image("Images/style/Font_"+str(font_key)+"_active.png")
        # Deactivate all other font buttons on current screen 
        other_keys = {key : value for key, value in self.booth.thumb_fonts.items() if key != font_key}
        for key in other_keys:
            self._current_window.buttons[key].update_image("Images/style/Font_"+str(key)+".png")
        self.create_thumb_from_input() 
    def set_font_up(self):
        self.booth.thumb_fontsize +=4
        self.create_thumb_from_input()
    def set_font_down(self):
        self.booth.thumb_fontsize -=4
        self.create_thumb_from_input()
    def save_to_usb(self,status):
        if status:
            try:                                            
                usb_name = os.listdir("/media/fotobox/")[0]
                try:
                    os.mkdir("/media/fotobox/{}/Pics".format(usb_name))
                    self.booth.save_path = "/media/fotobox/{}/Pics/".format(usb_name)
                except OSError:
                    self.booth.save_path = "/media/fotobox/{}/Pics/".format(usb_name)
                    None
                self.settings["usb"] = True
                self._settings_window.buttons["Save USB"] = pgbutton.Button("Images/settings/Save_USB_active.png",
                                                          self._settings_window.buttons["Save USB"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(True))
                self._settings_window.buttons["Save Desktop"] = pgbutton.Button("Images/settings/Save_Desktop.png",
                                                          self._settings_window.buttons["Save Desktop"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(False))
                
            except:
                self.settings["usb"] = False
                self.booth.save_path = self.booth.path_desktop
                self._settings_window.buttons["Save USB"] = pgbutton.Button("Images/settings/Save_USB_erro.png",
                                                          self._settings_window.buttons["Save USB"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(True))
                self._settings_window.buttons["Save Desktop"] = pgbutton.Button("Images/settings/Save_Desktop_active.png",
                                                          self._settings_window.buttons["Save Desktop"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(False))
                print("There is no USB-Stick connected or mounted. Please insert the usb stick again")
        else:
            self.settings["usb"] = False
            self.booth.save_path = self.booth.path_desktop
            self._settings_window.buttons["Save USB"] = pgbutton.Button("Images/settings/Save_USB.png",
                                                          self._settings_window.buttons["Save USB"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(True))
            self._settings_window.buttons["Save Desktop"] = pgbutton.Button("Images/settings/Save_Desktop_active.png",
                                                          self._settings_window.buttons["Save Desktop"].location,  # (x, y) position
                                                          lambda: self.save_to_usb(False))
        self.on_render()
    def cam_preview(self):
        self.booth.cam_preview()
        self._current_window = self._settings_window 
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.fill((0, 0, 0))  # clear all img
        for image in self._current_window.images.values():
            self._display_surf.blit(image.img, image.location)        
        for button in self._current_window.buttons.values():
            self._display_surf.blit(button.img, button.location)
        for box in self._current_window.inputboxes.values():
            # Blit the text
            text_center=box.txt_surface.get_rect(center=(int(box.size[0]/2),int(box.size[1]/2)))
            self._display_surf.blit(box.txt_surface,(box.location[0]+text_center[0],box.location[1]+text_center[1]))    
            # Blit the rect
            pygame.draw.rect(self._display_surf, box.color, box.rect,2)
        for text in self._current_window.texts.values():
            self._display_surf.blit(text.txt_surface,text.location)

        pygame.display.flip()
    def on_exit(self):
        self._running = False    
    def on_cleanup(self):
        pygame.quit()
        self.on_exit()

    def execute(self):
        self.on_init() # Initialise screens etc. 
        self.save_to_usb(self.settings["usb"]) # Initialise that USB-Stick is primary storage
        if __name__ == '__main__':
            while self._running:
                for event in pygame.event.get():
                    self.on_event(event)
                    self.on_loop()
                    self.on_render()
            self.on_cleanup()
    def set_print(self):
        self._current_window = self._after_capture_print_window

    def set_capture(self):
        self._current_window = self._capture_window
        self.on_render()
        self.booth.capture()
        self.last_pic_path = self.booth.make_collage()
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        link = self.NextCloudClient.upload_file(self.last_pic_path,f"Test/{timestamp}.jpg")
        self.NextCloudClient.create_qr(link,timestamp)
             
        if self.settings["printing"]==True and self.settings["Upload"]==False:
            self._after_capture_print_window.images["Montage"].update(self.last_pic_path)
            self._current_window = self._after_capture_print_window
            print(self.last_pic_path)
        elif self.settings["printing"]==False and self.settings["Upload"]==True:
            self._after_capture_QR_window.images["Montage"].update(self.last_pic_path)
            self._after_capture_QR_window.images["QR"].update(self.NextCloudClient.current_qr_path)
            self._current_window = self._after_capture_QR_window
        elif self.settings["printing"]==True and self.settings["Upload"]==True:
            self._after_capture_print_QR_window.images["Montage"].update(self.last_pic_path)
            self._after_capture_print_QR_window.images["QR"].update(self.NextCloudClient.current_qr_path)
            self._current_window = self._after_capture_print_QR_window
        else:
            self._current_window = self._start_window

    def set_start(self):
        self._current_window = self._start_window
    
    def open_settings(self):
        ## Add text to display status of printer
        self._settings_window.add_text(pgtext.Text("Mit der aktuellen Papierrolle und Toner wurden bereits {} Bilder gedruckt".format(self.booth.print_count),
                                                   (300,650),28),"Gedruckte Bilder")
        self._settings_window.add_text(pgtext.Text("Es können mit ihnen noch {} Bilder gedruckt werden".format(self.booth.print_max_count-self.booth.print_count),
                                                   (300,680),28),"Rest Bilder")
        self._settings_window.add_text(pgtext.Text("Wechsel Sie bitte beide, wenn nur noch {} Bilder gedruckt werden können".format(40),
                                                   (300,710),28),"Anweisung1")
        self._settings_window.add_text(pgtext.Text("Starte danach bitte den Drucker neu und Resete den Zähler",
                                                   (300,740),28),"Anweisung2")
        ## Add text to display free storage of SD
        self._settings_window.add_text(pgtext.Text("Der lokale Speicherplatz beträgt {} Gb. Kontaktiere Jonathan wenn kleiner als 1 GB ".format(str(round(self.get_free_system_space(),2))),
                                                   (300,340),28),"Speicherplatz")
        self._current_window = self._settings_window
        self.on_render()
    def create_thumb_from_input(self):
        window=self._current_window
        if window.inputboxes['Zeile 2'].get_text()=="":
            text= str(window.inputboxes['Zeile 1'].get_text()) 
        else:
            text= str(window.inputboxes['Zeile 1'].get_text()) + str("\n")+ str(window.inputboxes['Zeile 2'].get_text())
        self.booth.create_thumb(text,self.booth.get_thumb_size())
        self._current_window.images["thumbnail"].update(window.images["thumbnail"].path)
        self.on_render()
if __name__ == "__main__":
    theApp = App()
    theApp.execute()