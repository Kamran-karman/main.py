import arcade
from arcade.experimental.shadertoy import Shadertoy
import cv2

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
SCREEN_TITLE = "ShaderToy Video"


class ShadertoyVideo(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.shadertoy = Shadertoy(
            self.get_framebuffer_size(),
            """
            void mainImage( out vec4 fragColor, in vec2 fragCoord )
            {
                // Normalized pixel coordinates (from 0 to 1)
                vec2 suv = fragCoord/iResolution.xy;

                fragColor = vec4(1.5 * sin(suv.y * iResolution.y/3. + iTime * 20.));
                fragColor = 1.- floor(abs(fragColor));
                fragColor *= vec4(sin(suv.y), 0, cos( 1. - suv.y * 2.) , 1);
                fragColor *= texture(iChannel0, suv);
            } 
            """,
        )
        # INSERT YOUR OWN VIDEO HERE
        self.video = cv2.VideoCapture("Example.mp4")
        width, height = (
            int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        self.video_texture = self.ctx.texture((width, height), components=3)
        self.video_texture.wrap_x = self.ctx.CLAMP_TO_EDGE
        self.video_texture.wrap_y = self.ctx.CLAMP_TO_EDGE
        self.video_texture.swizzle = "BGR1"
        self.shadertoy.channel_0 = self.video_texture
        self.set_size(width, height)

    def on_draw(self):
        self.clear()
        self.shadertoy.render()

    def on_update(self, delta_time: float):
        self.shadertoy.time += delta_time
        self.next_frame()

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.shadertoy.resize(self.get_framebuffer_size())

    def next_frame(self):
        exists, frame = self.video.read()
        frame = cv2.flip(frame, 0)
        if exists:
            self.video_texture.write(frame)


if __name__ == "__main__":
    ShadertoyVideo(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
