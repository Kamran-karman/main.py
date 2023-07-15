import math
import arcade
import random
from dataclasses import dataclass
from array import array
import arcade.gl
import arcade.gui
import time

MAX_TIME = 0.8
MIN_TIME = 0.3

KOOR_X = 400
KOOR_Y = 600
D_ZONE = 0.01
W = 1600
H = 900

SINI = (44, 117, 255)
BEL = (255, 255, 255)
RED = (255, 0, 0)

GRAVITI = 1
IG_JUMP_F = 20
SKOROST_IGROKA_WALK = 5
BEG_IGROKA = 20
V_VRAG = 5
BEG_VRAGA = 10
STOP = 7


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


class Molniay(arcade.Sprite):
    def __init__(self, radius, sprite_list, igrok, a):
        super().__init__()
        self.radius = radius
        self.sprite_list = sprite_list
        self.igrok = igrok
        self.en_x = 0
        self.en_y = 0
        self.udar = a
        self.s = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.s <= 3 and self.udar:
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
            if len(spisok) > 0:
                stx, sty = self.igrok.position
                en = spisok.index(min(spisok))
                enx, eny = spisok2[en]
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.s == 0:
                        sprite.hp -= 30
                spisok3.append(spisok2[en])
                arcade.draw_line(stx, sty, enx, eny, SINI, 30)
                arcade.draw_circle_filled(stx, sty, 50, SINI)
                arcade.draw_circle_filled(enx, eny, 30, SINI)
                arcade.draw_line(stx, sty, enx, eny, BEL, 20)
                arcade.draw_circle_filled(stx, sty, 45, BEL)
                arcade.draw_circle_filled(enx, eny, 25, BEL)
                radius = arcade.Sprite("C:/Users/user/Desktop/Igra/nuzhno/radius_porazheniya.png", 0.204)
                radius.position = enx, eny
                w = 0
                while w < 4:
                    if arcade.check_for_collision_with_list(radius, self.sprite_list):
                        if self.igrok.position == (stx, sty):
                            pred_poz = 0, 0
                        else:
                            pred_poz = stx, sty
                        spisok = []
                        spisok2 = []
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
                            if stx > enx:
                                self.en_x, self.en_y = enx - 30, eny + 10
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 30, eny + 10
                            break
                        elif w == 3 and len(spisok) != 0:
                            en = spisok.index(min(spisok))
                            stx, sty = radius.position
                            enx, eny = spisok2[en]
                            for sprite in self.sprite_list:
                                if sprite.position == (enx, eny) and self.s == 0:
                                    sprite.hp -= 30
                            arcade.draw_line(stx, sty, enx, eny, SINI, 30)
                            arcade.draw_circle_filled(enx, eny, 30, SINI)
                            arcade.draw_circle_filled(stx, sty, 30, SINI)
                            arcade.draw_line(stx, sty, enx, eny, BEL, 20)
                            arcade.draw_circle_filled(stx, sty, 25, BEL)
                            arcade.draw_circle_filled(enx, eny, 25, BEL)
                            if stx > enx:
                                self.en_x, self.en_y = enx - 30, eny + 10
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 30, eny + 10
                            break
                        else:
                            if len(spisok) != 0:
                                en = spisok.index(min(spisok))
                                stx, sty = radius.position
                                enx, eny = spisok2[en]
                                for sprite in self.sprite_list:
                                    if sprite.position == (enx, eny) and self.s == 0:
                                        sprite.hp -= 30
                                spisok3.append(spisok2[en])
                                arcade.draw_line(stx, sty, enx, eny, SINI, 30)
                                arcade.draw_circle_filled(enx, eny, 30, SINI)
                                arcade.draw_circle_filled(stx, sty, 30, SINI)
                                arcade.draw_line(stx, sty, enx, eny, BEL, 20)
                                arcade.draw_circle_filled(stx, sty, 25, BEL)
                                arcade.draw_circle_filled(enx, eny, 25, BEL)
                                radius.position = enx, eny
                    w += 1
        if self.s > 3:
            self.udar = False
        if self.udar:
            self.s += 1
        elif not self.udar:
            self.s = 0

    def koordinati(self):
        return self.en_x, self.en_y


