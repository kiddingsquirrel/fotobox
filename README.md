# Photobooth (Germnan Fotobox) 
A small python project to run a photobooth on a raspberry pi.
General principale of Photobooth:
  - Welcome screen with "Button to start capturing"
  - Capturing of 4 images with an overlayed countdown
  - Displaying of created montage of 4 images with button to print montage
The project contains two versions:
  - Version_2023 (ideal for single event) 
    - Simple GUI with limited setting options (secret button left top corner of Welcome screeen) 
    - Operating mode fixed to only allow printing
    - Appearance of the montage is fixed in code
  - Version_2024 (optimized for renting)
    - Upload of montage to nextcloud downloadable by QR-Code
    - Choice of 4 operating mode (providing the montage to user)
        - printing
        - printing with upload to nextcloud
        - upload to next cloud
        - only displaying the montage
    - Choice of 3 montage styles
        - 4 images on a post card with a thumbnail
        - 4 images on a post card
        - 4 images on a paper slip with a thumbnail
    - Creation of the thumbnail within the box
   
# Requirements
- Hardware:
  -    Raspberry Pi (tested models: raspberry pi 3, raspberry pi 4)
  -    SD-Card (between 8 to 32 Gb storage)
  -    Raspberry Pi CAM (tested models: pi camera, pi-camera HQ)
  -    Display or Touchscreen
- Software:
  -   Raspi-OS legacy 32bit (to support raspicam)
  -   pygame (GUI)
- Optional:
  -   Printer (teste models: Mitsubishi CP D80, Canon Shelpy CP 1300)
  -   GPIO buttons
  -   LEDs
 # Installation
 - Install and test picanera 
 - Clone the repository branch of the desired version
 - Follow the great turorial of https://www.peachyphotos.com/blog/stories/building-modern-gutenprint/ to install gutenprint
 - Set up the Main.py script to be executed on autostart
 - Have fun .....
 
