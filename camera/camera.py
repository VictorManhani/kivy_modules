from kivy.app import App
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.graphics import Rectangle, Canvas
from kivy.graphics.texture import Texture

import time
import numpy as np
import cv2

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(5)
    
    Camera:
        id: camera
        resolution: 500, 500

    BoxLayout:
        Image:
			id: image
            texture: self.texture

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '48dp'
        Button:
            text: 'Start'
            on_release:
                camera.play = True

        Button:
            text: 'Stop'
            on_release: camera.play = False
        
        Button:
            text: 'Capture'
            on_release: app.capture()
        
        Button:
            text: "Texture"
            on_release:
                app.save()
'''

class CameraApp(App):
    def save(self):
        camera = self.root.ids['camera']
        image = self.root.ids['image']
        texture = Texture.create(size = camera.texture.size)
        
        texture.blit_buffer(
            camera.texture.pixels, 
            colorfmt = camera.texture.colorfmt, 
            bufferfmt =  'ubyte' # camera.texture.bufferfmt
        )
        
        with image.canvas:
            Rectangle(
                texture = texture, 
                pos = image.pos, 
                size = image.size
            )

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.root.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    CameraApp().run()