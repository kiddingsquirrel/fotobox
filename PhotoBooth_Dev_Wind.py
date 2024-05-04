import sys
from PIL import Image, ImageOps,ImageFont, ImageColor, ImageDraw
import time
import pygame
import os
import shutil
from nc_py_api import Nextcloud
import qrcode

class NextCloudClient:
    def __init__(self,base_path,nc_folder, url, user, password):
        self.client = Nextcloud(nextcloud_url = url,nc_auth_user=user, nc_auth_pass=password)
        print(self.client.files.sharing.available)
        self.folder = nc_folder
        self.basepath = base_path
        self.current_link = None
        self.current_qr_path = os.path.join(base_path,"temps/","QR.png")
    
    def print_structure(self):
        
        all_files_folders = self.client.files.listdir(depth=-1)
        for obj in all_files_folders:
            print(obj.user_path)
    def upload_file(self,local_path, destination_path):
        try:
            with open(local_path,"rb") as file:
                file_data = file.read() # Ensure that fill is read correctly 
                response=self.client.files.upload(destination_path, file_data)
                print(response)
                link = self.client.files.sharing.create(destination_path,3).url
                print(link)
                return(link)
        except Exception as e:
            print(f"There was a problem uploading and creating the link: {e}")
            return None
        
    def create_qr(self, link, timestamp):
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4)
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            self.current_qr_path = os.path.join(self.basepath,"temps","QR.png")
            img.save(self.current_qr_path)
            print(f"Created qr-Code for {link}")
        except:
            print(f"Error creating QR-Code for {link}")
        
        print("Created QR")
                             
