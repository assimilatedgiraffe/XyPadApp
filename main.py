from kivy.app import App
from kivy.lib import osc
from kivy.lib.osc import oscAPI
from kivy.uix.button import *
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import *

oscIpAddress = '192.168.1.7'
oscPort = 9000


class XyPad(Button):

    def __init__(self, *args, **kwargs):
        super(XyPad, self).__init__(*args, **kwargs)
        self.x_msg = ''
        self.y_msg = ''

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            print(touch.pos)
            rel_pos = self.to_widget(*touch.pos, relative=True)
            x_scaled, y_scaled = rel_pos[0]/self.width , rel_pos[1] / self.height

            osc.sendMsg(self.x_msg, [x_scaled, ], ipAddr=oscIpAddress, port=oscPort)
            osc.sendMsg(self.y_msg, [y_scaled, ], ipAddr=oscIpAddress, port=oscPort)

            with self.canvas:
                Rectangle(pos=(rel_pos[0], self.y), size=(5, self.height))


class xypadApp(App):
    def build(self):
        oscAPI.init()
        main_layout = StackLayout()
        for i in range(4):
            xy_pad = XyPad(size_hint=(0.5, 0.5))
            xy_pad.x_msg = '/fxparam/{0}/value'.format(i*2 + 1)
            xy_pad.y_msg = '/fxparam/{0}/value'.format(i*2 + 2)
            main_layout.add_widget(xy_pad)

        return main_layout


if __name__ == '__main__':
    xypadApp().run()