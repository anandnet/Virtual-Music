__all__ = ("KivyCamera")
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty,NumericProperty,ListProperty
import cv2
from kivy.graphics.texture import Texture

class KivyCamera(Image):
    fps = NumericProperty(30)
    frame_size=ListProperty((320,240))

    def __init__(self, cap,**kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.register_event_type("on_update")
        self._capture = None
        self._capture = cap
        Clock.schedule_interval(self.update, 1.0 / self.fps)


    @property
    def capture(self):
        return self._capture

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame=self.on_update(frame)
            try:
                if frame.shape[2] is not 3:
                    pass
            except:
                frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
                pass
            #frame=cv2.resize(frame, (640, 480)) 
            buf1 = cv2.flip(frame, 0)
            buf1 = cv2.flip(buf1, 1)
            buf = buf1.tobytes()
            self.frame_size=(frame.shape[1],frame.shape[0])
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
            )
            image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.texture = image_texture
        
    def on_update(self,frame):
        """
        function gives each frame from cam/video source
        can be manupulated accordingly and frame return required
        """
        return frame