class UdarZevsa(arcade.Sprite):
    def __init__(self, radius, sprite_list, igrok):
        super().__init__()
        if sprite_list is arcade.SpriteList():
            print(1)
            self.sprite_list = arcade.SpriteList()
            self.sprite_list.append(sprite_list)
        else:
            self.sprite_list = sprite_list
        self.radius = radius
        self.igrok = igrok
        self.kk = random.randint(150, 175)
        self.s = 0
        self.s2 = False
        self.pora = False
        self.kriv = False

    def gipotenuza(self, katet, ugl):
        gipot = katet / math.sin(math.radians(ugl))
        return gipot

    def katet(self, gipot, katet):
        katet2 = (gipot ** 2 - katet ** 2) ** 0.5
        return katet2

    def kk_gg(self, k1, k2):
        self.kk = random.randint(k1, k2)
        self.ugl = random.randint(60, 85)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        spisok = []
        slovar = {}
        for sprite in self.sprite_list:
            if arcade.check_for_collision(self.radius, sprite):
                rast_x, rast_y = abs(sprite.center_x - self.radius.center_x),\
                    abs(sprite.center_y - self.radius.center_y)
                x, y = sprite.center_x, sprite.center_y
                slovar.update({(rast_x, rast_y): (x, y)})
            if len(slovar) > 0:
                cel = min(slovar)
                if math.hypot(cel[0], cel[1]) > 200:
                    self.kriv = True
                st_x, st_y = self.igrok.position
                if not self.kriv:
                    en_x, en_y = slovar[cel]
                    arcade.draw_line(st_x, st_y, en_x, en_y, SINI, 30)
                    arcade.draw_line(st_x, st_y, en_x, en_y, BEL, 25)
                elif self.kriv:
                    if self.pora:
                        self.kk_gg(150, 175)
                    gg = self.gipotenuza(self.kk, self.ugl)
                    kk2 = self.katet(gg, self.kk)
                    st_x, st_y = 0, 300
                    sr_x, sr_y = st_x + self.kk, st_y
                    en_x, en_y = sr_x, sr_y + kk2
                    spisok.append((st_x, st_y))
                    spisok.append((en_x, en_y))
                    popal = False
                    q1 = (st_x, st_y)
                    q2 = (en_x, en_y)
                    while not popal:
                        pass

    def update(self):
        if self.kriv:
            self.s += 1
            if self.s == 1 and not self.s2:
                self.s = 0
                self.s2 = True
                self.pora = True
            elif self.s == 30:
                self.pora = True


class GnevTora(arcade.Sprite):
    def __init__(self, x, y, sprite_list=None, sprite=None):
        super().__init__()
        # Эта переменная указывает список целей
        self.sprite_list = sprite_list
        # Эта переменная указывает одну цель
        self.sprite = sprite
        # Эта переменая - радиус поражения
        self.radius = Radius(1)
        self.x = x
        self.y = y
        # Счётчики
        self.s2 = 0
        self.s = 301
        # Эта переменна указывает, поразило ли кого-нибудь
        self.udar = False
        # Возможно эту переменную надо будет удалить
        self.drav = False

    # Эта функция будет переделана, но переделать можешь и ты
    def update_animation(self, delta_time: float = 1 / 60):
        self.s += 1
        if self.s <= 300:
            self.udar = False
            return
        if self.udar and self.s2 < 3 and self.s > 300:
            arcade.draw_circle_filled(self.x, self.y, 250, SINI)
            arcade.draw_circle_filled(self.x, self.y, 150, BEL)

        if self.s2 >= 3:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s2 += 1
        elif not self.udar:
            self.s2 = 0

    def on_update(self, delta_time: float = 1 / 60):
        self.radius.position = self.x, self.y

        # Последующие 2 условия проверяют одна ли цели или их несколько
        if self.sprite_list is not None:
            if arcade.check_for_collision_with_list(self.radius, self.sprite_list) and self.s2 == 1 and self.udar:
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self.radius, sprite):
                        sprite.oglush = True
                        sprite.hp -= 20

        if self.sprite is not None:
            if arcade.check_for_collision(self.radius, self.sprite) and self.s2 == 1 and self.udar:
                self.sprite.hp -= 20


