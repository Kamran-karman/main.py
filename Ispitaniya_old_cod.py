import arcade
import arcade.gui
from arcade.experimental import lights
import time
from array import array
from dataclasses import dataclass
import arcade.gl
import random
import math
from threading import Timer

Min_Time = 0.3
Max_Time = 0.8

Min_Time2 = 0.3
Max_Time2 = 0.8

Koor_y = 192
Koor_x = 80
D_Zone = 0.1
#######################
Gravity = 1500
Def_Damping = 1
Player_Damping = 0.7
R_Damping = 1
Pl_Friction = 1
Zem_Friction = 0.6
Plat_Friction = 0.8
Dynamic_Item_Friction = 0.6
R_Mass = 5
Plaeyr_mass = 2
P_Max_Horiz_Speed = 200
P_Max_Vertic_Speed = 1600
P_Move_Ground = 8000
R_Move_Ground = 4000
P_Jump_F = 75000
R_Jump_F = 100000

vib = 0


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class Svet_Vzriva:
    def __init__(self, x, y, lid_layer):
        self.x = x
        self.y = y
        self.lights_layer = lid_layer

    def vzriiiv(self):
        a = lights.Light(self.x, self.y, 350, (32, 32, 32), 'soft')
        def rtim():
            self.lights_layer.add(a)
        timer = Timer(0.25, rtim)
        timer.start()
        def tim():
            self.lights_layer.remove(a)
        timer = Timer(0.35, tim)
        timer.start()

        a1 = lights.Light(self.x, self.y, 250, (150, 40, 0), 'soft')
        def rtim1():
            self.lights_layer.add(a1)
        timer = Timer(0.2, rtim1)
        timer.start()
        def tim1():
            self.lights_layer.remove(a1)
        timer = Timer(0.25, tim1)
        timer.start()

        a2 = lights.Light(self.x, self.y, 150, (225, 125, 0), 'soft')
        def rtim2():
            self.lights_layer.add(a2)
        timer = Timer(0.05, rtim2)
        timer.start()
        def tim2():
            self.lights_layer.remove(a2)
        timer = Timer(0.1, tim2)
        timer.start()

        a3 = lights.Light(self.x, self.y, 100, (200, 0, 0), 'soft')
        def rtim3():
            self.lights_layer.add(a3)
        timer = Timer(0.05, rtim3)
        timer.start()
        def tim3():
            self.lights_layer.remove(a3)
        timer = Timer(0.1, tim3)
        timer.start()

        a4 = lights.Light(self.x, self.y, 50, (255, 255, 255), 'soft')
        self.lights_layer.add(a4)
        def tim4():
            self.lights_layer.remove(a4)
        timer = Timer(0.05, tim4)
        timer.start()

        a5 = lights.Light(self.x, self.y, 200, (150, 150, 150), 'soft')
        def rtim5():
            self.lights_layer.add(a5)
        timer = Timer(0.1, rtim5)
        timer.start()
        def tim5():
            self.lights_layer.remove(a5)
        timer = Timer(0.2, tim5)
        timer.start()

        a6 = lights.Light(self.x, self.y, 150, (28, 28, 28), 'soft')
        def rtim6():
            self.lights_layer.add(a6)
        timer = Timer(0.35, rtim6)
        timer.start()
        def tim6():
            self.lights_layer.remove(a6)
        timer = Timer(0.375, tim6)
        timer.start()

        a7 = lights.Light(self.x, self.y, 200, (24, 12, 0), 'soft')
        def rtim7():
            self.lights_layer.add(a7)
        timer = Timer(0.375, rtim7)
        timer.start()
        def tim7():
            self.lights_layer.remove(a7)
        timer = Timer(0.4, tim7)
        timer.start()

        a8 = lights.Light(self.x, self.y, 300, (20, 20, 0), 'soft')
        def rtim8():
            self.lights_layer.add(a8)
        timer = Timer(0.4, rtim8)
        timer.start()
        def tim8():
            self.lights_layer.remove(a8)
        timer = Timer(0.425, tim8)
        timer.start()

        a9 = lights.Light(self.x, self.y, 400, (16, 0, 0), 'soft')
        def rtim9():
            self.lights_layer.add(a9)
        timer = Timer(0.425, rtim9)
        timer.start()
        def tim9():
            self.lights_layer.remove(a9)
        timer = Timer(0.45, tim9)
        timer.start()


