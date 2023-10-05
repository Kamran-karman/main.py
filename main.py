import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import random
import arcade
import arcade.gui
from dataclasses import dataclass
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
IG_MAX_VERTICAL_SPEED = 100000
IG_MAX_HORIZANTAL_SPEED = 400
IGROK_JUMP_FORCE = 60000
WALL_FRICTION = 0.8
WALL_CT = 'wall'

# Координаты игрока
IGROK_POSITION = 300, 200


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class Igra1GlavaViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((255, 182, 193, 255))

        self.igrok = None
        self.brend = None

        self.box_fight = None
        self.fight = False

        self.vrag_list = None
        self.zhivie_vrag_list = None
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

        self.s_voln = 0

    def setup(self):
        self.kamera = arcade.Camera()

        self.smert_list1 = arcade.SpriteList()
        self.smert_list2 = arcade.SpriteList()

        self.sprite_list = arcade.SpriteList()
        self.v_drug_list = arcade.SpriteList()
        self.vrag_list = arcade.SpriteList()

        self.walls_list = arcade.SpriteList()
        for x in range(-50000, 50000, 128):
            wall = arcade.Sprite(':resources:images/tiles/grassMid.png')
            wall.position = x, 64
            self.walls_list.append(wall)

        self.zhivie_vrag_list = arcade.SpriteList()

        self.igrok = pers.Voyslav(self.vrag_list, self.fizika)
        self.igrok.position = IGROK_POSITION
        self.igrok.hp -= 130

        voin_in = pers.VoinInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list, 202)
        voin_in.position = 100, 200
        self.zhivie_vrag_list.append(voin_in)
        self.vrag_list.append(voin_in)
        self.v_drug_list.append(voin_in)

        for x in range(-100, 1, 100):
            vrag = pers.ZhitelInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list,
                                         random.randint(204, 205))
            vrag._position = x, 200
            vrag.hp -= 75
            self.zhivie_vrag_list.append(vrag)
            self.vrag_list.append(vrag)
            self.v_drug_list.append(vrag)

        for vrag in self.zhivie_vrag_list:
            vrag.v_drug_list = self.zhivie_vrag_list

        self.igrok.sprite_list = self.vrag_list

        self.box_fight = arcade.SpriteList()
        for x in range(-2032, 2033, 64):
            for i in range(-1, 2, 2):
                box = arcade.Sprite('nuzhno/box_fight.png')
                box.scale = 0.5
                box.position = x, 2032 * i
                self.box_fight.append(box)
        for y in range(-2032, 2033, 64):
            for i in range(-1, 2, 2):
                box = arcade.Sprite('nuzhno/box_fight.png')
                box.scale = 0.5
                box.position = 2032 * i, y
                self.box_fight.append(box)

        self.fizika = arcade.PymunkPhysicsEngine(GRAVITY, DAMPING)
        self.fizika.add_sprite(self.igrok, MASS_IGROK, FRICTION_IGROK, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                               max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
                               moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)
        self.fizika.add_sprite_list(self.walls_list, friction=WALL_FRICTION, collision_type=WALL_CT,
                                    body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.fizika.add_sprite_list(self.box_fight, friction=1, collision_type=WALL_CT,
                                    body_type=arcade.PymunkPhysicsEngine.STATIC)

        for vrag in self.zhivie_vrag_list:
            self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=200,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

        self.igrok.fizika = self.fizika

    def volna1(self):
        vrag_list = arcade.SpriteList()
        voin_in = pers.VoinInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list, 202)
        voin_in.position = -1450, 250
        vrag_list.append(voin_in)
        gromila = pers.Gromila(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list)
        gromila.position = 1450, 300
        vrag_list.append(gromila)
        for x in range(900, 1251, 150):
            vrag = pers.ZhitelInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list,
                                         random.randint(204, 205))
            vrag.position = x, 200
            vrag_list.append(vrag)
        for x in range(-1251, -900, 150):
            vrag = pers.ZhitelInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list,
                                         random.randint(204, 205))
            vrag.position = x, 200
            vrag_list.append(vrag)

        for vrag in vrag_list:
            self.vrag_list.append(vrag)
            self.zhivie_vrag_list.append(vrag)
            self.v_drug_list.append(vrag)
            self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=200,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

        for vrag in self.vrag_list:
            vrag.v_drug_list = self.v_drug_list

        self.igrok.sprite_list = self.vrag_list
        self.igrok.fizika = self.fizika

    def volna2(self):
        vrag_list = arcade.SpriteList()
        brend = pers.Brend(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list)
        brend._position = -1200, 200
        vrag_list.append(brend)
        for x in range(-1351, -1275, 75):
            voin_in = pers.VoinInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list, 202)
            voin_in.position = x, 250
            vrag_list.append(voin_in)
        for x in range(-1400, 1401, 2800):
            gromila = pers.Gromila(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list)
            gromila.position = x, 300
            vrag_list.append(gromila)
        for x in range(1250, 1351, 50):
            vrag = pers.ZhitelInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list,
                                         random.randint(204, 205))
            vrag.position = x, 200
            vrag_list.append(vrag)

        for vrag in vrag_list:
            self.vrag_list.append(vrag)
            self.zhivie_vrag_list.append(vrag)
            self.v_drug_list.append(vrag)
            self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=200,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

        for vrag in self.vrag_list:
            vrag.v_drug_list = self.v_drug_list

        self.igrok.sprite_list = self.vrag_list
        self.igrok.fizika = self.fizika

    def volna3(self):
        for vrag in self.vrag_list:
            if vrag.pers == 'Brend' and vrag.smert:
                vrag.hp += 1000
                vrag.smert = False
                vrag.angle = 0
                self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                       max_horizontal_velocity=200,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)
                self.zhivie_vrag_list.append(vrag)
                self.v_drug_list.append(vrag)
        vrag_list = arcade.SpriteList()
        s = 0
        for x in range(-1700, 1301, 75):
            s += 1
            if s <= 3 or x == 1300:
                voin_in = pers.VoinInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list, 202)
                voin_in.position = x, 250
                vrag_list.append(voin_in)
        for x in range(1400, 1501, 100):
            gromila = pers.Gromila(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list)
            gromila.position = x, 300
            vrag_list.append(gromila)
        for x in range(-1800, 1801, 3600):
            vrag = pers.ZhitelInnocentii(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list,
                                         random.randint(204, 205))
            vrag.position = x, 200
            vrag_list.append(vrag)

        for vrag in vrag_list:
            self.vrag_list.append(vrag)
            self.zhivie_vrag_list.append(vrag)
            self.v_drug_list.append(vrag)
            self.fizika.add_sprite(vrag, 2, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=200,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

        for vrag in self.vrag_list:
            vrag.v_drug_list = self.v_drug_list

        self.igrok.sprite_list = self.vrag_list
        self.igrok.fizika = self.fizika

    def on_draw(self):
        self.clear()

        self.smert_list1.draw()
        for vrag in self.zhivie_vrag_list:
            vrag.draw()
            vrag.update_animation()
        self.igrok.draw()
        self.igrok.update_animation()
        self.smert_list2.draw()

        self.walls_list.draw()
        # self.box_fight.draw()

        self.kamera.use()
        self.center_kamera_za_igrok()

    def on_update(self, delta_time: float):
        self.igrok.on_update()

        if self.igrok.smert:
            self.window.close()

        for vrag in self.zhivie_vrag_list:
            if vrag.smert:
                if random.randint(0, 1) == 1:
                    self.smert_list1.append(vrag)
                else:
                    self.smert_list2.append(vrag)
                self.zhivie_vrag_list.remove(vrag)
                self.v_drug_list.remove(vrag)
                self.fizika.remove_sprite(vrag)
                vrag.smert_func()

            else:
                vrag.on_update()

                x = vrag.return_force('x')
                y = vrag.return_force('y')

                if y > 0:
                    self.s += 1
                if self.s > 2 and not vrag.is_on_ground:
                    y = 0

                force = (x, y)
                friction = 0.1
                if abs(x) > 0:
                    force, friction = vrag.oglush_force(force, friction, 10)
                    force, friction = vrag.slabweak_func(force, friction)
                    self.fizika.apply_force(vrag, force)
                    self.fizika.set_friction(vrag, friction)
                    vrag.stamina -= 0.2 / 60
                elif y > 0:
                    force, friction = vrag.oglush_force(force, friction, 10)
                    force, friction = vrag.slabweak_func(force, friction)
                    self.fizika.apply_force(vrag, force)
                    vrag.stamina -= 2 / 60
                else:
                    self.fizika.set_friction(vrag, friction * 10)

                if y == 0 and self.s >= 2:
                    self.s = 0

                if vrag.return_position:
                    self.fizika.set_position(vrag, vrag.return_position_func())

        friction = 0.5
        if self.pravo and not self.levo:
            force = (IGROK_MOVE_GROUND, 0)
            force, friction = self.igrok.oglush_force(force, friction, 2)
            force, friction = self.igrok.slabweak_func(force, friction)
            self.fizika.apply_force(self.igrok, force)
            self.fizika.set_friction(self.igrok, friction)
            self.igrok.stamina -= 0.2 / 60
        elif not self.pravo and self.levo:
            force = (-IGROK_MOVE_GROUND, 0)
            force, friction = self.igrok.oglush_force(force, friction, 2)
            force, friction = self.igrok.slabweak_func(force, friction)
            self.fizika.apply_force(self.igrok, force)
            self.fizika.set_friction(self.igrok, friction)
            self.igrok.stamina -= 0.2 / 60
        else:
            self.fizika.set_friction(self.igrok, friction * 2)

        if self.igrok.molniya.tp and self.s1 == 0:
            self.s1 += 1
            poz = self.igrok.molniya.return_position()
            self.fizika.set_position(self.igrok, poz)

        if len(self.zhivie_vrag_list) <= 0 and self.s_voln == 0:
            self.fight = True
            self.s_voln += 1
            self.volna1()

        if len(self.zhivie_vrag_list) <= 1 and self.s_voln == 1:
            self.s_voln += 1
            self.volna2()

        if len(self.zhivie_vrag_list) <= 1 and self.s_voln == 2:
            self.s_voln += 1
            self.volna3()

        self.fizika.step()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RALT:
            self.igrok.udar_Zevsa.action = True

        if symbol == arcade.key.RCTRL:
            self.igrok.shar_mol.zaryad = True

        if symbol == arcade.key.RSHIFT:
            self.igrok.block.block = True

        if symbol == arcade.key.SPACE:
            self.igrok.shchit.action = True

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
                force, friction = self.igrok.oglush_force(force, 0, 2)
                force, friction = self.igrok.slabweak_func(force, friction)
                self.fizika.apply_force(self.igrok, force)
                self.igrok.stamina -= 2

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.RALT:
            self.igrok.udar_Zevsa.action = False

        if _symbol == arcade.key.RCTRL:
            self.igrok.shar_mol.action = True
            self.igrok.shar_mol.zaryad = False

        if _symbol == arcade.key.RSHIFT:
            self.igrok.block.block = False

        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pravo = False
        elif _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.levo = False

    def center_kamera_za_igrok(self, x=False, y=False):
        ekran_center_x = self.igrok.center_x - self.kamera.viewport_width / 3
        ekran_center_y = self.igrok.center_y - self.kamera.viewport_height / 5

        if ekran_center_x > 400:
            ekran_center_x = 400
        if ekran_center_x < - 2000:
            ekran_center_x = -2000

        self.kamera.move_to((ekran_center_x, ekran_center_y), 0.1)

        if x:
            return ekran_center_x
        if y:
            return ekran_center_y


window = arcade.Window(W, H)
viev1 = Igra1GlavaViev()
viev1.setup()
window.show_view(viev1)

window.show_view(viev1)

arcade.run()
