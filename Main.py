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
import PhotoBooth
import socket



working_dictonary= os.getcwd() #Dictonary in which all files are located(images and other classes)
class App(cevent.CEvent):
    def __init__(self):
        self._running = True                                                # Status of the programm
        self._display_surf = None                                           # Display Surface to render everything on
        self.size = self.width, self.height = 1280, 1024                    # Size of the Display Surface
        # Initialize Screens - Basic Functionality
        self._start_window = pgwindow.Window(self.size)                     # Welcome Screen with button to start the PhotoBox
        self._capture_window = pgwindow.Window(self.size)                   # Black-Screen on which Camera Images is overlaided
        self._after_capture_window = pgwindow.Window(self.size)
        # Screens to handle displaying and usage of the images 
        self._development_window = pgwindow.Window(self.size)
        self._printing_window = pgwindow.Window(self.size) 
        # Initialize Screens - Handling Erros - but Insure User - Images are Saved
        self._printing_failed_window = pgwindow.Window(self.size)           # Do i really need it ?
        # Optimizing User Experience                                        
        self._settings_window = pgwindow.Window(self.size)                  # Display for user to configure Box for the event
        self._set_montage_window = pgwindow.Window(self.size)               # Display for user to configure Montage
        # Initializing Start Situation 
        self._current_window = self._start_window
        
        self.settings = {"printing":False, "Upload":True, "usb":True,
                         "FULLSCREEN": False,
                         "Thumb_InBox": True, 
                         "montage_thumb_text" : "Dev Days 2024",
                         "montage_style": 2,
                         "NC-folder":"Dev-Days-2024", 
                         "nc-url":"https://nc-8872520695452827614.nextcloud-ionos.com/",
                         "nc_user":"boxjoni",
                         "nc_pw":"FUUhJw0NTnXw"}  # all settings should reside in this dict
        self.NextCloudClient = PhotoBooth.NextCloudClient(working_dictonary,self.settings["NC-folder"],self.settings["nc-url"],self.settings["nc_user"],self.settings["nc_pw"])
        self.booth = PhotoBooth.PhotoBooth(working_dictonary,self.settings["montage_style"],self.settings["Thumb_InBox"], self.settings["montage_thumb_text"])
        self.last_montage_path = "temps/collage.jpg"
        self.last_QR_path ="temps/QR.jpg"
        

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
        # Uploading 

        self._development_window.add_image(pgimage.Image("Images/Image_Development.png",(380,140),(520,600)),"Upload")
        
        #self._settings_window.add_text(pgtext.Text("Wechsel bitte die Papierrolle und Toner, wenn nur noch {} Bilder gedruckt werden können".format(40),(0,60),28),"Anweisung1")
        #### HIER WEITER ARBEITEN 
        # After Capture Screens - Adding buttons
        self._after_capture_window.add_image(pgimage.Image(self.last_montage_path,(140,55),(1000,667)),"Montage")
        self._after_capture_window.add_image(pgimage.Image("Images/After_Capture/Qr_explain.png",
                                                (140,755),
                                                (645,100),visibility=False),
                                                "Erklärung")
        self._after_capture_window.add_button(pgbutton.Button("Images/After_Capture/Print_b1.png",
                                                      (667,785), self.printone,visibility=False),
                                                      "drucken")
        self._after_capture_window.add_button(pgbutton.Button("Images/After_Capture/Qr_weiter.png",
                                                      (275,785),
                                                      self.set_start,visibility=False),
                                                      "weiter")
        self._after_capture_window.add_image(pgimage.Image(self.NextCloudClient.current_qr_path,
                                                                    (890,745),
                                                                    (250,250),visibility=False),
                                                                    "QR-Code")
        # Printing Screen 
        self._printing_window.add_image(pgimage.Image("Images/Printing.png",
                                                      (400,318),
                                                      (479,326)),
                                                      "Printing")
        
        # Settings - Adding buttons
        ## Mange Screen 
        self._settings_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (85, 20),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "back")
        self._settings_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (490, 20),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        self._settings_window.add_button(pgbutton.Button("Images/settings/ShutDown.png",
                                                         (890, 20),  # (x, y) position
                                                         self.shut_down),
                                                         "shutdown")
        ## Manage Camera and Montage
        self._settings_window.add_button(pgbutton.Button("Images/settings/Camera_Preview.png",
                                                         (15, 165),  # (x, y) position
                                                         self.cam_preview), 
                                                         "preview")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Set_Layout.png",
                                                         (650, 165),  # (x, y) position
                                                         self.open_set_montage_window),
                                                         "Weiter thumbnail")  
        
        ## Manage Use of Montage
        self._settings_window.add_text(pgtext.Text("Wie soll der Nutzer die Montage bekommen",
                                                   (21,300),36),
                                                   "TMontage")
        self._settings_window.add_button(pgbutton.Button("Images/settings/NA_pT_dF.png",
                                                         (21,350),  # (x, y) position
                                                         lambda: self.set_use_montage(True,False)), #
                                                         "pT_dF")
        self._settings_window.add_button(pgbutton.Button("Images/settings/NA_pT_dT.png",
                                                         (330,350),  # (x, y) position
                                                         lambda: self.set_use_montage(True,True)), #
                                                         "pT_dT")
        self._settings_window.add_button(pgbutton.Button("Images/settings/NA_pF_dT.png",
                                                         (655,350),  # (x, y) position
                                                         lambda: self.set_use_montage(False,True)), #
                                                         "pF_dT")
        self._settings_window.add_button(pgbutton.Button("Images/settings/NA_pF_dF.png",
                                                         (970,350),  # (x, y) position
                                                         lambda: self.set_use_montage(False,False)), #
                                                         "pF_dF")
        

        ## Add text to display free storage of SD
        self._settings_window.add_text(pgtext.Text("Speicherort der Bilder",
                                                   (660,490),28),"Speichern")
        self._settings_window.add_text(pgtext.Text("- aktueller Restspeicherplatz: {} Gb.".format(str(round(self.get_free_system_space(),2))),
                                                   (660,640),28),"Speicherplatz")
        

        ## Mange USB 
        
        self._settings_window.add_button(pgbutton.Button("Images/settings/Save_Desktop.png",
                                                         (660,515),  # (x, y) position
                                                         lambda: self.save_to_usb(False)), #
                                                         "Save Desktop")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Save_USB_active.png",
                                                         (970,515),  # (x, y) position
                                                         lambda: self.save_to_usb(True)), #
                                                         "Save USB")
        
        
        ## Manage Printer
        ## Adding Buttons to Manage printer
        self._printer_buttons= []
        self._settings_window.add_button(pgbutton.Button("Images/settings/restart.png",
                                                            (20, 850),  # (x, y) position
                                                            self.printer_restart,visibility=False), 
                                                            "printer restart")
        self._printer_buttons.append("printer restart")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Reset_Counter.png",
                                                            (325, 850),  # (x, y) position
                                                            self.printer_reset_counter,visibility=False), 
                                                            "printer reset counter")
        self._printer_buttons.append("printer reset counter")
        self._settings_window.add_button(pgbutton.Button("Images/settings/Tutorial_Printer.png",
                                                            (20,770),
                                                            self.open_tutorial_printer_window,visibility=False),
                                                            "Tutorial Printer")
        self._printer_buttons.append("Tutorial Printer")
        ## Add text to display status of printer
        self._printer_texts= []
        self._settings_window.add_text(pgtext.Text("Drucker - Status: ",
                                                    (20,490),28),"Drucker Status")
        self._printer_texts.append("Drucker Status")
        self._settings_window.add_text(pgtext.Text("- Verbindung mit Drucker: {}".format("TBD"),
                                                    (20,530),28),"Drucker Verbindung")
        self._printer_texts.append("Drucker Verbindung")
        self._settings_window.add_text(pgtext.Text("- aktueller Zähler Montagen: {}".format(self.booth.print_count),
                                                    (20,570),28),"Drucker Zähler")
        self._printer_texts.append("Drucker Zähler")
        self._settings_window.add_text(pgtext.Text("- Restkapazität: {}".format(self.booth.print_max_count-self.booth.print_count),
                                                    (20,610),28),"Drucker Restkapazität")
        self._printer_texts.append("Drucker Restkapazität")
        self._settings_window.add_text(pgtext.Text("Drucker - Hinweis: ",
                                                    (20,650),28),"Drucker Hinweis")
        self._printer_texts.append("Drucker Hinweis")
        self._settings_window.add_text(pgtext.Text("- Toner und Papier bei Restkapazität von {} wechseln".format(40),
                                                    (20,690),28),"Drucker Anweisung1")
        self._printer_texts.append("Drucker Anweisung1")
        self._settings_window.add_text(pgtext.Text("- Danach ist Neustart und Zäherreset notwendig",
                                                    (20,730),28),"Drucker Anweisung2")
        self._printer_texts.append("Drucker Anweisung2")
        ## Add text for status of NextCloud 
        self._nc_texts = []
        self._settings_window.add_text(pgtext.Text("Cloud - Status:",
                                                        (660,690),28),"Cloud Status")
        self._nc_texts.append("Cloud Status")
        self._settings_window.add_text(pgtext.Text("- Netzwerkstatus: {}".format(self.get_network_connection()),
                                                    (660,730),28),"Network")
        self._nc_texts.append("Network")
        self._settings_window.add_text(pgtext.Text("-Next-Cloud Ordner:",(660,770),28),"NC-Folder")
        self._nc_texts.append("NC-Folder")
        self._settings_window.add_inputbox(pginputbox.InputBox((970,750),(300,40),self.NextCloudClient.get_nc_folder(),
                                                                    self.update_NC_folder),"Input NC-Folder")
        
        self._settings_window.add_text(pgtext.Text("- Status des NC-Ordners {}: {}".format(self.NextCloudClient.get_nc_folder(), 
                                                                                            "Erreichbar " if self.NextCloudClient.check_folder_exist(self.NextCloudClient.nc_folder)
                                                                                            else "Nicht erreichbar"
                                                                                            ),
                                                    (660,810),28),"NC-Erreichbarkeit")
        self._nc_texts.append("NC-Erreichbarkeit")
        # Set Montage Window
        ## Add Buttons User-Experience
        self._set_montage_window.add_button(pgbutton.Button("Images/settings/Back.png",
                                                         (90, 30),  # (x, y) position
                                                         self.open_settings), # anchor
                                                         "back")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Back_Foto.png",
                                                         (500, 30),  # (x, y) position
                                                         self.set_start), # anchor
                                                         "Set Start")
        self._set_montage_window.add_button(pgbutton.Button("Images/settings/close.png",
                                                         (900, 30),  # (x, y) position
                                                         self.on_cleanup),
                                                         "exit")
        ## Add Buttons for user to choose the style
        self._set_montage_window.add_image(pgimage.Image("Images/style/Drucklayout.png",
                                                        (560,160),
                                                        (156,36)),
                                                        "Drucklayout")
        self._style_buttons = []
        self._set_montage_window.add_button(pgbutton.Button("Images/style/style_1.png",
                                                         (90, 205),  # (x, y) position
                                                         lambda: self.set_style_montage(1)), 
                                                         "style_1")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/style_2.png",
                                                         (500, 205),  # (x, y) position
                                                         lambda: self.set_style_montage(2)), 
                                                         "style_2")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/style_3.png",
                                                         (910, 205),  # (x, y) position
                                                         lambda: self.set_style_montage(3)), 
                                                         "style_3")
        ## Add Elements for user to adjust the thumbnail
        self._thumb_images = []
        self._set_montage_window.add_image(pgimage.Image("Images/style/Thumbnaildesign.png",
                                                        (525,615),
                                                        (220,38)),
                                                        "Thumbnaildesign")
        self._thumb_images.append("Thumbnaildesign")
        self._set_montage_window.add_image(pgimage.Image(self.booth.thumb_path,(205,750),(870,68)),"thumbnail")
        self._thumb_images.append("thumbnail")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Thumb_InBox.png",(90,675),lambda: self.set_thumb_source("InBox")),"InBox")
        self._thumb_buttons = []
        self._thumb_buttons.append("InBox")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Thumb_InkScape.png",(800,675),lambda: self.set_thumb_source("InkScape")),"InkScape")
        self._thumb_buttons.append("InkScape")
        ## Add Elements for Font Management 
        self._font_images = []
        self._set_montage_window.add_image(pgimage.Image("Images/style/Zeile1.png",
                                                    (90,840),
                                                    (95,35)),
                                                    "Text Zeile 1")
        self._font_images.append("Text Zeile 1")
        self._set_montage_window.add_image(pgimage.Image("Images/style/Zeile2.png",
                                                    (90,910),
                                                    (95,35)),
                                                    "Text Zeile 2")
        self._font_images.append("Text Zeile 2")
        self._font_input_boxes = []
        self._set_montage_window.add_inputbox(pginputbox.InputBox((205,840),(380,50),"",self.create_thumb_from_input),'Zeile 1')
        self._font_input_boxes.append('Zeile 1')
        self._set_montage_window.add_inputbox(pginputbox.InputBox((205,910),(380,50),"",self.create_thumb_from_input),'Zeile 2')
        self._font_input_boxes.append("Zeile 2")  
        self._font_buttons = []
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Up.png",
                                                       (650, 840),  # (x, y) position
                                                       self.set_font_up), 
                                                       "Font Up")
        self._font_buttons.append("Font Up")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Down.png",
                                                         (650, 910),  # (x, y) position
                                                         self.set_font_down), 
                                                         "Font Down")
        self._font_buttons.append("Font Down")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Oswald_active.png",
                                                         (740, 840),  # (x, y) position
                                                         lambda: self.set_font("Oswald")), 
                                                         "Oswald")
        self._font_buttons.append("Oswald")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Bentham.png",
                                                         (920, 840),  # (x, y) position
                                                         lambda: self.set_font("Bentham")), 
                                                         "Bentham")
        self._font_buttons.append("Bentham")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Flaemisch.png",
                                                         (1100, 840),  # (x, y) position
                                                         lambda: self.set_font("Flaemisch")), 
                                                         "Flaemisch")
        self._font_buttons.append("Flaemisch")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Lora.png",
                                                         (740, 910),  # (x, y) position
                                                         lambda: self.set_font("Lora")), 
                                                         "Lora")
        self._font_buttons.append("Lora")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Linux.png",
                                                         (920, 910),  # (x, y) position
                                                         lambda: self.set_font("Linux")), 
                                                         "Linux")
        self._font_buttons.append("Linux")
        self._set_montage_window.add_button(pgbutton.Button("Images/style/Font_Great.png",
                                                         (1100, 910),  # (x, y) position
                                                         lambda: self.set_font("Great")), 
                                                         "Great")
        self._font_buttons.append("Great")
   
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
    def printer_reset_counter(self):
        self.booth.save_print_count(0)
        self.booth.print_count = self.booth.load_print_count()
        # self.booth.print_count=0
        # print("print count 1",self.booth.print_count)
        print("print count 2",self.booth.print_count)
        print("updatet Count")
        self.open_settings()
    def open_tutorial_printer_window(self):
        pass # tbd.
    def open_set_montage_window(self):
        # Thumb
        for button in self._thumb_buttons:
            self._set_montage_window.buttons[button].visibility=False
        for image in self._thumb_images:
            self._set_montage_window.images[image].visibility = False
        # Font
        for image in self._font_images:
            self._set_montage_window.images[image].visibility = False
        for button in self._font_buttons:
            self._set_montage_window.buttons[button].visibility=False
        for inputbox in self._font_input_boxes:
            self._set_montage_window.inputboxes[inputbox].visibility = False
        if self.booth.thumb:
            if self.booth.thumb_inbox:
                self._set_montage_window.buttons["InBox"].update_image("Images/style/Thumb_InBox_a.png")
                self._set_montage_window.buttons["InkScape"].update_image("Images/style/Thumb_InkScape.png")
            else:
                self._set_montage_window.buttons["InBox"].update_image("Images/style/Thumb_InBox.png")
                self._set_montage_window.buttons["InkScape"].update_image("Images/style/Thumb_InkScape_a.png")
            if self.booth.montage_style==1:
                self._set_montage_window.images["thumbnail"].location= (205,750)
                self._set_montage_window.images["thumbnail"].size=(870,68)
            if self.booth.montage_style==3:
                self._set_montage_window.images["thumbnail"].location= (500,675)
                self._set_montage_window.images["thumbnail"].size=(280 ,130)
            for button in self._thumb_buttons:
                self._set_montage_window.buttons[button].visibility = True
            for image in self._thumb_images:
                self._set_montage_window.images[image].visibility = True
            self._set_montage_window.images["thumbnail"].update(self.booth.thumb_path)
            if self.booth.thumb_inbox==True:
                for button in self._font_buttons:
                    self._set_montage_window.buttons[button].visibility=True
                for image in self._font_images:
                    self._set_montage_window.images[image].visibility = True
                for inputbox in self._font_input_boxes:
                    self._set_montage_window.inputboxes[inputbox].visibility = True 
        self._current_window= self._set_montage_window
        self.on_render()
    def set_style_montage(self,style):
        self._set_montage_window.buttons[f"style_{style}"].update_image(f"Images/style/style_{str(style)}_active.png")
        other_styles = [num for num in range(1, 4) if num != style]
        for c_style in other_styles:
            self._set_montage_window.buttons[f"style_{c_style}"].update_image(f"Images/style/style_{str(c_style)}.png")
        self.booth.set_montage_style(style)
        self.open_set_montage_window()
    def set_thumb_source(self,variable):
        if variable == "InBox":
            self.booth.set_thumb_path(True)
        elif variable =="InkScape":
            self.booth.set_thumb_path(False)
        self.booth.set_montage_style(self.booth.montage_style)
        print(self.booth.thumb_path)
        self.open_set_montage_window() 
            
    def open_QR_window(self):
        # tbd.
        pass
    def set_font(self,font_key):
        # Adjust the current thumb_font
        self.booth.thumb_font=os.path.join(self.booth.base_path,"Fonts",self.booth.thumb_fonts[font_key])
        #self.booth.thumb_font=self.booth.base_path+str(r"\\Fonts\\")+self.booth.thumb_fonts[font_key]
        print(self.booth.thumb_font)
        # Highlight/ activate the current font button on current screen 
        self._set_montage_window.buttons[font_key].update_image("Images/style/Font_"+str(font_key)+"_active.png")
        # Deactivate all other font buttons on current screen 
        other_keys = {key : value for key, value in self.booth.thumb_fonts.items() if key != font_key}
        for key in other_keys:
            self._set_montage_window.buttons[key].update_image("Images/style/Font_"+str(key)+".png")
        self.create_thumb_from_input() 
    def set_font_up(self):
        self.booth.thumb_fontsize +=4
        self.create_thumb_from_input()
    def set_font_down(self):
        self.booth.thumb_fontsize -=4
        self.create_thumb_from_input()
    def set_use_montage(self, b_printing, b_upload):
        self.settings["printing"]=b_printing
        self.settings["Upload"]=b_upload
        self.open_settings()

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
            if image.visibility:
                self._display_surf.blit(image.img, image.location)        
        for button in self._current_window.buttons.values():
            if button.visibility:
                self._display_surf.blit(button.img, button.location)
        for box in self._current_window.inputboxes.values():
            if box.visibility:
                # Blit the text
                text_center=box.txt_surface.get_rect(center=(int(box.size[0]/2),int(box.size[1]/2)))
                self._display_surf.blit(box.txt_surface,(box.location[0]+text_center[0],box.location[1]+text_center[1]))    
                # Blit the rect
                pygame.draw.rect(self._display_surf, box.color, box.rect,2)
        for text in self._current_window.texts.values():
            if text.visibility:
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


    def set_capture(self):
        self._current_window = self._capture_window
        self.on_render()
        self.booth.capture()
        self._current_window = self._development_window
        self.on_render()
        self.last_pic_path = self.booth.make_collage()
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        for button in self._after_capture_window.buttons:
            self._after_capture_window.buttons[button].visibility= False
        for image in self._after_capture_window.images:
            self._after_capture_window.images[image].visibility= False
        if self.booth.montage_style == 1 or self.booth.montage_style==2:
            # Postcard Format
            self._after_capture_window.images["Montage"].size = (1000,667)
            self._after_capture_window.images["Montage"].location = [140,55]
            self._after_capture_window.images["Montage"].update(self.last_pic_path)
            self._after_capture_window.images["Montage"].visibility=True
            if self.settings["Upload"]==True:
                link = self.NextCloudClient.upload_file(self.last_pic_path,f"{timestamp}.jpg")
                self.NextCloudClient.create_qr(link,timestamp)
                print(self.NextCloudClient.get_status_last_update())
                if self.NextCloudClient.get_status_last_update()==True:
                    self._after_capture_window.images["QR-Code"].location=[890,745]
                    self._after_capture_window.images["QR-Code"].update(self.NextCloudClient.current_qr_path)
                    self._after_capture_window.images["QR-Code"].visibility=True
                    if self.settings["printing"]==True:
                        self._after_capture_window.images["Erklärung"].size=(650,88)
                        self._after_capture_window.images["Erklärung"].location=[140,760]
                        self._after_capture_window.images["Erklärung"].update("Images/After_Capture/Print_Qr_explain.png")
                        self._after_capture_window.images["Erklärung"].visibility= True
                        self._after_capture_window.buttons["drucken"].size= (350, 120)
                        self._after_capture_window.buttons["drucken"].location = [515,875]
                        self._after_capture_window.buttons["drucken"].update_image("Images/After_Capture/Print_Qr_b1.png")
                        self._after_capture_window.buttons["drucken"].visibility=True
                        self._after_capture_window.buttons["weiter"].size= (350, 120)
                        self._after_capture_window.buttons["weiter"].location = [140,875]
                        self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Print_Qr_bWeiter.png")
                        self._after_capture_window.buttons["weiter"].visibility=True
                    if self.settings["printing"]==False:
                        self._after_capture_window.images["Erklärung"].size=(645,100)
                        self._after_capture_window.images["Erklärung"].location=[140,755]
                        self._after_capture_window.images["Erklärung"].update("Images/After_Capture/Qr_explain.png")
                        self._after_capture_window.images["Erklärung"].visibility= True
                        self._after_capture_window.buttons["weiter"].size= (730, 120)
                        self._after_capture_window.buttons["weiter"].location = [140,875]
                        self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Qr_weiter.png")
                        self._after_capture_window.buttons["weiter"].visibility=True
            if self.settings["Upload"]==False or self.NextCloudClient.get_status_last_update()== False:
                if self.settings["printing"]==True:
                    self._after_capture_window.buttons["drucken"].size= (470, 150)
                    self._after_capture_window.buttons["drucken"].location = [667,785]
                    self._after_capture_window.buttons["drucken"].update_image("Images/After_Capture/Print_b1.png")
                    self._after_capture_window.buttons["drucken"].visibility=True
                    self._after_capture_window.buttons["weiter"].size= (470, 150)
                    self._after_capture_window.buttons["weiter"].location = [140,785]
                    self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Print_bWeiter.png")
                    self._after_capture_window.buttons["weiter"].visibility=True
                if self.settings["printing"]==False:
                    self._after_capture_window.buttons["weiter"].size= (730, 120)
                    self._after_capture_window.buttons["weiter"].location = [275,875]
                    self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Qr_weiter.png")
                    self._after_capture_window.buttons["weiter"].visibility=True
            
                
        if self.booth.montage_style == 3:
            # Stripe Format
            self._after_capture_window.images["Montage"].size = (300,900)
            self._after_capture_window.images["Montage"].location = [150,60]
            self._after_capture_window.images["Montage"].update(self.last_pic_path)
            self._after_capture_window.images["Montage"].visibility=True
            if self.settings["Upload"]==True:
                link = self.NextCloudClient.upload_file(self.last_pic_path,f"{timestamp}.jpg")
                self.NextCloudClient.create_qr(link,timestamp)
                print(self.NextCloudClient.get_status_last_update())
                if self.NextCloudClient.get_status_last_update()==True:
                    self._after_capture_window.images["QR-Code"].update(self.NextCloudClient.current_qr_path)
                    self._after_capture_window.images["QR-Code"].visibility=True
                    if self.settings["printing"]==True:
                        self._after_capture_window.images["QR-Code"].location=[950,390]
                        self._after_capture_window.images["Erklärung"].size=(650,88)
                        self._after_capture_window.images["Erklärung"].location=[545,265]
                        self._after_capture_window.images["Erklärung"].update("Images/After_Capture/Print_Qr_explain.png")
                        self._after_capture_window.images["Erklärung"].visibility= True
                        self._after_capture_window.buttons["drucken"].size= (350, 120)
                        self._after_capture_window.buttons["drucken"].location = [545,530]
                        self._after_capture_window.buttons["drucken"].update_image("Images/After_Capture/Print_Qr_b1.png")
                        self._after_capture_window.buttons["drucken"].visibility=True
                        self._after_capture_window.buttons["weiter"].size= (350, 120)
                        self._after_capture_window.buttons["weiter"].location = [545,390]
                        self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Print_Qr_bWeiter.png")
                        self._after_capture_window.buttons["weiter"].visibility=True   
                    if self.settings["printing"]==False:
                        self._after_capture_window.images["QR-Code"].location=[745,415]
                        self._after_capture_window.images["Erklärung"].size=(645,100)
                        self._after_capture_window.images["Erklärung"].location=[545,265]
                        self._after_capture_window.images["Erklärung"].update("Images/After_Capture/Qr_explain.png")
                        self._after_capture_window.images["Erklärung"].visibility= True
                        self._after_capture_window.buttons["weiter"].size= (730, 120)
                        self._after_capture_window.buttons["weiter"].location = [500,720]
                        self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Qr_weiter.png")
                        self._after_capture_window.buttons["weiter"].visibility=True
            if self.settings["Upload"]==False or self.NextCloudClient.get_status_last_update()== False:
                if self.settings["printing"]==True:
                    self._after_capture_window.buttons["drucken"].size= (470, 150)
                    self._after_capture_window.buttons["drucken"].location = [630,570]
                    self._after_capture_window.buttons["drucken"].update_image("Images/After_Capture/Print_b1.png")
                    self._after_capture_window.buttons["drucken"].visibility=True
                    self._after_capture_window.buttons["weiter"].size= (470, 150)
                    self._after_capture_window.buttons["weiter"].location = [630,300]
                    self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Print_bWeiter.png")
                    self._after_capture_window.buttons["weiter"].visibility=True
                if self.settings["printing"]==False:
                    self._after_capture_window.buttons["weiter"].size= (730, 120)
                    self._after_capture_window.buttons["weiter"].location = [505,450]
                    self._after_capture_window.buttons["weiter"].update_image("Images/After_Capture/Qr_weiter.png")
                    self._after_capture_window.buttons["weiter"].visibility=True    
            pass
        
        # Next Step handle false Upload :(
        
        self._current_window = self._after_capture_window
        
        """
        self._after_capture_window.add_image(pgimage.Image(self.last_montage_path,(140,55),(1000,667)),"Montage")
        self._after_capture_window.add_image(pgimage.Image("Images/After_Capture/Qr_explain.png",
                                                (140,755),
                                                (645,100),visibility=False),
                                                "Erklärung")
        self._after_capture_window.add_button(pgbutton.Button("Images/After_Capture/Print_b1.png",
                                                      (667,785), self.printone,visibility=False),
                                                      "drucken")
        self._after_capture_window.add_button(pgbutton.Button("Images/After_Capture/Qr_weiter.png",
                                                      (275,785),
                                                      self.set_start,visibility=False),
                                                      "weiter")
        self._after_capture_window.add_image(pgimage.Image(self.NextCloudClient.current_qr_path,
                                                                    (890,745),
                                                                    (250,250),visibility=False),
                                                                    "QR-Code")
        
        
        """
        
        
        """
        if self.settings["Upload"]==True:
            link = self.NextCloudClient.upload_file2(self.last_pic_path,f"{timestamp}.jpg")
            if self.NextCloudClient.last_upload_succesfull:
                self.NextCloudClient.create_qr(link,timestamp)
                if self.settings["printing"]==True:

                    self._after_capture_print_QR_window.images["Montage"].update(self.last_pic_path)
                    self._after_capture_print_QR_window.images["QR"].update(self.NextCloudClient.current_qr_path)
                    self._current_window = self._after_capture_print_QR_window
                else:
                    self._after_capture_QR_window.images["Montage"].update(self.last_pic_path)
                    self._after_capture_QR_window.images["QR"].update(self.NextCloudClient.current_qr_path)
                    self._current_window = self._after_capture_QR_window
            else:
                if self.settings["printing"]==True:
                    self._after_capture_print_window.images["Montage"].update(self.last_pic_path)
                    self._current_window = self._after_capture_print_window
                else:
                    self._after_capture_window.images["Montage"].update(self.last_pic_path)
                    self._current_window = self._after_capture_window
        else:
            if self.settings["printing"]==True:
                self._after_capture_print_window.images["Montage"].update(self.last_pic_path)
                self._current_window = self._after_capture_print_window
            else:
                self._after_capture_window.images["Montage"].update(self.last_pic_path)
                self._current_window = self._after_capture_window
        """
    def set_start(self):
        self._current_window = self._start_window
    
    def open_settings(self):
        # Update Buttons to decide how to provide montage  
        self._settings_window.buttons["pT_dF"].update_image("Images/settings/NA_pT_dF.png")
        self._settings_window.buttons["pT_dT"].update_image("Images/settings/NA_pT_dT.png")
        self._settings_window.buttons["pF_dT"].update_image("Images/settings/NA_pF_dT.png")
        self._settings_window.buttons["pF_dF"].update_image("Images/settings/NA_pF_dF.png")
        if self.settings["printing"]== True and self.settings["Upload"]==False:
            self._settings_window.buttons["pT_dF"].update_image("Images/settings/A_pT_dF.png")
        if self.settings["printing"]== True and self.settings["Upload"]==True:
            self._settings_window.buttons["pT_dT"].update_image("Images/settings/A_pT_dT.png")
        if self.settings["printing"]== False and self.settings["Upload"]==True:
            self._settings_window.buttons["pF_dT"].update_image("Images/settings/A_pF_dT.png")
        if self.settings["printing"]== False and self.settings["Upload"]==False:
            self._settings_window.buttons["pF_dF"].update_image("Images/settings/A_pF_dF.png")
        ## Update Speicherplatz 
        self._settings_window.texts["Speicherplatz"].update_text("- aktueller Restspeicherplatz: {} Gb.".format(str(round(self.get_free_system_space(),2))))
        # Set Visibility to False for all elements related to printing and nc
        for text in self._printer_texts:
            self._settings_window.texts[text].visibility=False
        for button in self._printer_buttons:
            self._settings_window.buttons[button].visibility=False
        for text in self._nc_texts:
            self._settings_window.texts[text].visibility=False
        self._settings_window.inputboxes["Input NC-Folder"].visibility = False
        # Update and set Visible elements related to printing
        if self.settings["printing"]:
            # Updating Dynamic Text
            self._settings_window.texts["Drucker Zähler"].update_text("- aktueller Zähler Montagen: {}".format(self.booth.print_count))
            self._settings_window.texts["Drucker Restkapazität"].update_text("- Restkapazität: {}".format(self.booth.print_max_count-self.booth.print_count))            
            # Setting Visibility
            for text in self._printer_texts:
                self._settings_window.texts[text].visibility=True
            for button in self._printer_buttons:
                self._settings_window.buttons[button].visibility=True
        # Update and set Visible elements related to NC-Cloud 
        if self.settings["Upload"]:
            # Updating Dynamic Elements
            self._settings_window.texts["Network"].update_text("- Netzwerkstatus: {}".format(self.get_network_connection()))
            self._settings_window.inputboxes["Input NC-Folder"].update_text(str(self.NextCloudClient.get_nc_folder()))
            self._settings_window.texts["NC-Erreichbarkeit"].update_text("- Status des NC-Ordners {}: {}".format(self.NextCloudClient.get_nc_folder(), 
                                                                                            "Erreichbar " if self.NextCloudClient.check_folder_exist(self.NextCloudClient.nc_folder)
                                                                                            else "Nicht erreichbar"
                                                                                            ))
            # Setting Visibility
            for text in self._nc_texts:
                self._settings_window.texts[text].visibility=True
            self._settings_window.inputboxes["Input NC-Folder"].visibility = True
        
        self._current_window= self._settings_window
        self.on_render()
    def update_NC_folder(self):
        self._current_window = self._settings_window 
        c_folder_name = str(self._settings_window.inputboxes["Input NC-Folder"].get_text())
        self._settings_window.texts["NC-Erreichbarkeit"].update_text(" ")
        print("before ob render 1")
        self.open_settings()
        self._settings_window.texts["NC-Erreichbarkeit"].update_text("- Status des NC-Ordners {}:".format(self.NextCloudClient.get_nc_folder()))
        self.NextCloudClient.set_nc_folder(c_folder_name)
        print("before ob render 2")
        self.open_settings()
        self.NextCloudClient.create_folder(c_folder_name)
        self._settings_window.texts["NC-Erreichbarkeit"].update_text("- Status des NC-Ordners {}: {}".format(self.NextCloudClient.get_nc_folder(), 
                                                                                            "Erreichbar " if self.NextCloudClient.check_folder_exist(self.NextCloudClient.nc_folder)
                                                                                            else "Nicht erreichbar"
                                                                                            ))
        self.open_settings()
    def create_thumb_from_input(self):
        window=self._set_montage_window
        if window.inputboxes['Zeile 2'].get_text()=="":
            text= str(window.inputboxes['Zeile 1'].get_text()) 
        else:
            text= str(window.inputboxes['Zeile 1'].get_text()) + str("\n")+ str(window.inputboxes['Zeile 2'].get_text())
        self.booth.create_thumb(text,self.booth.get_thumb_size())
        self.open_set_montage_window()
    def get_network_connection(self,host="8.8.8.8", port=53, timeout=3):
        try:
            # Create a socket object
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Try connecting to the host
            s.connect((host, port))
            
            # If connection was successful, close the socket
            s.close()
            return "Connected"
        except Exception as e:
            print(f"An network error occurred: {e}")
            return "Not Connected"
if __name__ == "__main__":
    theApp = App()
    theApp.execute()