class Player(arcade.Sprite):
    def __init__(self, a):
        super().__init__()
        self.center_x = Koor_x
        self.center_y = Koor_y
        self.scale = 1
        self.storona = 1

        self.a = a

        self.c_walk_tex = 0

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")
        main_patch1 = (":resources:images/animated_characters/female_adventurer/femaleAdventurer")
        main_patch2 = (":resources:images/animated_characters/male_person/malePerson")
        main_patch3 = (":resources:images/animated_characters/female_person/femalePerson")

        self.idle_tex = load_texture_pair(f'{main_patch}_idle.png')
        self.jump_tex = load_texture_pair(f'{main_patch}_jump.png')
        self.fall_tex = load_texture_pair(f'{main_patch}_fall.png')

        self.walk_t = []
        for i in range(8):
            tex = load_texture_pair(f":resources:images/animated_characters/male_adventurer/maleAdventurer_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.idle_tex_fa = load_texture_pair(f'{main_patch1}_idle.png')
        self.jump_tex_fa = load_texture_pair(f'{main_patch1}_jump.png')
        self.fall_tex_fa = load_texture_pair(f'{main_patch1}_fall.png')

        self.walk_t_fa = []
        for i in range(8):
            tex = load_texture_pair(f"{main_patch1}_walk{i}.png")
            self.walk_t_fa.append(tex)
        self.texture = self.idle_tex_fa[0]

        self.idle_tex_mp = load_texture_pair(f'{main_patch2}_idle.png')
        self.jump_tex_mp = load_texture_pair(f'{main_patch2}_jump.png')
        self.fall_tex_mp = load_texture_pair(f'{main_patch2}_fall.png')

        self.walk_t_mp = []
        for i in range(8):
            tex = load_texture_pair(f"{main_patch2}_walk{i}.png")
            self.walk_t_mp.append(tex)
        self.texture = self.idle_tex_mp[0]

        self.idle_tex_fp = load_texture_pair(f'{main_patch3}_idle.png')
        self.jump_tex_fp = load_texture_pair(f'{main_patch3}_jump.png')
        self.fall_tex_fp = load_texture_pair(f'{main_patch3}_fall.png')

        self.walk_t_fp = []
        for i in range(8):
            tex = load_texture_pair(f"{main_patch3}_walk{i}.png")
            self.walk_t_fp.append(tex)
        self.texture = self.idle_tex_fp[0]

        self.hit_box = self.texture.hit_box_points
        self.is_on_ground = True
        self.x_odometr = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        global vib
        if self.a == 0:
            if dx < -D_Zone and self.storona == 0:
                self.storona = 1
            elif dx > D_Zone and self.storona == 1:
                self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            self.x_odometr += dx

            if not self.is_on_ground:
                if dy > D_Zone:
                    self.texture = self.jump_tex[self.storona]
                    return
                elif dy < -D_Zone:
                    self.texture = self.fall_tex[self.storona]
                    return

            if abs(dx) < D_Zone:
                self.texture = self.idle_tex[self.storona]
                return

            if abs(self.x_odometr) > 10:
                self.x_odometr = 0
                self.c_walk_tex += 1
                if self.c_walk_tex > 7:
                    self.c_walk_tex = 0
                self.texture = self.walk_t[self.c_walk_tex][self.storona]
        elif self.a == 1:
            if dx < -D_Zone and self.storona == 0:
                self.storona = 1
            elif dx > D_Zone and self.storona == 1:
                self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            self.x_odometr += dx

            if not self.is_on_ground:
                if dy > D_Zone:
                    self.texture = self.jump_tex_fa[self.storona]
                    return
                elif dy < -D_Zone:
                    self.texture = self.fall_tex_fa[self.storona]
                    return

            if abs(dx) < D_Zone:
                self.texture = self.idle_tex_fa[self.storona]
                return

            if abs(self.x_odometr) > 10:
                self.x_odometr = 0
                self.c_walk_tex += 1
                if self.c_walk_tex > 7:
                    self.c_walk_tex = 0
                self.texture = self.walk_t_fa[self.c_walk_tex][self.storona]
        elif self.a == 2:
            if dx < -D_Zone and self.storona == 0:
                self.storona = 1
            elif dx > D_Zone and self.storona == 1:
                self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            self.x_odometr += dx

            if not self.is_on_ground:
                if dy > D_Zone:
                    self.texture = self.jump_tex_mp[self.storona]
                    return
                elif dy < -D_Zone:
                    self.texture = self.fall_tex_mp[self.storona]
                    return

            if abs(dx) < D_Zone:
                self.texture = self.idle_tex_mp[self.storona]
                return

            if abs(self.x_odometr) > 10:
                self.x_odometr = 0
                self.c_walk_tex += 1
                if self.c_walk_tex > 7:
                    self.c_walk_tex = 0
                self.texture = self.walk_t_mp[self.c_walk_tex][self.storona]
        elif self.a == 3:
            if dx < -D_Zone and self.storona == 0:
                self.storona = 1
            elif dx > D_Zone and self.storona == 1:
                self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            self.x_odometr += dx

            if not self.is_on_ground:
                if dy > D_Zone:
                    self.texture = self.jump_tex_fp[self.storona]
                    return
                elif dy < -D_Zone:
                    self.texture = self.fall_tex_fp[self.storona]
                    return

            if abs(dx) < D_Zone:
                self.texture = self.idle_tex_fp[self.storona]
                return

            if abs(self.x_odometr) > 10:
                self.x_odometr = 0
                self.c_walk_tex += 1
                if self.c_walk_tex > 7:
                    self.c_walk_tex = 0
                self.texture = self.walk_t_fp[self.c_walk_tex][self.storona]


class Vrag(arcade.Sprite):
    def __init__(self, scale):
        super().__init__()
        self.storona = 1
        self.c_walk_tex = 0
        self.scale = scale

        main_patch = (":resources:images/animated_characters/robot/robot")

        self.idle_tex = load_texture_pair(f'{main_patch}_idle.png')
        self.jump_tex = load_texture_pair(f'{main_patch}_jump.png')
        self.fall_tex = load_texture_pair(f'{main_patch}_fall.png')

        self.walk_t = []
        for i in range(8):
            tex = load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.hit_box = self.texture.hit_box_points
        self.is_on_ground = True
        self.x_odometr = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_Zone and self.storona == 0:
            self.storona = 1
        elif dx > D_Zone and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > D_Zone:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < -D_Zone:
                self.texture = self.fall_tex[self.storona]
                return

        if abs(dx) < D_Zone:
            self.texture = self.idle_tex[self.storona]
            return

        if abs(self.x_odometr) > 10:
            self.x_odometr = 0
            self.c_walk_tex += 1
            if self.c_walk_tex > 7:
                self.c_walk_tex = 0
            self.texture = self.walk_t[self.c_walk_tex][self.storona]


class GameViev(arcade.View):
    def __init__(self):
        super().__init__()
        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='C:/Users/user/Desktop/Igra/shederi/ver_shad_v1.glsl',
                                                    fragment_shader='C:/Users/user/Desktop/Igra/shederi/frag_shad.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.chasti_list2 = []
        self.program2 = self.window.ctx.load_program(vertex_shader='C:/Users/user/Desktop/Igra/shederi/ver_shad_v2.glsl',
                                                     fragment_shader='C:/Users/user/Desktop/Igra/shederi/frag_shad2.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.player = None
        self.phi = None
        self.plat_list = None
        self.vrag_list = None
        self.stena_list = None
        self.zem_list = None
        self.invise_plat = None
        self.vrag = None
        self.vrag_jump1 = None
        self.vrag_jump2 = None
        self.vrag_jump3 = None
        self.bomb_list = None
        self.sound_jump = None
        self.sound_jump1 = None
        self.sound_bomb = None
        self.sound_bomb1 = None
        self.sound_fall = None
        self.sound_fall1 = None
        self.music = None
        self.music_play = None
        self.meneger = None
        self.bomb_load = None
        self.serd_load = None
        self.v_box = None
        self.v_box1 = None
        self.meng = None
        self.v_box2 = None
        self.serd_kol = None
        self.bomb_kol_info = None
        self.lights_layer = None
        self.player_lights0 = None
        self.player_lights = None
        self.vzriv_lig = None
        self.vrag_lidhts = None
        self.vrag_lidhts1 = None
        self.vrag_lidhts2 = None
        self.vrag_lidhts3 = None
        self.vrag_lidhts4 = None
        self.vrag_lidhts5 = None
        self.fon_r = None
        self.lights_layer1 = None
        self.player_lights1 = None
        self.player_lights2 = None

        self.v = None

        self.schetchik = 0
        self.kd = 90
        global vib
        if vib == 0:
            self.hp = 3
        elif vib == 1 or vib == 3:
            self.hp = 1
        elif vib == 2:
            self.hp = 5
        self.bomb_kol = 0

        self.left_pressed = False
        self.right_pressed = False
        self.da_net1 = False
        self.g = 0
        self.gg = False

    def setup(self):
        self.meng = arcade.gui.UIManager()
        self.meng.enable()
        self.v_box2 = arcade.gui.UIBoxLayout()
        self.meng.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y='center', child=self.v_box2))

        text = arcade.gui.UITextArea(text="    Вы победили!!!\n     Это победа!!!", width=700, height=180, font_size=64,
                                     style='Impact')
        self.v_box2.add(text.with_space_around(bottom=60))

        kn1 = arcade.gui.UIFlatButton(text='Заново', width=400, height=80)
        self.v_box2.add(kn1.with_space_around(bottom=40))

        kn2 = arcade.gui.UIFlatButton(text='Выбор персонажа', width=400, height=80)
        self.v_box2.add(kn2.with_space_around(bottom=40))

        kn3 = arcade.gui.UIFlatButton(text='Выйти из игры', width=400, height=80)
        self.v_box2.add(kn3.with_space_around(bottom=100))

        def click_kn1(event):
            gem = GameViev()
            gem.setup()
            self.window.show_view(gem)
            del gem
        kn1.on_click = click_kn1

        def click_kn2(event):
            vi = Vibor()
            self.window.show_view(vi)
            del vi
        kn2.on_click = click_kn2

        def click_kn3(event):
            arcade.close_window()
        kn3.on_click = click_kn3

        self.lights_layer = lights.LightLayer(1600, 900)
        self.lights_layer.set_background_color(arcade.color.BURGUNDY)

        self.lights_layer1 = lights.LightLayer(1600, 900)
        self.player_lights = lights.Light(0, 0, 100, (100, 100, 100), 'soft')
        self.player_lights2 = lights.Light(0, 0, 100, (100, 100, 100), 'soft')

        global vib
        if vib == 0:
            self.player_lights0 = lights.Light(0, 0, 200, (200, 200, 200), 'soft')
            self.player_lights1 = lights.Light(0, 0, 200, (200, 200, 200), 'soft')
            k = lights.Light(400, 680, 1800, (30, 30, 30), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1300, (100, 100, 100), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1100, (100, 100, 100), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 500, (125, 125, 125), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 250, (150, 150, 150), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 100, (200, 200, 200), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 50, (255, 255, 255), 'soft')
            self.lights_layer1.add(k)
        elif vib == 1:
            self.player_lights0 = lights.Light(0, 0, 200, (150, 200, 255), 'soft')
            self.player_lights1 = lights.Light(0, 0, 200, (150, 200, 255), 'soft')
            k = lights.Light(400, 680, 1800, (30, 30, 30), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1300, (100, 100, 100), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1100, (50, 100, 155), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 500, (125, 125, 125), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 250, (150, 150, 150), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 100, (150, 200, 255), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 50, (255, 255, 255), 'soft')
            self.lights_layer1.add(k)
        elif vib == 2:
            self.player_lights0 = lights.Light(0, 0, 200, (255, 200, 0), 'soft')
            self.player_lights1 = lights.Light(0, 0, 200, (255, 200, 0), 'soft')
            k = lights.Light(400, 680, 1800, (30, 30, 30), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1300, (100, 100, 100), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1100, (150, 100, 0), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 500, (125, 125, 125), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 250, (150, 150, 150), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 100, (250, 200, 0), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 50, (255, 255, 255), 'soft')
            self.lights_layer1.add(k)
        elif vib == 3:
            self.player_lights0 = lights.Light(0, 0, 200, (255, 140, 0), 'soft')
            self.player_lights1 = lights.Light(0, 0, 200, (255, 140, 0), 'soft')
            k = lights.Light(400, 680, 1800, (30, 30, 30), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1300, (100, 100, 100), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 1100, (155, 40, 0), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 500, (125, 125, 125), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 250, (150, 150, 150), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 100, (255, 140, 0), 'soft')
            self.lights_layer1.add(k)
            k = lights.Light(400, 400, 50, (255, 255, 255), 'soft')
            self.lights_layer1.add(k)

        self.vrag_lidhts = lights.Light(392, 160, 25, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts)

        self.vrag_lidhts1 = lights.Light(368, 443, 20, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts1)

        self.vrag_lidhts2 = lights.Light(1520, 185, 42, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts2)

        self.vrag_lidhts3 = lights.Light(888, 155, 25, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts3)

        self.vrag_lidhts4 = lights.Light(1264, 155, 25, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts4)

        self.vrag_lidhts5 = lights.Light(1392, 155, 25, (75, 0, 0), 'soft')
        self.lights_layer.add(self.vrag_lidhts5)

        self.fon_r = arcade.SpriteList()
        for i in range(-100, 1700, 100):
            for q in range(-100, 1000, 100):
                e = arcade.Sprite("C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/images/krasn.jpg")
                e.position = i, q
                self.fon_r.append(e)

        self.music = arcade.load_sound('C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/music/Naruto_OST.mp3')
        self.music_play = arcade.play_sound(self.music, 0.2, looping=True)

        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.meneger.add(arcade.gui.UIAnchorWidget(anchor_x='right', anchor_y='top', child=self.v_box))
        self.v_box1 = arcade.gui.UIBoxLayout()
        self.meneger.add(arcade.gui.UIAnchorWidget(anchor_x='right', anchor_y='top', child=self.v_box1))

        self.bomb_load = arcade.load_texture(':resources:images/tiles/bomb.png')
        bomb_text = arcade.gui.UITextureButton(texture=self.bomb_load, scale=0.25)
        self.v_box.add(bomb_text.with_space_around(top=20, right=100))
        self.bomb_kol_info = arcade.gui.UITextArea(text=f'X {self.bomb_kol}', width=50, height=25, font_size=15,
                                                   font_name='Impact')
        self.v_box1.add(self.bomb_kol_info.with_space_around(top=22.5, bottom=30, right=45))

        if vib == 0:
            self.serd_load = arcade.load_texture(':resources:images/'
                                                 'animated_characters/male_adventurer/maleAdventurer_idle.png')
        if vib == 1:
            self.serd_load = arcade.load_texture(':resources:images/animated_characters/female_adventurer/'
                                                 'femaleAdventurer_idle.png')
        if vib == 2:
            self.serd_load = arcade.load_texture(':resources:images/animated_characters/male_person/malePerson_idle.'
                                                 'png')
        if vib == 3:
            self.serd_load = arcade.load_texture(':resources:images/animated_characters/female_person/'
                                                 'femalePerson_idle.png')
        bomb_text = arcade.gui.UITextureButton(texture=self.serd_load, scale=0.5)
        self.v_box.add(bomb_text.with_space_around(right=100))
        self.serd_kol = arcade.gui.UITextArea(text=f'X {self.hp}', width=50, height=25, font_size=15,
                                              font_name='Impact')
        self.v_box1.add(self.serd_kol.with_space_around(right=45))

        main = ':resources:sounds/'
        self.sound_jump = arcade.load_sound(f"{main}jump5.wav")
        self.sound_bomb = arcade.load_sound(f"{main}hit2.wav")
        self.sound_fall = arcade.load_sound(f'{main}fall1.wav')

        if vib == 0:
            self.player = Player(0)
            self.v = 0
        elif vib == 1:
            self.player = Player(1)
            self.v = 1
        elif vib == 2:
            self.player = Player(2)
            self.v = 2
        elif vib == 3:
            self.player = Player(3)
            self.v = 3

        self.bomb_list = arcade.SpriteList()
        for i in range(304, 433, 64):
            a = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
            a.center_x = i
            if i == 368:
                a.center_y = 486
            else:
                a.center_y = 440
            self.bomb_list.append(a)
        a = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
        a.center_x = 202
        a.center_y = 216
        self.bomb_list.append(a)
        for i in range(542, 798, 128):
            a = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
            a.center_x = i
            a.center_y = 152
            self.bomb_list.append(a)
        s = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
        s.center_x = 800
        s.center_y = 280
        q = 64
        self.bomb_list.append(s)
        for i in range(992, 1184, 96):
            a = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
            a.center_x = i
            a.center_y = 152
            self.bomb_list.append(a)
            q = 64
        for i in range(1200, 1457, 128):
            a = arcade.Sprite(':resources:images/tiles/bomb.png', 0.25)
            a.center_x = i
            if i == 1200:
                a.center_y = 248
            else:
                a.center_y = 248 + q
                q += 64
            self.bomb_list.append(a)

        self.vrag_list = arcade.SpriteList()
        a = Vrag(0.5)
        a.center_x = 368
        a.center_y = 448
        self.vrag_list.append(a)
        q = Vrag(1.2)
        q.center_x = 1520
        q.center_y = 205
        self.vrag_list.append(q)

        self.vrag_jump1 = Vrag(0.5)
        self.vrag_jump1.center_y = 170
        self.vrag_jump1.center_x = 888

        self.vrag_jump2 = Vrag(0.5)
        self.vrag_jump2.center_y = 170
        self.vrag_jump2.center_x = 1264

        self.vrag_jump3 = Vrag(0.5)
        self.vrag_jump3.center_y = 170
        self.vrag_jump3.center_x = 1392

        self.stena_list = arcade.SpriteList()
        for i in range(128, 850, 64):
            a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
            a.center_x = 0
            a.center_y = i
            self.stena_list.append(a)
        for i in range(128, 850, 64):
            a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
            a.center_x = 1600
            a.center_y = i
            self.stena_list.append(a)

        self.vrag = Vrag(0.65)
        self.vrag.center_y = 170
        self.vrag.center_x = 392

        self.invise_plat = arcade.Sprite(':resources:images/tiles/boxCrate_single.png', 0.25)
        self.invise_plat.center_y = 304
        self.invise_plat.center_x = 600

        self.zem_list = arcade.SpriteList()
        for i in range(0, 1664, 64):
            a = arcade.Sprite(':resources:images/tiles/dirtMid.png')
            a.center_x = i
            a.center_y = 64
            self.zem_list.append(a)

        self.plat_list = arcade.SpriteList()
        for i in range(10):
            if i == 0:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 202
                a.center_y = 160
            elif i == 1:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 768
                a.center_y = 160
            elif i == 2:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 832
                a.center_y = 160
            elif i == 3:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 800
                a.center_y = 224
            elif i == 4:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 432
                a.center_y = 384
            elif i == 5:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 368
                a.center_y = 384
            elif i == 6:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 304
                a.center_y = 384
            elif i == 7:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 1200
                a.center_y = 192
            elif i == 8:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 1328
                a.center_y = 256
            else:
                a = arcade.Sprite(':resources:images/tiles/boxCrate.png', 0.5)
                a.center_x = 1456
                a.center_y = 320
            self.plat_list.append(a)

        self.phi = arcade.PymunkPhysicsEngine(gravity=(0, -Gravity), damping=Def_Damping)
        if self.v == 0:
            self.phi.add_sprite(self.player, mass=Plaeyr_mass + 0.1, friction=Pl_Friction, damping=Player_Damping,
                                max_vertical_velocity=P_Max_Vertic_Speed,
                                max_horizontal_velocity=P_Max_Horiz_Speed + 20, collision_type='player',
                                moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        if self.v == 1:
            self.phi.add_sprite(self.player, mass=Plaeyr_mass - 0.2, friction=Pl_Friction, damping=Player_Damping,
                                max_vertical_velocity=P_Max_Vertic_Speed + 20,
                                max_horizontal_velocity=P_Max_Horiz_Speed, collision_type='player',
                                moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        if self.v == 2:
            self.phi.add_sprite(self.player, mass=Plaeyr_mass + 0.15, friction=Pl_Friction, damping=Player_Damping,
                                max_vertical_velocity=P_Max_Vertic_Speed - 5,
                                max_horizontal_velocity=P_Max_Horiz_Speed, collision_type='player',
                                moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        if self.v == 3:
            self.phi.add_sprite(self.player, mass=Plaeyr_mass - 0.2, friction=Pl_Friction, damping=Player_Damping,
                                max_vertical_velocity=P_Max_Vertic_Speed - 5,
                                max_horizontal_velocity=P_Max_Horiz_Speed - 15, collision_type='player',
                                moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        self.phi.add_sprite_list(self.zem_list, friction=Zem_Friction, collision_type='wall',
                                 body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite_list(self.plat_list, friction=Plat_Friction, collision_type='wall',
                                 body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite(self.invise_plat, friction=Plat_Friction, collision_type='wall',
                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite_list(self.stena_list, friction=Plat_Friction, collision_type='wall',
                                 body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite_list(self.vrag_list, friction=Plat_Friction, collision_type='platforms',
                                 body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite(self.vrag, friction=Plat_Friction, collision_type='platforms',
                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.phi.add_sprite(self.vrag_jump1, friction=0, collision_type='platforms', damping=R_Damping,
                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC, mass=R_Mass, max_horizontal_velocity=0,
                            moment=arcade.PymunkPhysicsEngine.MOMENT_INF, max_vertical_velocity=3200)
        self.phi.add_sprite(self.vrag_jump2, friction=0, collision_type='wall', damping=R_Damping,
                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC, mass=R_Mass, max_horizontal_velocity=0,
                            moment=arcade.PymunkPhysicsEngine.MOMENT_INF, max_vertical_velocity=3200)
        self.phi.add_sprite(self.vrag_jump3, friction=0, collision_type='wall', damping=R_Damping,
                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC, mass=R_Mass, max_horizontal_velocity=0,
                            moment=arcade.PymunkPhysicsEngine.MOMENT_INF, max_vertical_velocity=3200)

    def vzriv(self, x, y):
        def gen_initional_data(initional_x, initional_y):
            for i in range(200):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0, 0.9)
                dx = math.sin(angle) * speed / 1.5
                dy = math.cos(angle) * speed / 1.5
                red = random.uniform(0.5, 1)
                green = random.uniform(0.1, red)
                blue = 0
                fade_rate = random.uniform(1 / Max_Time, 1 / Min_Time)
                yield initional_x
                yield initional_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        x2 = x / self.window.width * 2 - 1
        y2 = y / self.window.height * 2 - 1

        initional_data = gen_initional_data(x2, y2)

        buffer = self.window.ctx.buffer(data=array('f', initional_data))

        buf_descript = arcade.gl.BufferDescription(buffer, '2f 2f 3f f', ['in_pos', 'in_vel', 'in_color',
                                                                          'in_fade_rate'])
        vao = self.window.ctx.geometry([buf_descript])
        chasti = Chasti(buffer, vao, time.time())
        self.chasti_list.append(chasti)

    def krov(self, x, y, storona):
        if storona == 0:
            storona = -1
        elif storona == 1:
            storona = 1

        def gen_initional_data2(initional_x, initional_y):
            for i in range(50):
                angle = random.uniform(0, storona * math.pi)
                speed = random.uniform(0, 0.9)
                dx = math.sin(angle) * speed / 1.5
                dy = math.cos(angle) * speed / 1.5
                red = random.uniform(0.1, 1)
                green = 0
                blue = 0
                fade_rate = random.uniform(1 / Max_Time2, 1 / Min_Time2)
                yield initional_x
                yield initional_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        x2 = x / self.window.width * 2 - 1
        y2 = y / self.window.height * 2 - 1

        initional_data = gen_initional_data2(x2, y2)

        buffer = self.window.ctx.buffer(data=array('f', initional_data))

        buf_descript = arcade.gl.BufferDescription(buffer, '2f 2f 3f f', ['in_pos', 'in_vel', 'in_color',
                                                                          'in_fade_rate'])
        vao = self.window.ctx.geometry([buf_descript])
        chasti = Chasti(buffer, vao, time.time())
        self.chasti_list2.append(chasti)

    def on_update(self, delta_time: float):
        self.g += 1

        self.player_lights0.position = self.player.position
        self.player_lights1.position = self.player.position
        self.player_lights.position = self.player.position
        self.player_lights2.position = self.player.position

        if self.left_pressed and not self.right_pressed:
            if vib == 0:
                force = (-P_Move_Ground - 1000, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
            if vib == 1 or vib == 2:
                force = (-P_Move_Ground, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
            if vib == 3:
                force = (-P_Move_Ground + 500, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
        elif not self.left_pressed and self.right_pressed:
            if vib == 0:
                force = (P_Move_Ground + 1000, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
            if vib == 1 or vib == 2:
                force = (P_Move_Ground, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
            if vib == 3:
                force = (P_Move_Ground - 500, 0)
                self.phi.apply_force(self.player, force)
                self.phi.set_friction(self.player, 0)
        else:
            self.phi.set_friction(self.player, 1)

        if self.bomb_kol < 12:
            if self.vrag_jump1.is_on_ground:
                force = (0, R_Jump_F + 10000)
                self.phi.apply_force(self.vrag_jump1, force)
            self.vrag_lidhts3.position = self.vrag_jump1.position
            if self.vrag_jump2.is_on_ground:
                force = (0, R_Jump_F + 75000)
                self.phi.apply_force(self.vrag_jump2, force)
            self.vrag_lidhts4.position = self.vrag_jump2.position
            if self.vrag_jump3.is_on_ground:
                force = (0, R_Jump_F + 75000)
                self.phi.apply_force(self.vrag_jump3, force)
            self.vrag_lidhts5.position = self.vrag_jump3.position
            colis = arcade.check_for_collision_with_list(self.player, self.vrag_list)
            if arcade.check_for_collision(self.player, self.vrag) or colis or arcade.check_for_collision(self.player,
                                          self.vrag_jump1) or arcade.check_for_collision(
                self.player, self.vrag_jump2) or \
                    arcade.check_for_collision(self.player, self.vrag_jump3):
                if self.kd >= 90:
                    self.hp -= 1
                    self.serd_kol.text = f'X {self.hp}'
                    self.kd = 0
                    if self.player.storona == 0:
                        st = self.player.right
                    else:
                        st = self.player.left
                    self.krov(st, self.player.center_y, self.player.storona)
        else:
            if not self.da_net1:
                self.phi.remove_sprite(self.vrag)
                self.phi.remove_sprite(self.vrag_jump3)
                self.phi.remove_sprite(self.vrag_jump2)
                self.phi.remove_sprite(self.vrag_jump1)
                self.phi.remove_sprite(self.vrag_list[0])
                self.phi.remove_sprite(self.vrag_list[1])
                self.da_net1 = True

        for i in self.bomb_list:
            if arcade.check_for_collision(self.player, i):
                sv_vzr = Svet_Vzriva(i.center_x, i.center_y, self.lights_layer)
                sv_vzr.vzriiiv()
                self.sound_bomb1 = arcade.play_sound(self.sound_bomb, volume=0.25)
                self.vzriv(i.center_x, i.center_y)
                self.bomb_kol += 1
                self.bomb_kol_info.text = f'X {self.bomb_kol}'
                self.bomb_list.remove(i)

        self.kd += 1
        self.schetchik += 1

        if self.hp < 1:
            arcade.stop_sound(self.music_play)

        if self.bomb_kol >= 12:
            arcade.close_window()

        temp_list2 = self.chasti_list2.copy()
        for chasti in temp_list2:
            if time.time() - chasti.start_time > Max_Time2:
                self.chasti_list2.remove(chasti)

        temp_list = self.chasti_list.copy()
        for chasti in temp_list:
            if time.time() - chasti.start_time > Max_Time:
                self.chasti_list.remove(chasti)

        self.phi.step()

    def on_draw(self):
        self.clear()

        if self.bomb_kol < 12:
            with self.lights_layer:
                self.fon_r.draw()

                self.stena_list.draw()
                self.vrag.draw()
                self.bomb_list.draw()
                self.stena_list.draw()
                self.plat_list.draw()

                self.vrag_jump1.draw()
                self.vrag_jump1.draw()
                self.vrag_jump2.draw()
                self.vrag_jump3.draw()
                self.vrag_list.draw()

                if self.kd >= 90:
                    self.player.draw()
                elif self.kd <= 6:
                    pass
                elif self.kd > 6 and self.kd <= 12:
                    self.player.draw()
                elif self.kd > 12 and self.kd <= 18:
                    pass
                elif self.kd > 18 and self.kd <= 24:
                    self.player.draw()
                elif self.kd > 24 and self.kd <= 30:
                    pass
                elif self.kd > 30 and self.kd <= 36:
                    self.player.draw()
                elif self.kd > 36 and self.kd <= 42:
                    pass
                elif self.kd > 42 and self.kd <= 48:
                    self.player.draw()
                elif self.kd > 48 and self.kd <= 54:
                    pass
                elif self.kd > 54 and self.kd <= 60:
                    self.player.draw()
                elif self.kd > 60 and self.kd <= 66:
                    pass
                elif self.kd > 66 and self.kd <= 72:
                    self.player.draw()
                elif self.kd > 72 and self.kd <= 78:
                    pass
                elif self.kd > 78 and self.kd <= 84:
                    self.player.draw()
                elif self.kd > 84 and self.kd <= 90:
                    pass

                self.window.ctx.point_size = 7 * self.window.get_pixel_ratio()

                for chasti in self.chasti_list2:
                    self.program2['time'] = time.time() - chasti.start_time
                    chasti.vao.render(self.program2, mode=self.window.ctx.POINTS)

                for chasti in self.chasti_list:
                    self.program['time'] = time.time() - chasti.start_time
                    chasti.vao.render(self.program, mode=self.window.ctx.POINTS)

                self.zem_list.draw()
            self.lights_layer.draw(ambient_color=(10, 0, 0))

        if self.schetchik < 300:
            arcade.draw_text('Нажмите ПРОБЕЛ, чтобы включить фонарик', 1580, 20, (240, 240, 240), 23, bold=True,
                             anchor_x='right')

        if self.hp < 1:
            pr = Porazhenie()
            self.window.show_view(pr)
            del pr

        if self.bomb_kol >= 12:
            with self.lights_layer1:
                self.fon_r.draw()

                self.stena_list.draw()
                self.bomb_list.draw()
                self.stena_list.draw()
                self.plat_list.draw()

                self.player.draw()

                self.zem_list.draw()
            self.lights_layer1.draw(ambient_color=(10, 10, 10))

            self.meng.draw()

        self.meneger.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.phi.remove_sprite(self.player)
            self.player.center_y = 600
            if self.v == 0:
                self.phi.add_sprite(self.player, mass=Plaeyr_mass + 0.1, friction=Pl_Friction, damping=Player_Damping,
                                    max_vertical_velocity=P_Max_Vertic_Speed,
                                    max_horizontal_velocity=P_Max_Horiz_Speed + 20, collision_type='player',
                                    moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
            if self.v == 1:
                self.phi.add_sprite(self.player, mass=Plaeyr_mass - 0.2, friction=Pl_Friction, damping=Player_Damping,
                                    max_vertical_velocity=P_Max_Vertic_Speed + 20,
                                    max_horizontal_velocity=P_Max_Horiz_Speed, collision_type='player',
                                    moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
            if self.v == 2:
                self.phi.add_sprite(self.player, mass=Plaeyr_mass + 0.15, friction=Pl_Friction, damping=Player_Damping,
                                    max_vertical_velocity=P_Max_Vertic_Speed - 5,
                                    max_horizontal_velocity=P_Max_Horiz_Speed, collision_type='player',
                                    moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
            if self.v == 3:
                self.phi.add_sprite(self.player, mass=Plaeyr_mass - 0.2, friction=Pl_Friction, damping=Player_Damping,
                                    max_vertical_velocity=P_Max_Vertic_Speed - 5,
                                    max_horizontal_velocity=P_Max_Horiz_Speed - 15, collision_type='player',
                                    moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.left_pressed = True

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            if self.player.is_on_ground:
                if vib == 0:
                    force = (0, P_Jump_F)
                    self.phi.apply_force(self.player, force)
                    self.sound_jump1 = arcade.play_sound(self.sound_jump, volume=0.2)
                if vib == 1:
                    force = (0, P_Jump_F + 5000)
                    self.phi.apply_force(self.player, force)
                    self.sound_jump1 = arcade.play_sound(self.sound_jump, volume=0.2)
                if vib == 2 or vib == 3:
                    force = (0, P_Jump_F - 1500)
                    self.phi.apply_force(self.player, force)
                    self.sound_jump1 = arcade.play_sound(self.sound_jump, volume=0.2)

        if symbol == arcade.key.SPACE:
            if self.player_lights0 in self.lights_layer:
                self.lights_layer.remove(self.player_lights0)
                self.lights_layer1.remove(self.player_lights1)
                self.lights_layer.remove(self.player_lights)
                self.lights_layer1.remove(self.player_lights2)
            else:
                self.lights_layer.add(self.player_lights0)
                self.lights_layer1.add(self.player_lights1)
                self.lights_layer.add(self.player_lights)
                self.lights_layer1.add(self.player_lights2)

        if self.bomb_kol >= 12:
            if symbol == arcade.key.ESCAPE:
                arcade.close_window()
            if symbol == arcade.key.ENTER:
                gem = GameViev()
                gem.setup()
                self.window.show_view(gem)
                del gem
        else:
            if symbol == arcade.key.ESCAPE:
                paus = Paus(self)
                self.window.show_view(paus)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.gg = False
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.left_pressed = False


class GlavMenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.meneger = None
        self.v_box = None
        self.lig_layer = None
        self.kra_lig = None
        self.bel_lig = None
        self.fon_ch = None

    def on_show_view(self):
        self.lig_layer = lights.LightLayer(1600, 900)
        self.lig_layer.set_background_color(arcade.color.WHITE)

        self.bel_lig = lights.Light(800, 350, 250, (255, 255, 255), 'soft')
        self.lig_layer.add(self.bel_lig)

        self.kra_lig = lights.Light(800, 900, 500, (255, 0, 0), 'soft')
        self.lig_layer.add(self.kra_lig)

        self.fon_ch = arcade.SpriteList()
        for i in range(-100, 1701, 100):
            for q in range(-100, 1001, 100):
                e = arcade.Sprite("C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/images/bel.jpg")
                e.position = i, q
                self.fon_ch.append(e)

        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()

        self.v_box = arcade.gui.UIBoxLayout()
        self.meneger.add(arcade.gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.v_box))

        Zag = arcade.gui.UITextArea(text="  Засада роботов", width=660, height=120, font_size=64,
                                    font_name='Impact', text_color=(200, 10, 10))
        self.v_box.add(Zag.with_space_around(bottom=160))

        nach = arcade.gui.UIFlatButton(text='Начать играть', width=400, height=80)
        self.v_box.add(nach.with_space_around(bottom=40))
        vit = arcade.gui.UIFlatButton(text='Выйти из игры', width=400, height=80)
        self.v_box.add(vit.with_space_around(bottom=100))

        def on_click_nach(event):
            game = Vibor()
            self.window.show_view(game)
            del game
        nach.on_click = on_click_nach

        def on_click_vit(event):
            arcade.close_window()
        vit.on_click = on_click_vit

    def on_draw(self):
        with self.lig_layer:
            self.fon_ch.draw()
        self.lig_layer.draw(ambient_color=(0, 0, 0))

        self.meneger.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game = Vibor()
            self.window.show_view(game)
            del game
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


class Vibor(arcade.View):
    def __init__(self):
        super().__init__()

        self.meneger = None
        self.fem_pers = None
        self.fem_adv = None
        self.m_pers = None
        self.m_adv = None
        self.v_box = None
        self.lig_layer0 = None
        self.lig_layer1 = None
        self.lig_layer2 = None
        self.lig_layer3 = None
        self.lig_01 = None
        self.lig_02 = None
        self.lig_03 = None
        self.lig_11 = None
        self.lig_12 = None
        self.lig_13 = None
        self.lig_21 = None
        self.lig_22 = None
        self.lig_23 = None
        self.lig_31 = None
        self.lig_32 = None
        self.lig_33 = None
        self.fon_0 = None

        self.kol12 = 0

    def on_show_view(self):
        self.lig_layer0 = lights.LightLayer(1600, 800)
        self.lig_01 = lights.Light(800, 590, 100, (200, 200, 200), 'soft')
        self.lig_layer0.add(self.lig_01)
        z = lights.Light(800, 590, 200, (200, 200, 200), 'soft')
        self.lig_layer0.add(z)
        self.lig_02 = lights.Light(550, 450, 100, (255, 140, 0), 'soft')
        self.lig_layer0.add(self.lig_02)
        self.lig_03 = lights.Light(1050, 450, 100, (150, 200, 255), 'soft')
        self.lig_layer0.add(self.lig_03)
        self.fon_0 = arcade.SpriteList()
        for x in range(-100, 1900, 100):
            for y in range(-100, 1000, 100):
                a = arcade.Sprite('C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/images/bel.jpg')
                a.position = x, y
                self.fon_0.append(a)

        self.lig_layer1 = lights.LightLayer(1600, 800)
        self.lig_11 = lights.Light(800, 590, 100, (150, 200, 255), 'soft')
        self.lig_layer1.add(self.lig_11)
        z = lights.Light(800, 590, 200, (150, 200, 255), 'soft')
        self.lig_layer1.add(z)
        self.lig_12 = lights.Light(550, 450, 100, (200, 200, 200), 'soft')
        self.lig_layer1.add(self.lig_12)
        self.lig_13 = lights.Light(1050, 450, 100, (250, 200, 0), 'soft')
        self.lig_layer1.add(self.lig_13)

        self.lig_layer2 = lights.LightLayer(1600, 800)
        self.lig_21 = lights.Light(800, 590, 100, (250, 200, 0), 'soft')
        self.lig_layer2.add(self.lig_21)
        z = lights.Light(800, 590, 200, (250, 200, 0), 'soft')
        self.lig_layer2.add(z)
        self.lig_22 = lights.Light(550, 450, 100, (150, 200, 255), 'soft')
        self.lig_layer2.add(self.lig_22)
        self.lig_23 = lights.Light(1050, 450, 100, (255, 140, 0), 'soft')
        self.lig_layer2.add(self.lig_23)

        self.lig_layer3 = lights.LightLayer(1600, 800)
        self.lig_31 = lights.Light(800, 590, 100, (255, 140, 0), 'soft')
        self.lig_layer3.add(self.lig_31)
        z = lights.Light(800, 590, 200, (255, 140, 0), 'soft')
        self.lig_layer3.add(z)
        self.lig_32 = lights.Light(550, 450, 100, (250, 200, 0), 'soft')
        self.lig_layer3.add(self.lig_32)
        self.lig_33 = lights.Light(1050, 450, 100, (200, 200, 200), 'soft')
        self.lig_layer3.add(self.lig_33)

        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()

        kn_1 = arcade.gui.UIFlatButton(1000, 385, 100, 130)
        self.meneger.add(kn_1)
        kn_2 = arcade.gui.UIFlatButton(500, 385, 100, 130)
        self.meneger.add(kn_2)

        kn_3 = arcade.gui.UIFlatButton(645, 300, 310, 150, 'Выбрать')
        self.meneger.add(kn_3)


        self.fem_pers = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 1.1,
                                      center_x=800, center_y=600)
        self.fem_adv = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_"
                                     "idle.png", 1.1, center_x=800, center_y=600)
        self.m_pers = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", 1.1,
                                    center_x=800, center_y=600)
        self.m_adv = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", 1.1,
                                   center_x=800, center_y=600)

        @dek_schet
        def on_click_kn(evennt):
            global kol
            global kol2

            if kol == 1:
                self.kol12 = 1
                kol2 = 3
            if kol == 2:
                self.kol12 = 2
                kol2 = 2
            if kol == 3:
                self.kol12 = 3
                kol2 = 1
            if kol == 4:
                self.kol12 = 0
                kol2 = 0

            if kol > 3 or self.kol12 == 0:
                kol = 0

        kn_1.on_click = on_click_kn

        @dek_schet1
        def on_click_kn1(evennt):
            global kol
            global kol2

            if kol2 == 1:
                self.kol12 = 3
                kol = 3
            if kol2 == 2:
                self.kol12 = 2
                kol = 2
            if kol2 == 3:
                self.kol12 = 1
                kol = 1
            if kol2 == 4:
                self.kol12 = 0
                kol = 0

            if kol2 > 3 or self.kol12 == 0:
                kol2 = 0

        kn_2.on_click = on_click_kn1

        def on_click_kn2(event):
            game = GameViev()
            game.setup()
            self.window.show_view(game)
            del game

        kn_3.on_click = on_click_kn2

    def on_draw(self):
        self.clear()
        if self.kol12 == 0:
            with self.lig_layer0:
                self.fon_0.draw()
            self.lig_layer0.draw(ambient_color=(0, 0, 0))
        if self.kol12 == 1:
            with self.lig_layer1:
                self.fon_0.draw()
            self.lig_layer1.draw(ambient_color=(0, 0, 0))
        if self.kol12 == 2:
            with self.lig_layer2:
                self.fon_0.draw()
            self.lig_layer2.draw(ambient_color=(0, 0, 0))
        if self.kol12 == 3:
            with self.lig_layer3:
                self.fon_0.draw()
            self.lig_layer3.draw(ambient_color=(0, 0, 0))

        global vib
        if self.kol12 == 0:
            self.m_adv.draw()
            arcade.draw_text('Male Adventurer', 800, 490, (0, 0, 0), 20, anchor_x='center', anchor_y='center',
                             bold=True)
            vib = 0
        elif self.kol12 == 1:
            self.fem_adv.draw()
            arcade.draw_text('Female Adventurer', 800, 490, (0, 0, 0), 20, anchor_x='center', anchor_y='center',
                             bold=True)
            vib = 1
        elif self.kol12 == 2:
            self.m_pers.draw()
            arcade.draw_text('Male Person', 800, 490, (0, 0, 0), 20, anchor_x='center', anchor_y='center', bold=True)
            vib = 2
        elif self.kol12 == 3:
            self.fem_pers.draw()
            arcade.draw_text('Female Person', 800, 490, (0, 0, 0), 20, anchor_x='center', anchor_y='center', bold=True)
            vib = 3

        self.meneger.draw()

        if self.kol12 == 0:
            arcade.draw_text('<', 545, 450, (255, 140, 0), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
            arcade.draw_text('>', 1050, 450, (150, 200, 255), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
        if self.kol12 == 1:
            arcade.draw_text('<', 545, 450, (200, 200, 200), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
            arcade.draw_text('>', 1050, 450, (250, 200, 0), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
        if self.kol12 == 2:
            arcade.draw_text('<', 545, 450, (150, 200, 255), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
            arcade.draw_text('>', 1050, 450, (255, 140, 0), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
        if self.kol12 == 3:
            arcade.draw_text('<', 545, 450, (250, 200, 0), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)
            arcade.draw_text('>', 1050, 450, (200, 200, 200), font_size=64, anchor_x='center', anchor_y='center',
                             bold=True)

        arcade.draw_rectangle_outline(800, 575, 300, 250, (20, 20, 20), 10)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game = GameViev()
            game.setup()
            self.window.show_view(game)
            del game
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


kol = 0
kol2 = 0


def dek_schet(f):
    def wer(*args, **kwargs):
        global kol
        kol += 1
        f(*args, **kwargs)
    return wer


def dek_schet1(f):
    def wer(*args, **kwargs):
        global kol2
        kol2 += 1
        f(*args, **kwargs)
    return wer


class Paus(arcade.View):
    def __init__(self, viev):
        super().__init__()
        self.viev = viev

        self.meng = None
        self.v_box = None
        self.lig_layer = None
        self.fon = None

    def on_show_view(self):
        self.lig_layer = lights.LightLayer(800, 450)
        global vib
        if vib == 0:
            f = lights.Light(800, 350, 400, (200, 200, 200), 'soft')
            self.lig_layer.add(f)
        if vib == 1:
            f = lights.Light(800, 350, 400, (150, 200, 255), 'soft')
            self.lig_layer.add(f)
        if vib == 2:
            f = lights.Light(800, 350, 400, (250, 200, 0), 'soft')
            self.lig_layer.add(f)
        if vib == 3:
            f = lights.Light(800, 350, 400, (255, 140, 0), 'soft')
            self.lig_layer.add(f)

        q = lights.Light(790, 740, 175, (255, 255, 255), 'soft')
        self.lig_layer.add(q)

        self.fon = arcade.SpriteList()
        for i in range(-100, 1900, 100):
            for q in range(-100, 1000, 100):
                a = arcade.Sprite("C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/images/bel.jpg")
                a.position = i, q
                self.fon.append(a)

        self.meng = arcade.gui.UIManager()
        self.meng.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.meng.add(arcade.gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.v_box))

        text = arcade.gui.UITextArea(text='        Пауза', width=660, height=120, font_size=64, style='Impact',
                                     text_color=(20, 20, 20))
        self.v_box.add(text.with_space_around(bottom=60))

        kn1 = arcade.gui.UIFlatButton(text='Продолжить', width=400, height=80)
        self.v_box.add(kn1.with_space_around(bottom=40))

        kn2 = arcade.gui.UIFlatButton(text='Заново', width=400, height=80)
        self.v_box.add(kn2.with_space_around(bottom=40))

        kn3 = arcade.gui.UIFlatButton(text='Выбор персонажа', width=400, height=80)
        self.v_box.add(kn3.with_space_around(bottom=40))

        kn4 = arcade.gui.UIFlatButton(text='Выйти из игры', width=400, height=80)
        self.v_box.add(kn4)

        def click_kn1(event):
            self.window.show_view(self.viev)
        kn1.on_click = click_kn1

        def click_kn2(event):
            gem = GameViev()
            gem.setup()
            self.window.show_view(gem)
            del gem
        kn2.on_click = click_kn2

        def click_kn3(event):
            vibor = Vibor()
            self.window.show_view(vibor)
            del vibor
        kn3.on_click = click_kn3

        def click_kn4(event):
            arcade.close_window()
        kn4.on_click = click_kn4

    def on_draw(self):
        self.clear()

        with self.lig_layer:
            self.fon.draw()
        self.lig_layer.draw(ambient_color=(0, 0, 0))

        self.meng.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.viev)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            self.viev.setup()
            self.window.show_view(self.viev)


class Porazhenie(arcade.View):
    def __init__(self):
        super().__init__()

        self.maneger = None
        self.v_bax = None
        self.lights_layer1 = None
        self.pr_light = None
        self.fon_r = None

    def on_show_view(self):
        self.lights_layer1 = lights.LightLayer(1600, 900)
        self.lights_layer1.set_background_color(arcade.color.BURGUNDY)

        self.pr_light = lights.Light(800, 450, 550, (200, 0, 0), 'soft')
        self.lights_layer1.add(self.pr_light)

        self.fon_r = arcade.SpriteList()
        for i in range(-100, 1900, 100):
            for q in range(-100, 1000, 100):
                e = arcade.Sprite("C:/Users/user/Desktop/Igra/venv/Lib/site-packages/arcade/resources/images/bel.jpg")
                e.position = i, q
                self.fon_r.append(e)

        self.maneger = arcade.gui.UIManager()
        self.maneger.enable()
        self.v_bax = arcade.gui.UIBoxLayout()
        self.maneger.add(arcade.gui.UIAnchorWidget(anchor_x="center", anchor_y="center", child=self.v_bax))

        pr_text = arcade.gui.UITextArea(text="     Вы проиграли", text_color=(0, 0, 0), width=660,
                                        height=120, font_size=64, font_name='Impact')
        self.v_bax.add(pr_text.with_space_around(bottom=60))
        zan_kn = arcade.gui.UIFlatButton(text='Заново', width=400, height=80)
        self.v_bax.add(zan_kn.with_space_around(bottom=40))

        glav_m_kn = arcade.gui.UIFlatButton(text="Выбор персонажа", width=400, height=80)
        self.v_bax.add(glav_m_kn.with_space_around(bottom=40))

        vit_kn = arcade.gui.UIFlatButton(text='Выйти из игры', width=400, height=80)
        self.v_bax.add(vit_kn.with_space_around(bottom=40))

        def on_click_nach(event):
            game = GameViev()
            game.setup()
            self.window.show_view(game)
            del game
        zan_kn.on_click = on_click_nach

        def on_click_glav_m(event):
            game = Vibor()
            self.window.show_view(game)
            del game
        glav_m_kn.on_click = on_click_glav_m

        def on_click_vit(event):
            arcade.close_window()
        vit_kn.on_click = on_click_vit

    def on_draw(self):
        with self.lights_layer1:
            self.fon_r.draw()
        self.lights_layer1.draw(ambient_color=(50, 0, 0))
        self.maneger.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game = GameViev()
            game.setup()
            self.window.show_view(game)
            del game
        elif symbol == arcade.key.SPACE:
            game = Vibor()
            self.window.show_view(game)
            del game
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()


win0 = arcade.Window(1600, 900)
glav_menu = GlavMenu()
win0.show_view(glav_menu)
arcade.run()
