class Window:
    def __init__(self, size):
        self.buttons = {}
        self.images = {}
        self.inputboxes = {}
        self.size = self.width, self.height = size
        self.background = None
    def add_inputbox(self,inputbox, name):
        # inputbox needs to be object of class pyinputbox.InputBox
        self.inputboxes[name]=inputbox
    def add_image(self, image, name):
        # image needs to be object of class pgimage.Image
        self.images[name] = image

    def add_button(self, button, name):
        # button needs to be object of class pgbutton.Button
        self.buttons[name] = button

    def press_button(self, pos):
        for button in self.buttons.values():
            if button.over_button(pos):
                button.event()
                return