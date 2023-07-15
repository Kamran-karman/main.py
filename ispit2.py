from array import array
from dataclasses import dataclass
import arcade
import arcade.gl
import random
import time
import math


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "GPUParticleExplosion"

KOL_CHAST = 500

MAX_TIME = 0.6
MIN_TIME = 0.2


def draw(self, *, filter=None, pixelated=None, blend_function=None):
    if self.udar:
        spisok = []
        spisok2 = []
        spisok3 = []
        for sprite in self.sprite_list:
            if arcade.check_for_collision(self.radius, sprite):
                poz_x, poz_y = abs(sprite.center_x - self.igrok.center_x), \
                    abs(sprite.center_y - self.igrok.center_y)
                pozi = (poz_x, poz_y)
                spisok.append(pozi)
                x, y = sprite.center_x, sprite.center_y
                xy = (x, y)
                spisok2.append(xy)
        if len(spisok) != 0:
            st_x, st_y = self.igrok.position
            en = None
            if len(spisok) != 0:
                for pozi in spisok:
                    if min(spisok) == pozi:
                        en = spisok.index(pozi)
            en_x, en_y = spisok2[en]
            spisok3.append(spisok2[en])
            arcade.draw_line(st_x, st_y, en_x, en_y, SINI, 30)
            arcade.draw_circle_filled(st_x, st_y, 50, SINI)
            arcade.draw_circle_filled(en_x, en_y, 30, SINI)
            arcade.draw_line(st_x, st_y, en_x, en_y, BEL, 20)
            arcade.draw_circle_filled(st_x, st_y, 45, BEL)
            arcade.draw_circle_filled(en_x, en_y, 25, BEL)
            radius = arcade.Sprite("C:/Users/user/Desktop/Igra/nuzhno/radius_porazheniya.png", 0.204)
            radius.position = en_x, en_y
            w = 0
            while w < 4:
                if arcade.check_for_collision_with_list(radius, self.sprite_list):
                    spisok = []
                    spisok2 = []
                    if self.igrok.position == (st_x, st_y):
                        pred_poz = 0, 0
                    else:
                        pred_poz = st_x, st_y
                    for sprite in self.sprite_list:
                        if arcade.check_for_collision(radius, sprite) and sprite.position != radius.position \
                                and sprite.position != pred_poz:
                            poz_x, poz_y = abs(radius.center_x - sprite.center_x), abs(
                                radius.center_y - sprite.center_y)
                            pozi = (poz_x, poz_y)
                            x, y = sprite.center_x, sprite.center_y
                            xy = (x, y)
                            e = 0
                            for i in spisok3:
                                if xy[0] == i[0] and xy[1] == i[1]:
                                    e += 1
                            if e == 0:
                                spisok.append(pozi)
                                spisok2.append(xy)
                    if len(spisok) == 0:
                        if st_x > en_x:
                            self.en_x, self.en_y = en_x - 30, en_y + 10
                        elif st_x < en_x:
                            self.en_x, self.en_y = en_x + 30, en_y + 10
                            self.s = False
                        break
                    elif w == 3 and len(spisok) != 0:
                        en = None
                        for pozi in spisok:
                            if min(spisok) == pozi:
                                en = spisok.index(pozi)
                        st_x, st_y = radius.position
                        en_x, en_y = spisok2[en]
                        arcade.draw_line(st_x, st_y, en_x, en_y, SINI, 30)
                        arcade.draw_circle_filled(en_x, en_y, 30, SINI)
                        arcade.draw_circle_filled(st_x, st_y, 30, SINI)
                        arcade.draw_line(st_x, st_y, en_x, en_y, BEL, 20)
                        arcade.draw_circle_filled(st_x, st_y, 25, BEL)
                        arcade.draw_circle_filled(en_x, en_y, 25, BEL)
                        if st_x > en_x:
                            self.en_x, self.en_y = en_x - 30, en_y + 10
                        elif st_x < en_x:
                            self.en_x, self.en_y = en_x + 30, en_y + 10
                            self.s = False
                        break
                    else:
                        en = None
                        if len(spisok) != 0:
                            st_x, st_y = radius.position
                            for pozi in spisok:
                                if min(spisok) == pozi:
                                    en = spisok.index(pozi)
                            en_x, en_y = spisok2[en]
                            spisok3.append(spisok2[en])
                            arcade.draw_line(st_x, st_y, en_x, en_y, SINI, 30)
                            arcade.draw_circle_filled(en_x, en_y, 30, SINI)
                            arcade.draw_circle_filled(st_x, st_y, 30, SINI)
                            arcade.draw_line(st_x, st_y, en_x, en_y, BEL, 20)
                            arcade.draw_circle_filled(st_x, st_y, 25, BEL)
                            arcade.draw_circle_filled(en_x, en_y, 25, BEL)
                            radius.position = en_x, en_y
                w += 1


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.chasti_list = []
        self.program = self.ctx.load_program(vertex_shader='C:/Users/user/Desktop/Igra/shederi_igra/ver_snad_v1_ogon.glsl',
                                             fragment_shader='C:/Users/user/Desktop/Igra/shederi_igra/frag_shad_ogon.glsl')
        self.ctx.enable_only(self.ctx.BLEND)

        self.s = 0

    def on_draw(self):
        self.clear()
        if self.s >= 0:

            x = random.randint(450, 550)
            y = random.randint(150, 250)

            def gen_init__data(init_x, init_y):
                for i in range(50):
                    prav_gran_x = 510 / self.width * 2. - 1
                    lev_gran_x = 490 / self.width * 2. - 1
                    dx = random.uniform(-0.15, 0.15)
                    dy = random.uniform(0, 2)
                    r = random.uniform(0, 1)
                    b = random.uniform(0, r)
                    g = 0
                    fade_rate = random.uniform(1 / MAX_TIME, 1 / MIN_TIME)
                    x3b = 550 / self.width * 2. - 1
                    x3m = 450 / self.width * 2. - 1
                    if init_x < x3m or init_x > x3b:
                        init_x = random.randint(450, 550) / self.width * 2. - 1
                    y3b = 250 / self.height * 2. - 1
                    y3m = 150 / self.height * 2. - 1
                    if init_y < y3m or init_y > y3b:
                        init_y = random.randint(150, 250) / self.height * 2. - 1
                    yield init_x
                    yield init_y
                    yield dx
                    yield dy
                    yield r
                    yield g
                    yield b
                    yield fade_rate
                    yield prav_gran_x
                    yield lev_gran_x
                    init_x += random.randint(-5, 5) / self.width * 2. - 1
                    init_y += random.randint(-5, 5) / self.height * 2. - 1

            x2 = x / self.width * 2. - 1.
            y2 = y / self.height * 2. - 1.

            init_data = gen_init__data(x2, y2)

            bauffer = self.ctx.buffer(data=array('f', init_data))

            buffer_deskript = arcade.gl.BufferDescription(bauffer, '2f 2f 3f f f f', ['in_pos', 'in_vel', 'in_color',
                                                                                      'in_fade_rate', 'in_prav_x',
                                                                                      'in_lev_x'])

            vao = self.ctx.geometry([buffer_deskript])

            chast = Chasti(buffer=bauffer, vao=vao, start_time=time.time())
            self.chasti_list.append(chast)

        self.ctx.point_size = 10 * self.get_pixel_ratio()

        for chast in self.chasti_list:
            self.program['time'] = time.time() - chast.start_time
            chast.vao.render(self.program, mode=self.ctx.POINTS)

        arcade.draw_rectangle_outline(500, 200, 200, 100, arcade.color.WHITE, 10)

    def on_update(self, delta_time: float):
        self.s += 1

        temp_list = self.chasti_list.copy()
        for chast in temp_list:
            if time.time() - chast.start_time > MAX_TIME:
                self.chasti_list.remove(chast)


window = MyWindow()
window.center_window()
arcade.run()