class Vrag1(arcade.Sprite):
    def __init__(self):
        super().__init__()
        main_patch = ":resources:images/alien/"
        self.idle = load_tex_pair(f"{main_patch}/alienBlue_front.png")
        self.texture = self.idle[1]
        self.hp = 0
        self.oglush = False

    def update_animation(self, delta_time: float = 1 / 60):
        stx = self.center_x
        sty = self.top + 15
        if self.hp < 0:
            text_uron = f'{self.hp * -1}'
        else:
            text_uron = f'{self.hp}'
        arcade.draw_text(text_uron, stx, sty, (200, 0, 0), 16, font_name='Impact', anchor_x='center',
                         anchor_y='center')


class Atak(arcade.Sprite):
    def __init__(self, storona):
        super().__init__()
        self.udar = False
        self.storona = storona

        self.s_atak_tex1 = 0

        self.atak_t1 = []
        for i in range(2, 4):
            tex = load_tex_pair(f'nuzhno/atak_animation/maleAdventurer_atak{i}.png')
            self.atak_t1.append(tex)
        self.texture = self.atak_t1[1][self.storona]

        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        self.s_atak_tex1 += 0.025
        if self.s_atak_tex1 > 2:
            self.s_atak_tex1 = 0
        self.texture = self.atak_t1[int(self.s_atak_tex1)][self.storona]


class Vrag(arcade.Sprite):
    def __init__(self, igrok, kast_scena=False):
        super().__init__()
        self.hp = 100

        self.stan = False
        self.s_stan = 0
        self.oglush = False
        self.s_oglush = 0

        self.scale = 1
        self.storona = 1
        self.radius_vid = Radius(3)
        self.radius_ataki = Radius(0)
        self.igrok = igrok
        self.udar = False
        self.kast_scena = kast_scena
        self.atak = Atak(self.storona)
        self.atak_anim = False

        self.s = 81
        self.s1 = 121

        self.sch_walk_tex = 0
        self.s_atak_tex1 = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle[0]

        self.atak_t1 = []
        tex = load_tex_pair('nuzhno/atak_animation/maleAdventurer_atak0.png')
        self.atak_t1.append(tex)
        tex = load_tex_pair('nuzhno/atak_animation/maleAdventurer_atak1.png')
        self.atak_t1.append(tex)
        self.texture = self.idle[0]

        self.hit_box = self.texture.hit_box_points

        self.c_y = None
        self.y_oglush = True

    def on_update(self, delta_time: float = 1 / 60):
        self.s += 1
        self.radius_vid.position = self.radius_ataki.position = self.atak.position = self.position
        if self.storona == 0:
            self.atak.position = self.atak.center_x + 25, self.atak.center_y + 10
        elif self.storona == 1:
            self.atak.position = self.atak.center_x - 25, self.atak.center_y + 10
        self.atak.storona = self.storona
        stop = abs(self.igrok.center_x - self.radius_vid.center_x)
        if arcade.check_for_collision(self.radius_vid, self.igrok) and not self.stan and not self.oglush:
            if not self.kast_scena:
                if self.igrok.center_x > self.radius_vid.center_x:
                    if self.igrok.left - self.right <= 20:
                        self.change_x = 0
                    elif 0.0 <= stop < STOP:
                        self.change_x = 0
                    else:
                        self.change_x = V_VRAG
                elif self.igrok.center_x < self.radius_vid.center_x:
                    if self.left - self.igrok.right <= 20:
                        self.change_x = 0
                    elif 0.0 <= stop < STOP:
                        self.change_x = 0
                    else:
                        self.change_x = -V_VRAG
            else:
                self.change_x = 0
        else:
            self.change_x = 0

        if not self.kast_scena:
            if self.atak_anim:
                self.change_x = 0
            if arcade.check_for_collision(self.radius_ataki, self.igrok) and not self.oglush:
                self.udar = True
                if arcade.check_for_collision(self.atak, self.igrok) and self.s > 80:
                    self.s = 0
                    self.igrok.hp -= 5
                    print(self.igrok.hp)
            else:
                self.udar = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.s1 += 1
        if self.y_oglush:
            self.c_y = self.center_y

        if self.oglush and self.s_oglush <= 150:
            self.y_oglush = False
            self.change_x = 0
            self.change_y = 0
            self.s_oglush += 1
            self.angle = -90
            self.center_y = 128

        if self.s_oglush > 150:
            self.y_oglush = True
            self.oglush = False
            self.s_oglush = 0
            self.angle = 0
            self.center_y = self.c_y

        if self.stan and self.s_stan <= 120:
            self.change_x = 0
            self.change_y = 0
            self.s_stan += 1

        if self.s_stan > 120:
            self.stan = False
            self.s_stan = 0

        if self.change_x > 0 and self.storona == 1:
            self.storona = 0
        elif self.change_x < 0 and self.storona == 0:
            self.storona = 1

        if self.change_y > 0:
            self.texture = self.jump_tex[self.storona]
        elif self.change_y < 0:
            self.texture = self.fall_tex[self.storona]

        if self.change_y == 0 and self.change_x == 0:
            self.texture = self.idle[self.storona]

        if abs(self.change_x) > 0 and self.change_y == 0:
            self.sch_walk_tex += 0.1
            if self.sch_walk_tex > 8:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[int(self.sch_walk_tex)][self.storona]

        if self.udar and self.s1 > 120 or self.atak_anim:
            self.atak_anim = True
            self.atak.update_animation()
            self.atak.draw()
            self.s_atak_tex1 += 0.025
            if self.s_atak_tex1 > 2:
                self.atak_anim = False
                self.s1 = 0
                self.s_atak_tex1 = 0
                self.texture = self.idle[self.storona]
                return 
            self.texture = self.atak_t1[int(self.s_atak_tex1)][self.storona]
            #self.atak.update_animation()


