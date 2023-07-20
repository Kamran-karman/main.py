import random
import time
import arcade
import arcade.gui
from dataclasses import dataclass
from array import array
import arcade.gl
import Pers

W = 1600
H = 900


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class Radius(arcade.Sprite):
    def __init__(self, razmer=2):
        super().__init__()

        self.rad = load_tex_pair('nuzhno/radius_porazheniya.png')
        if razmer == 0:
            self.scale = 0.0306
        if razmer == 1:
            self.scale = 0.102
        elif razmer == 2:
            self.scale = 0.204
        elif razmer == 3:
            self.scale = 0.408
        self.texture = self.rad[1]


class Igra1GlavaViev(arcade.View):
  def __init__(self):
    super().__init__()
        arcade.set_background_color((255, 182, 193))

        # Переменные для частиц
        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='shederi_igra/ver_shad_tl_ogon.glsl',
                                                    fragment_shader='shederi_igra/frag_shad_tl_ogon.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.walls_list = None
        self.platforms_list = None

        self.fizika = None

        self.kamera = None

        # GUI-переменные
        self.meneger = None
        self.meneger1 = None
        self.meneger2 = None
        self.text = ''
        self.text_info = None
        self.text_info1 = None
        self.text_info2 = None
        self.v_box = None
        self.v_box1 = None

        # Переменные True, либо False
        self.levo = False
        self.pravo = False
        self.beg = False=

        self.t_main_patch = (':resources:images/tiles/')
    def setup(self):
