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

GRAVITY = (0, -1250)
DAMPING = 0.9
IGROK_MOVE_GROUND = 10000
MASS_IGROK = 1
FRICTION_IGROK = 0
IGROK_CT = 'player'
IG_MAX_VERTICAL_SPEED = 2000
IG_MAX_HORIZANTAL_SPEED = 350
IGROK_JUMP_FORCE = 40000
WALL_FRICTION = 0.8
WALL_CT = 'wall'


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class Igra1GlavaViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((255, 182, 193, 1))
        self.f = False

        # Переменные для частиц
        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='shederi_igra/ver_shad_tl_ogon.glsl',
                                                    fragment_shader='shederi_igra/frag_shad_tl_ogon.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.igrok = None

        self.vrag_list = None
        self.v_drug_list = None

        self.walls_list = None
        self.platforms_list = None
        self.sprite_list = None

        self.smert_list1 = None
        self.smert_list2 = None

        self.fizika = None

        self.kamera = None

        # Переменные True, либо False
        self.levo = False
        self.pravo = False

        self.s = 0
        self.s1 = 0
        self.s_zoom = 0
        self.s_zoom1 = 0
        self.zoom = False
        self.zoom1 = False

        self.t_main_patch = (':resources:images/tiles/')

    def setup(self):
        self.kamera = arcade.Camera()

        self.smert_list1 = arcade.SpriteList()
        self.smert_list2 = arcade.SpriteList()

        self.sprite_list = arcade.SpriteList()
        self.v_drug_list = arcade.SpriteList()

        self.walls_list = arcade.SpriteList()
        for x in range(-10000, 10000, 128):
            wall = arcade.Sprite(f'{self.t_main_patch}grassMid.png')
            wall.position = x, 64
            self.walls_list.append(wall)
            self.sprite_list.append(wall)

        for x in range(192, 3000, 64):
            wall = arcade.Sprite(f'{self.t_main_patch}grassMid.png', 0.5)
            wall.position = x, 160
            self.walls_list.append(wall)
            self.sprite_list.append(wall)

        for x in range(192, 3000, 64):
            wall = arcade.Sprite(f'{self.t_main_patch}grassMid.png', 0.5)
            wall.position = x, 224
            self.walls_list.append(wall)
            self.sprite_list.append(wall)

        for x in range(-5000, -10, 384):
            wall = arcade.Sprite(f'{self.t_main_patch}grassMid.png')
            wall.position = x, 192
            self.walls_list.append(wall)
            self.sprite_list.append(wall)

        self.vrag_list = arcade.SpriteList()

        self.igrok = pers.BetaMaster(self.vrag_list)

        vrag = pers.Vrag(self.igrok, self.sprite_list, self.vrag_list)
        vrag._position = 500, 400
        self.vrag_list.append(vrag)

        for x in range(700, 1400, 100):
            vrag = pers.Vrag(self.igrok, self.sprite_list, self.vrag_list)
            vrag._position = x, 400
            self.vrag_list.append(vrag)

        for vrag in self.vrag_list:
            vrag.v_drug_list = self.vrag_list

        self.igrok.sprite_list = self.vrag_list

        self.fizika = arcade.PymunkPhysicsEngine(GRAVITY, DAMPING)
        self.fizika.add_sprite(self.igrok, MASS_IGROK, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                               max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
                               moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9, collision_type='player')
        self.fizika.add_sprite_list(self.walls_list, friction=1,
                                    body_type=arcade.PymunkPhysicsEngine.STATIC, collision_type='wall')
        for vrag in self.vrag_list:
            self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=200,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

    def on_draw(self):
        self.kamera.use()
        self.center_kamera_za_igrok()
        self.clear()

        self.smert_list1.draw()
        self.vrag_list.draw()
        self.igrok.draw()
        self.smert_list2.draw()

        self.walls_list.draw()
        for vrag in self.vrag_list:
            vrag.draw()
            vrag.update_animation()

        self.igrok.update_animation()

    def on_update(self, delta_time: float):
        if self.zoom:
            self.s_zoom += 1
            if self.s_zoom > 180:
                self.s_zoom = 0
                self.zoom = False
            if self.zoom:
                if self.s_zoom <= 180:
                    self.kamera.zoom -= 1 / 1800
        if self.zoom1:
            self.s_zoom1 += 1
            if self.s_zoom1 > 180:
                self.s_zoom1 = 0
                self.zoom1 = False
            if self.zoom1:
                if self.s_zoom1 <= 180:
                    self.kamera.zoom += 1 / 1800

        self.igrok.on_update()
        for vrag in self.vrag_list:
            if vrag.smert:
                if random.randint(0, 1) == 1:
                    self.smert_list1.append(vrag)
                elif random.randint(0, 1) == 0:
                    self.smert_list2.append(vrag)
                self.vrag_list.remove(vrag)
                self.fizika.remove_sprite(vrag)
            else:
                vrag.on_update()

                x = vrag.return_force('x')
                y = vrag.return_force('y')

                if y > 0:
                    self.s += 1
                if self.s > 2 and not vrag.is_on_ground:
                    y = 0

                if abs(x) > 0:
                    self.fizika.apply_force(vrag, (x, y))
                    self.fizika.set_friction(vrag, 0.1)
                elif y > 0:
                    self.fizika.apply_force(vrag, (x, y))
                else:
                    self.fizika.set_friction(vrag, 1)

                if y == 0 and self.s >= 2:
                    self.s = 0

        if not self.f:
            if self.pravo and not self.levo:
                force = (IGROK_MOVE_GROUND, 0)
                self.fizika.apply_force(self.igrok, force)
                self.fizika.set_friction(self.igrok, 0.1)
            elif not self.pravo and self.levo:
                force = (-IGROK_MOVE_GROUND, 0)
                self.fizika.apply_force(self.igrok, force)
                self.fizika.set_friction(self.igrok, 0.1)
            else:
                self.fizika.set_friction(self.igrok, 1)

                if self.igrok.molniya.action and self.s1 == 0 and self.igrok.molniya.s >= self.igrok.molniya.timer_for_s:
            self.s1 += 1
            poz = self.igrok.molniya.return_position()
            self.fizika.set_position(self.igrok, poz)

        self.fizika.step()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.L:
            self.igrok.kulak_gaia.udar = True

        if symbol == arcade.key.RCTRL:
            self.igrok.veter_otalk.udar = True

        if symbol == arcade.key.RSHIFT:
            self.igrok.block.block = True

        if symbol == arcade.key.LCTRL:
            self.zoom1 = True
            self.zoom = False

        if symbol == arcade.key.Z:
            self.zoom = True
            self.zoom1 = False

        if symbol == arcade.key.SPACE:
            self.igrok.udar.action = True

        if symbol == arcade.key.NUM_2:
            self.igrok.streliPeruna.action = True

        if symbol == arcade.key.NUM_0:
            self.igrok.molniya.action = True
            self.s1 = 0

        if symbol == arcade.key.NUM_1:
            self.igrok.gnev_Tora.action = True

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.pravo = True
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.levo = True

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            if self.igrok.is_on_ground:
                force = (0, IGROK_JUMP_FORCE)
                self.fizika.apply_force(self.igrok, force)

        if symbol == arcade.key.F:
            self.f = True
            self.fizika.remove_sprite(self.igrok)

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.RSHIFT:
            self.igrok.block.block = False

        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pravo = False
        elif _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.levo = False

        if _symbol == arcade.key.G:
            self.f = False
            self.fizika.add_sprite(self.igrok, MASS_IGROK, FRICTION_IGROK, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
                                   moment=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9, collision_type='player')

    def center_kamera_za_igrok(self, x=False, y=False):
        ekran_center_x = self.igrok.center_x - self.kamera.viewport_width / 3
        ekran_center_y = self.igrok.center_y - self.kamera.viewport_height / 5

        self.kamera.move_to((ekran_center_x, ekran_center_y), 0.1)

        if x:
            return ekran_center_x
        if y:
            return ekran_center_y


win = arcade.Window(W, H)
viev1 = Igra1GlavaViev()
viev1.setup()
win.show_view(viev1)

arcade.run()
