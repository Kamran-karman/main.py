import random
import time
import arcade
import arcade.gui
from dataclasses import dataclass
from array import array
import arcade.gl
import pers

W = 1600
H = 900

GRAVITY = (0, -1000)
DAMPING = 0.9
IGROK_MOVE_GROUND = 7000
MASS_IGROK = 1.5
FRICTION_IGROK = 0.2
IG_COLLISION_TYPE = 'player'
IG_MAX_VERTICAL_SPEED = 1600
IG_MAX_HORIZANTAL_SPEED = 200
WALL_FRICTION = 0.1
WALL_COLLISION_TYPE = 'wall'


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class Radius(arcade.Sprite):
    def __init__(self, razmer=2):
        super().__init__()

        self.rad = pers.load_tex_pair('nuzhno/radius_porazheniya.png')
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
        #arcade.set_background_color((255, 182, 193))

        # Переменные для частиц
        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='shederi_igra/ver_shad_tl_ogon.glsl',
                                                    fragment_shader='shederi_igra/frag_shad_tl_ogon.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.igrok = None

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
        self.beg = False

        self.t_main_patch = (':resources:images/tiles/')

    def setup(self):
        self.igrok = pers.IgrokVoyslav()

        self.walls_list = arcade.SpriteList()
        for x in range(-64, 1700, 128):
            wall = arcade.Sprite(':resources:images/tiles/dirtMid.png')
            wall.position = x, 64
            self.walls_list.append(wall)

        self.fizika = arcade.PymunkPhysicsEngine(GRAVITY, DAMPING)
        self.fizika.add_sprite(self.igrok, MASS_IGROK, FRICTION_IGROK, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                               max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
                               moment=arcade.PymunkPhysicsEngine.DYNAMIC)
        self.fizika.add_sprite_list(self.walls_list, friction=WALL_FRICTION, collision_type=WALL_COLLISION_TYPE,
                                    body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_draw(self):
        self.clear()

        self.walls_list.draw()

        self.igrok.draw()

    def on_update(self, delta_time: float):
        if self.pravo and not self.levo:
            force = (IGROK_MOVE_GROUND, 0)
            self.fizika.apply_force(self.igrok, force)
            self.fizika.set_friction(self.igrok, 0)
        elif not self.pravo and self.levo:
            force = (-IGROK_MOVE_GROUND, 0)
            self.fizika.apply_force(self.igrok, force)
            self.fizika.set_friction(self.igrok, 0)
        else:
            self.fizika.set_friction(self.igrok, 1)

        self.fizika.step()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.pravo = True
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.levo = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pravo = False
        elif _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.levo = False


win = arcade.Window(W, H)
viev1 = Igra1GlavaViev()
viev1.setup()
win.show_view(viev1)

arcade.run()