class Oruzhie(arcade.Sprite):
    def __init__(self, igrok, sprite, kast_scena=False):
        super().__init__()
        self.palka = load_tex_pair('nuzhno/bridgeB.png')
        self.texture = self.palka[1]
        self.scale = 1
        self.udar = False
        self.angle = -30
        self.igrok = igrok
        self.sprite = sprite
        self.kast_scena = kast_scena
        self.s1 = 60

        self.s = -30

        self.hit_box = self.texture.hit_box_points
        self.nazad = False

    def on_update(self, delta_time: float = 1 / 60):
        self.position = self.sprite.position

        self.s += 1
        if arcade.check_for_collision(self, self.igrok) and self.s >= 30 and not self.kast_scena:
            self.s = 0
            self.igrok.hp -= 5
            print(self.igrok.hp)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.udar and self.s1 >= 60:
            self.angle -= 5
        if self.angle <= -110:
            self.s1 = 0
            self.udar = False
            self.angle = -30

        if self.s1 < 60:
            self.s1 += 1


class Shit(arcade.Sprite):
    def __init__(self, sprite):
        super().__init__()

        self.shit = load_tex_pair('nuzhno/bridgeB.png')
        self.texture = self.shit[1]
        self.scale = 0.5
        self.sprite = sprite
        self.blok = False
        self.blok_x = self.center_x + 20

    def on_update(self, delta_time: float = 1 / 60):
        if self.blok:
            self.center_x = self.blok_x
        else:
            self.position = self.sprite.position


class Igrok(arcade.Sprite):
    def __init__(self, a):
        super().__init__()
        self.hp = 100
        self.a = a

        self.scale = 1
        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")
        main_patch1 = ()
        main_patch2 = ()
        main_patch3 = ()
        main_patch4 = ()
        main_patch5 = ()
        main_patch6 = ()
        main_patch7 = ()
        self.idle_tex = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        if self.a == 0:
            if self.change_x > 0 and self.storona == 1:
                self.storona = 0
            elif self.change_x < 0 and self.storona == 0:
                self.storona = 1

            if self.change_y > 0:
                self.texture = self.jump_tex[self.storona]
            elif self.change_y < 0:
                self.texture = self.fall_tex[self.storona]

            if self.change_y == 0 and self.change_x == 0:
                self.texture = self.idle_tex[self.storona]

            if abs(self.change_x) > 0 and self.change_y == 0:
                self.sch_walk_tex += 0.2
                if self.sch_walk_tex > 7:
                    self.sch_walk_tex = 0
                self.texture = self.walk_t[int(self.sch_walk_tex)][self.storona]


class IgraViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((200, 200, 200))

        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='shederi_igra/ver_shad_tl_ogon.glsl',
                                                    fragment_shader='shederi_igra/frag_shad_tl_ogon.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.celi_milnii_list = None
        self.palka_list = None
        self.list_Vrag = None
        self.igrok = None
        self.fizika = None
        self.zem_list = None
        self.stena_list = None
        self.t_main_patch = (':resources:images/tiles/')
        self.kamera = None
        self.vrag_list = None
        self.radius = None
        self.molniya = None
        self.gnevTora = None
        self.shit = None

        self.levo = False
        self.pravo = False
        self.molniya_ataka = False
        self.beg = False

        self.skorost_igroka = SKOROST_IGROKA_WALK

        self.s = 0
        self.x = 9984
        self.kd_mol = 301

    def tl_ogon(self, x0, y0, r=0., b=0., g=0., max_t=MAX_TIME, min_t=MIN_TIME, r_x=50, r_y=50,
                dx=random.uniform(-0.15, 0.15), dy=random.uniform(0, 2)):
        # Рандомизируется координаты появления частиц
        x = random.randint(x0 - r_x, x0 + r_x)
        y = random.randint(y0 - r_y, y0 + r_y)

        # Проверка правильности цвета
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        # Генератор для частиц
        def gen_init__data(init_x, init_y, r1, g1, b1, dx1, dy1):
            fade_rate = random.uniform(1 / max_t, 1 / min_t)
            yield init_x
            yield init_y
            yield dx1
            yield dy1
            yield r1
            yield g1
            yield b1
            yield fade_rate

        x2 = x / (1600 + 0) * 2. - 1.
        y2 = y / (900 + 0) * 2. - 1.

        init_data = gen_init__data(x2, y2, r, g, b, dx, dy)

        bauffer = self.window.ctx.buffer(data=array('f', init_data))

        buffer_deskript = arcade.gl.BufferDescription(bauffer, '2f 2f 3f f', ['in_pos', 'in_vel', 'in_color',
                                                                              'in_fade_rate'])

        vao = self.window.ctx.geometry([buffer_deskript])

        chast = Chasti(buffer=bauffer, vao=vao, start_time=time.time())
        self.chasti_list.append(chast)

    def setup(self):
        self.celi_milnii_list = arcade.SpriteList()

        self.igrok = Igrok(0)
        self.igrok.center_x = KOOR_X
        self.igrok.center_y = KOOR_Y
        self.radius = arcade.Sprite("C:/Users/user/Desktop/Igra/nuzhno/radius_porazheniya.png", 0.204)
        self.palka_list = arcade.SpriteList()
        self.gnevTora = GnevTora(self.igrok.center_x, self.igrok.center_y, self.celi_milnii_list)

        self.list_Vrag = arcade.SpriteList()

        self.vrag_list = arcade.SpriteList()
        vrag = Vrag1()
        vrag.scale = 1
        vrag.position = 1300, 222
        self.vrag_list.append(vrag)
        self.celi_milnii_list.append(vrag)

        for x in range(1700, 2900, 300):
            vrag = Vrag1()
            vrag.position = x, 222
            self.vrag_list.append(vrag)
            self.celi_milnii_list.append(vrag)

        for x in range(3500, 5000, 150):
            vrag = Vrag1()
            vrag.position = x, 222
            self.vrag_list.append(vrag)
            self.celi_milnii_list.append(vrag)

        self.zem_list = arcade.SpriteList()
        for x in range(-128, 10000, 128):
            zem = arcade.Sprite(f"{self.t_main_patch}dirtMid.png")
            zem.center_x = x
            zem.center_y = 64
            self.zem_list.append(zem)

        self.stena_list = arcade.SpriteList()
        stena = arcade.Sprite(f'{self.t_main_patch}boxCrate_single.png')
        stena.position = 100, 192
        self.stena_list.append(stena)

        y = 175
        for x in range(5300, 5940, 128):
            y = y + 200 + random.randint(-100, 100)
            vrag = Vrag1()
            vrag.scale = 0.5
            vrag.position = x, y
            self.vrag_list.append(vrag)
            y = 175
            self.celi_milnii_list.append(vrag)

        vrag = Vrag1()
        vrag.scale = 0.5
        vrag.position = 7666, 175
        self.vrag_list.append(vrag)

        for x in range(6200, 7201, 1000):
            vrag = Vrag1()
            vrag.position = x, 222
            self.vrag_list.append(vrag)
            self.celi_milnii_list.append(vrag)

        for x in range(7500, 9000, 150):
            vrag = Vrag(self.igrok)
            vrag.position = x, 192
            palka = Oruzhie(self.igrok, vrag)
            self.palka_list.append(palka)
            self.list_Vrag.append(vrag)
            self.zem_list.append(vrag)
            self.celi_milnii_list.append(vrag)

        self.fizika = arcade.PhysicsEnginePlatformer(self.igrok, self.zem_list, GRAVITI, walls=self.stena_list)

        self.molniya = Molniay(self.radius, self.celi_milnii_list, self.igrok, self.molniya_ataka)

        self.shit = Shit(self.igrok)

        self.kamera = arcade.Camera(W, H)

    def on_update(self, delta_time: float):
        self.gnevTora.on_update()
        self.gnevTora.x, self.gnevTora.y = self.igrok.position
        for vrag in self.list_Vrag:
            vrag.on_update()

        if self.igrok.center_y < 0:
            self.igrok.position = KOOR_X, KOOR_Y
        self.s += 1
        self.kd_mol += 1

        if self.pravo and not self.levo:
            if self.beg:
                self.igrok.change_x = self.skorost_igroka + BEG_IGROKA
            else:
                self.igrok.change_x = self.skorost_igroka
        elif self.levo and not self.pravo:
            if self.beg:
                self.igrok.change_x = -self.skorost_igroka - BEG_IGROKA
            else:
                self.igrok.change_x = -self.skorost_igroka
        else:
            self.igrok.change_x = 0

        self.radius.position = self.igrok.position

        self.fizika.update()

    def on_draw(self):
        self.clear()

        self.vrag_list.draw()
        self.igrok.draw()
        self.igrok.update_animation()
        self.stena_list.draw()
        self.zem_list.draw()
        self.list_Vrag.draw()

        for vrag in self.list_Vrag:
            vrag.update_animation()

        self.shit.draw()

        if self.s >= 120:
            self.s = 0
            zem = arcade.Sprite(f"{self.t_main_patch}dirtMid.png")
            zem.center_x = self.x
            zem.center_y = 64
            zem.draw()
            self.x += 128
            self.zem_list.append(zem)
            fizika = arcade.PhysicsEnginePlatformer(self.igrok, self.zem_list, GRAVITI)

        arcade.draw_circle_outline(2300, 222, 500.004, arcade.color.RED, 3)
        arcade.draw_circle_outline(self.igrok.center_x, self.igrok.center_y, 500.004, RED, 5)

        if arcade.check_for_collision_with_list(self.radius, self.vrag_list):
            for vrag in self.vrag_list:
                if arcade.check_for_collision(vrag, self.radius):
                    arcade.draw_line(self.igrok.center_x, self.igrok.center_y, vrag.center_x, vrag.center_y, RED, 10)

        for cel in self.celi_milnii_list:
            if cel is not Vrag:
                cel.update_animation()

        self.molniya.update_animation()
        if self.kd_mol <= 300:
            self.molniya_ataka = False
        if self.molniya_ataka and self.kd_mol > 300:
            self.kd_mol = 0
            self.molniya_ataka = False
            self.molniya.udar = True
            self.molniya.update_animation()
            self.igrok.position = self.molniya.koordinati()

        self.gnevTora.update_animation()

        self.center_kamera_za_igrok()
        self.kamera.use()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.molniya_ataka = True

        if symbol == arcade.key.NUM_0:
            self.gnevTora.udar = True

        if symbol == arcade.key.LEFT:
            self.levo = True
        elif symbol == arcade.key.RIGHT:
            self.pravo = True

        if symbol == arcade.key.UP:
            if self.fizika.can_jump():
                self.igrok.change_y = IG_JUMP_F

        if symbol == arcade.key.RSHIFT:
            self.beg = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.NUM_0:
            self.shit.blok = False

        if _symbol == arcade.key.LEFT:
            self.levo = False
        elif _symbol == arcade.key.RIGHT:
            self.pravo = False

        if _symbol == arcade.key.RSHIFT:
            self.beg = False

    def center_kamera_za_igrok(self):
        ekran_center_x = self.igrok.center_x - self.kamera.viewport_width / 3
        ekran_center_y = self.igrok.center_y - self.kamera.viewport_height / 2

        if ekran_center_y < 0:
            ekran_center_y = 0
        if ekran_center_x < 0:
            ekran_center_x = 0

        self.kamera.move_to((ekran_center_x, ekran_center_y), 0.05)


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


okno = arcade.Window(W, H, 'Igra')
igra_viev = IgraViev()
igra_viev.setup()
okno.show_view(igra_viev)
arcade.run()