class PhotoBooth:
    
    def __init__(self,base_path):
        self.base_path = base_path
        # Define some Constants: ------------------------------------
        # Style 2 is default
        # Image Capturing
        self.resolution = (2340,1523) # px(width,height)  capturing
        self.pic_size = (860,560)   # px(width,height) on montage
        # Printing 
        self.printer ="D80_4x6x2" #Name of the printer
        self.slip_format = (1800,1200) # px of the paper 
        self.paper_format = (1800, 2400) # px of paper which will be cut
        self.print_rows= 2   # number of rows of montage on print
        self.print_colums= 1 # number of colums of montage on print
        # Montage
        self.total_pics = 4 # number of pictures taken
        self.grid_rows = 2  # number of rows on montage
        self.grid_colums= 2 # number of columns on montage
        self.x_offset= 25
        self.x_space = 25      
        self.y_space = 25
        self.y_offset= 25
        self.thumb = False  # Is there a thumbnail
        self.thumb_4x1_path= os.path.join(self.base_path,"Thumbnails/4x1_Montage/thumb.png")
        self.thumb_4x1_size= (600, 135) 
        self.thumb_2x2_path= os.path.join(self.base_path,"Thumbnails/2x2_Montage/thumb.png")
        self.thumb_2x2_size= (1740, 135) 

        self.thumb_size = self.thumb_4x1_size
        self.thumb_path = self.thumb_4x1_path
        
        self.thumb_fonts = {'Oswald':'Oswald/Oswald-VariableFont_wght.ttf',
                            'Bentham':'Bentham/Bentham-Regular.ttf',
                            'Flaemisch':'flaemische-kanzleischrift/Flaemische Kanzleischrift.ttf',
                            'Lora':'Lora/Lora-VariableFont_wght.ttf',
                            'Linux':'linux_biolinum/LinBiolinum_R.ttf',
                            'Great':'Great_Vibes/GreatVibes-Regular.ttf'}
        self.thumb_font = os.path.join(self.base_path,"/Fonts/Oswald/Oswald-VariableFont_wght.ttf")
        self.thumb_fontsize = 50 
        self.thumb_img = Image.open(self.thumb_path) # Open Image for the thumbnail
        self.thumb_img.resize((self.thumb_size[0], self.thumb_size[1])) # Image for the thumbnail 
        #Print Management and Log
        self.print_log_path = os.path.join(self.base_path,"print_log.txt")
        self.print_count = self.load_print_count() 
        self.print_max_count = 215
        #File Management
        self.path_desktop = os.path.join(self.base_path,"Dummy_Desktop/")
        self.path_media = os.path.join(self.base_path,"Dummy_Media")
        self.save_path = self.path_media
        self.back_up_path = os.path.join(self.base_path,"Dummy_Backup/")  
        try:
            os.mkdir(self.save_path)
        except OSError:
            None
        # -----------------------------------------------------------
        pygame.init()
        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)  
    def load_print_count(self):
        try:
            with open(self.print_log_path,"r") as file:
                count= int(file.read())
                print(f"The current print cout is {str(count)}")
                return count
        except FileNotFoundError as e:
            print(f"Error: {e}")
            # Creat File if it doesn't exist and return 0
            self.save_print_count(str(0))
            return int(0)
    def save_print_count(self,count):
        with open(self.print_log_path,"w") as file:
            file.write(str(count))        
    def get_thumb_status(self):
        return self.thumb
    def get_thumb_size(self):
        return self.thumb_size
    def style_set(self,style):
        if style == 1: #4Bilder + Thumbnail - 4x6*2 Paper Slipe
            # Image Capturing
            self.resolution = (2340,1316) # px(width,height)  capturing
            self.pic_size = (860,480)   # px(width,height) on montage
            # Printing 
            self.printer ="D80_4x6x2" #Name of the printer
            self.slip_format = (1800,1200) # px of the paper 
            self.paper_format = (1800, 2400) # px of paper which will be cut
            self.print_rows= 2   # number of rows of montage on print
            self.print_colums= 1 # number of colums of montage on print
            # Monatge
            self.total_pics = 4 # number of pictures taken
            self.grid_rows = 2  # number of rows on montage
            self.grid_colums= 2 # number of columns on montage
            self.x_offset= 25
            self.x_space = 25      
            self.y_space = 25
            self.y_offset= 25
            self.thumb = True  # Is there a thumbnail
            self.thumb_size = self.thumb_2x2_size # px of thumbnail image
            self.thumb_path = self.thumb_2x2_path# path to the thumbnail
        if style == 2: #4Bilder
            # Image Capturing
            self.resolution = (2340,1523) # px(width,height)  capturing
            self.pic_size = (860,560)   # px(width,height) on montage
            # Printing 
            self.printer ="D80_4x6x2"#Name of the printer
            self.slip_format = (1800,1200) # px of the paper 
            self.paper_format = (1800, 2400) # px of paper which will be cut
            # Monatge
            self.total_pics = 4 # number of pictures taken
            self.grid_rows = 2  # number of rows on montage
            self.grid_colums= 2 # number of columns on montage
            self.x_offset= 25
            self.x_space = 25      
            self.y_space = 25
            self.y_offset= 25
            self.thumb = False  # Is there a thumbnail
        if style == 3: # 4 Bilder + Thumbnail - 2x6*2 Paper Slipe
            # Image Capturing
            self.resolution = (2340,1523) #self._current_window.buttons[font_key].update_image("Images/style/Font_"+str(font_key)+"_active.png") px(width,height)  capturing
            self.pic_size = (530,350)   # px(width,height) on montage
            # Printing 
            self.printer ="D80_2x6x2" #Name of the printer
            self.slip_format = (600,1800) # px of the paper 
            self.paper_format = (1200, 1800) # px of paper which will be cut
            self.print_rows= 1   # number of rows of montage on print
            self.print_colums= 2 # number of colums of montage on print
            # Monatge
            self.total_pics = 4 # number of pictures taken
            self.grid_rows = 4  # number of rows on montage
            self.grid_colums= 1 # number of columns on montage
            self.x_offset= 25
            self.x_space = 40      
            self.y_space = 25
            self.y_offset= 25
            self.thumb = True  # Is there a thumbnail
            self.thumb_size = self.thumb_4x1_size# px of thumbnail image
            self.thumb_path = self.thumb_4x1_path # path to the thumbnail

    def show_image(self, image_path):
        pygame.init()
        pygame.display.set_caption('Photo Booth Pics')
        pygame.mouse.set_visible(True)  # hide or show the mouse cursor
        screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, self.size)  # resize to screen size
        screen.blit(img,(self.offset_x, self.offset_y))
        pygame.display.flip()
        
    def printer_restart(self):
        printer = self.printer
        line = str("sudo cupsenable ")+printer
        print(line)
        os.system(line)

    def capture(self):
        pass
        
    def cam_preview(self):
        pass
    
    def make_collage(self):
        now = time.strftime("%Y-%m-%d-%H-%M-%S")
	## Open Images and Make Collage 
        file_path = "{}booth_{}.jpg".format(self.save_path, now)
        images = map(Image.open, ["temps/image_{}.jpg".format(i) for i in range(self.total_pics)])          
        images = map(ImageOps.mirror, images)
        images = list(images)
        print(["temps/image_{}.jpg".format(i) for i in range(self.total_pics)])
        # y_space = (self.paper_format[1]-(self.pic_size[1]*4))/5.
        y_off = self.y_offset
        new_im = Image.new('RGB', self.slip_format, color=(255,255,255))
        im_number =0
        row =0
        for row in range(0,self.grid_rows,1):
            colum=0
            x_off = self.x_offset
            for colum in range(0,self.grid_colums,1):
                im = images[im_number]
                im = im.resize((self.pic_size[0], self.pic_size[1]))
                #flipped = im.tranself.thumb_fontsizespose(method=Image.ROTATE_180)
                #new_im.paste(flipped, (0, int(y_off)))self._style1_window.add_image(pgimage.Image("Images/style/Zeile1.png",
                new_im.paste(im, (int(x_off), int(y_off)))
                x_off += self.x_space + im.size[0]
                im_number +=1
            y_off += self.y_space+im.size[1]
        if self.thumb == True:
            self.thumb_img = Image.open(self.thumb_path)
            self.thumb_img.resize((self.thumb_size[0], self.thumb_size[1]))
            new_im.paste(self.thumb_img,(0, y_off))
        ## Save Thumbnail
        new_im.save(os.path.expanduser(file_path))
        new_im.save("temps/collage.jpg")
        
	##Create Back-Up Folder of images
        current_back_up_folder = "{}/{}".format(self.back_up_path,now)
        shutil.copytree("temps",current_back_up_folder)
        current_back_up_folder = "{}/{}".format(self.save_path,now)
        shutil.copytree("temps",current_back_up_folder)
        ## Return paths
        print("make collage returns:", file_path)
        return file_path

    def take_pic(self):
        # takes picture, makes collage and returns path to collage
        # Instruction Image
        self.show_image("Images/instructions.png")
        time.sleep(2)
        self.capture()
        now = time.strftime("%Y-%m-%d-%H-%M")
        dest_file = "~/Desktop/Booth_Pics/booth_{}.jpg".format(now)
        self.make_collage(dest_file)
        # self.show_image("~/Desktop/Booth_Pics/booth_{}.jpg".format(now))
        # sleep(timedisplay)
        # print pic

    def print_montage(self, dest_file):
        img = Image.open(dest_file)
        img_print = Image.new("RGB", self.paper_format, color=(255,255,255))
        y_off=0
        for row in range(0,self.print_rows,1):
            colum=0
            x_off=0
            for colum in range(0,self.print_colums,1):
                img_print.paste(img,(int(x_off),int(y_off)))
                x_off += img.size[0]
            y_off += img.size[1]
        img_print.save("temps/print_tmp.png")
        line= str("sudo lp -d ") + self.printer +str(" ") + str("temps/print_tmp.png")
        print(line)
        os.system(line)  # -o media=Custom.7.4x21.0cm
        self.save_print_count(self.print_count+1)
    def create_thumb(self,text,size,anchor="mm",align="center"):
        font =  self.thumb_font
        fontsize = self.thumb_fontsize
        self.thumb_img= Image.new(mode="RGBA",size=size,color="white")
        font = ImageFont.truetype(font,fontsize)   
        draw = ImageDraw.Draw(self.thumb_img)
        draw.multiline_text((size[0]/2,size[1]/2),text,anchor=anchor,align=align,font=font, fill="black")
        self.thumb_img.save(self.thumb_path)
        print("saved new thumb to", self.thumb_path)  

