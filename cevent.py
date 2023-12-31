import pygame
# from pygame.locals import *


class CEvent:
    def __init__(self):
        pass

    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass

    def on_key_down(self, event):
        if event.key == 27:
            self.on_exit()
        self._current_window.input_inputbox(event)

    def on_key_up(self, event):
        pass

    def on_mouse_focus(self):
        pass

    def on_mouse_blur(self):
        pass

    def on_mouse_move(self, event):
        pass

    def on_mouse_wheel(self, event):
        pass

    def on_lbutton_up(self, event):
        pass

    def on_lbutton_down(self, event):
        self._current_window.press_button(pygame.mouse.get_pos())
        self._current_window.press_inputbox(pygame.mouse.get_pos())

    def on_rbutton_up(self, event):
        pass

    def on_rbutton_down(self, event):
        pass

    def on_mbutton_up(self, event):
        pass

    def on_mbutton_down(self, event):
        pass

    def on_minimize(self):
        pass

    def on_restore(self):
        pass

    def on_resize(self, event):
        pass

    def on_expose(self):
        pass

    def on_exit(self):
        pass

    def on_user(self, event):
        pass

    def on_joy_axis(self, event):
        pass

    def on_joybutton_up(self, event):
        pass

    def on_joybutton_down(self, event):
        pass

    def on_joy_hat(self, event):
        pass

    def on_joy_ball(self, event):
        pass

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.on_exit()

        elif event.type >= pygame.USEREVENT:
            self.on_user(event)

        elif event.type == pygame.VIDEOEXPOSE:
            self.on_expose()

        elif event.type == pygame.VIDEORESIZE:
            self.on_resize(event)

        elif event.type == pygame.KEYUP:
            self.on_key_up(event)

        elif event.type == pygame.KEYDOWN:
            self.on_key_down(event)

        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_move(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 0:
                self.on_lbutton_up(event)
            elif event.button == 1:
                self.on_mbutton_up(event)
            elif event.button == 2:
                    self.on_rbutton_up(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)

        elif event.type == pygame.ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()


if __name__ == "__main__":
    event = CEvent()
