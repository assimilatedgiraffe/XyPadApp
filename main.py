from kivy.app import App
from kivy.lib import osc
from kivy.lib.osc import oscAPI
from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.button import *
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import *

oscIpAddress = '192.168.1.7'
oscPort = 9000


class XyPad(Button):

    x_param_value = BoundedNumericProperty(0, min=0, max=1, errorhandler=lambda x: 1 if x > 1 else 0)
    y_param_value = BoundedNumericProperty(0, min=0, max=1, errorhandler=lambda x: 1 if x > 1 else 0)
    lines = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(XyPad, self).__init__(*args, **kwargs)
        self.x_msg = ''
        self.y_msg = ''
#        self.x_param_value = BoundedNumericProperty(0, min=0, max=1, errorhandler=lambda x: 1 if x > 1 else 0)
#        self.y_param_value = BoundedNumericProperty(0, min=0, max=1, errorhandler=lambda x: 1 if x > 1 else 0)
#        lines = []
        with self.canvas:
            Color(0, 1, 0, 1)  # set the colour to green
            self.lines = [Rectangle(), Rectangle(), Ellipse(size=(50,50))]

        self.bind(pos=self.update_lines, size=self.update_lines)


    def update_lines(self, *args):
        self.lines[0].pos = self.x + 0.5*self.width, self.y
        self.lines[0].size = (3, self.height)
        self.lines[1].pos = self.x, self.y + 0.5*self.height
        self.lines[1].size = (self.width, 3)
        self.lines[2].pos = self.center_x - 25, self.center_y - 25

#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             with self.canvas:
#                 #Color(ud['color'], 1, 1, mode='hsv', group=g)
#                 touch.ud['lines'] = [
#                     Rectangle(pos=(touch.x, self.y), size=(3, self.height)),
#                     Rectangle(pos=(self.x, touch.y), size=(self.width, 3))]
#                     Point(points=(touch.x, touch.y), pointsize=5)]




    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            print(touch.pos)
            rel_pos = self.to_widget(*touch.pos, relative=True)
            x_scaled, y_scaled = rel_pos[0]/self.width, rel_pos[1] / self.height

            osc.sendMsg(self.x_msg, [x_scaled, ], ipAddr=oscIpAddress, port=oscPort)
            osc.sendMsg(self.y_msg, [y_scaled, ], ipAddr=oscIpAddress, port=oscPort)

            self.x_param_value = x_scaled
            self.y_param_value = y_scaled

    def on_x_param_value(self, obj, value):
        self.lines[0].pos = self.x + value*self.width, self.y
        self.lines[2].pos = self.x + value*self.width - 25, self.lines[2].pos[1]

    def on_y_param_value(self, obj, value):
        self.lines[1].pos = self.x, self.y + value*self.height
        self.lines[2].pos = self.lines[2].pos[0], self.y + value*self.height - 25,

    # def on_touch_up(self, touch):
    #     #if self.collide_point(*touch.pos):
    #     print(touch.ud['lines'])
    #     for line in se:
    #             self.canvas.remove(line)


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