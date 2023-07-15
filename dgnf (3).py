# ver = 0.2.3
import random
import time

import arcade
import arcade.gui
from dataclasses import dataclass
from array import array
import arcade.gl

# Начальные координаты игрока
KOOR_X = 0
KOOR_Y = 292

# Размер экрана
W = 1600
H = 900

# Время для частиц
MAX_TIME = 0.8
MIN_TIME = 0.3

# Цвета
SINI = (44, 117, 255)
BEL = (255, 255, 255)
RED = (255, 0, 0)

# Физические константы
GRAVITI = 1
IG_JUMP_F = 30
SKOROST_IGROKA_WALK = 5
ENEMY_SPEED = 2
BEG_IGROKA = 20
V_VRAG = 5
BEG_VRAGA = 10
STOP = 11

# Звуковые константы
GROMKOST_MUSIC = 0.2

# Монологи
MONOLOG = ['Войны. ', 'Они длятся так долго, что мирные времена уже никто не помнит. ', 'Абсолютно каждая страна мира '
           'Асилмога, так или иначе, затянута в войны. Но никто и не хочет, чтобы настал мир, хотя бы там, где они '
           'живут. Все только радуются войнами, этим жертвам, этим смертям. ', 'И такое отношение к войнам никем не '
           'навязанное, каждый слой населения хочет войны, хочет насилия, хочет смерти. А миролюбивых и пацифистов '
           'называют наивными или предателями. ', 'Но ради чего? Ради чего, все эти войны? Ради чего, все эти жертвы? '
           'Ради чего, все эти смерти? ', 'На все эти вопросы, все отвечают одинаково: “Ради Великого Мира!”. ',
           'Воевать ради мира. ', 'Разобщаться, ненавидеть и убивать друг друга, чтобы потом объединиться, любить, '
           'дружить и помогать друг другу. ', 'Звучит тупо.' 'Война и мир – это две противоположности, как свет и'
           ' тьма, как добро и зло, как белый и чёрный. ', 'Боги же, с друг другом не ладят. Поэтому не способны '
           'остановить войны, а если и пытаются, то только подкидывают масло в огонь. ', 'Есть, ли надежда у мира '
           'Асилмога или он сгинет в войнах? ', 'Покажет только время…']
print(len(MONOLOG))

# Диалоги
DIALOG1 = ['Кто ты, странник?', 'Я Войслав, воин СЗА. А Вы кто?', 'Я Бренд, здешний командир ополченцев. Мы охраняем '
           'нашу деревню от врагов, поэтому хочу узнать: зачем ты сюда пришёл?', 'Мне было приказано устранить здешних '
           'мятежников, чтобы они не наводили смуту в нашей стране. Поэтому задам вопрос я Вам: никого тут из '
           'подозрительных не замечали?', 'Да!', 'Мы можем провести тебя до их убежища, но ты не ужели ты думаешь, '
           'что одним щитом ты их всех устранишь?', 'По пути сюда я потерял свой меч. Поэтому надеялся на помощь '
           'местных, и не зря.', 'Хе-хе-хе.', 'И вправду, не зря.. Что ж, Войслав, у меня есть меч. ', 'Но я его тебе '
           'не дам, а то вдруг по пути к убежищу предателей, ты и мой меч потеряешь. ', 'Ха-ха-ха', 'Поэтому, Войслав, я'
           ' предлагаю тебе…', 'Убежать? ', 'Я не трус, и хоть с голыми руками, но я выполни свою миссию!']

print(len(DIALOG1))


def graviti_for_platform(platform, minimum, graviti_constant, walls_list):
    if platform.bottom > minimum:
        platform.change_y -= graviti_constant
        return platform.change_y
    if arcade.check_for_collision_with_list(platform, walls_list):
        return 0, 128 + (128 * platform.scale) / 2


@dataclass
class Chasti:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


# Radius - это специальный класс для радиуса
# действий игрока, ловушек, врагов и тд.
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


class HitBoxIgrok(arcade.Sprite):
    def __init__(self, vibor):
        super().__init__()
        self.vibor = vibor

        self.scale = 1.05

        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

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


# Класс игрока
class Igrok(arcade.Sprite):
    def __init__(self, vibor):
        super().__init__()
        # Хп игрока
        self.hp = 100

        #
        self.s = 0
        self.s1 = 180

        self.hitbox_igrok = HitBoxIgrok(0)

        # В игре будет в общем 8 главных героев,
        # за которых можно будет поиграть. С помощью этой переменной указывается,
        # за какого персонажа, игрок, будет играть.
        self.vibor = vibor

        self.center_x = KOOR_X
        self.center_y = KOOR_Y
        self.scale = 1

        # Эта переменная указывает, в какую сторону
        # смотрит персонаж
        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

        self.idle_tex = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.hit_box = self.texture.hit_box_points

        self.na_taran = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.hitbox_igrok.update_animation()
        self.s1 += 1
        if self.s1 < 180:
            self.na_taran = False
        if self.na_taran:
            self.s += 1
            if self.s > 180:
                self.s = 0
            if self.s == 0:
                self.s1 = 0
                self.na_taran = False

        if self.vibor == 0:
            self.hitbox_igrok.position = self.position
            self.hitbox_igrok.change_x = self.change_x
            self.hitbox_igrok.change_y = self.change_y

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

            if self.na_taran:
                if abs(self.change_x) > 0 and self.change_y == 0:
                    self.sch_walk_tex += 1
                    if self.sch_walk_tex > 7:
                        self.sch_walk_tex = 0
                    self.texture = self.walk_t[int(self.sch_walk_tex)][self.storona]


class Vrag(arcade.Sprite):
    def __init__(self, igrok, kast_scena=False, vr_stan=150, vr_oglush=150):
        super().__init__()
        self.hp = 100

        # Переменные для контроля игрока
        self.stan = False
        self.s_stan = 0
        self.vr_stan = vr_stan
        self.oglush = False
        self.s_oglush = 0
        self.vr_oglush = vr_oglush
        self.c_y = None
        self.y_oglush = True
        self.otkid = False
        self.s_otkid = 0
        self.vr_otkid = 90
        self.s_ch_y = 0

        self.scale = 1
        self.storona = 1
        # Эта переменная, которая указывает
        # радиус перемещения врага к игроку
        self.radius_vid = Radius(3)
        # Эта переменная указывает радиус, в котором враг атакует цель
        self.radius_ataki = Radius(0)
        self.igrok = igrok
        # Эта переменная указывает, попал ли враг по цел
        self.udar = False
        # Эта переменая указывает, просходт ли каст сцена в данный момент ил нет
        self.kast_scena = kast_scena

        self.sch_walk_tex = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle[0]

        self.hit_box = self.texture.hit_box_points

    def on_update(self, delta_time: float = 1 / 60):
        self.radius_vid.position = self.radius_ataki.position = self.position
        # Эта переменная указывает растояние от позиции игрока до позиции врага
        stop = abs(self.igrok.center_x - self.radius_vid.center_x)
        if not self.kast_scena:
            # Это условие проверяет: есть ли игрк в радиусе перемещения врага, находится ли враг в стане и в оглушении
            if arcade.check_for_collision(self.radius_vid, self.igrok) and not self.stan and not self.oglush \
                    and not self.otkid:
                # Последуещие 2 условия задают направление и скорость врагу
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

            # Это условие проверяет, попал ли враг по цели
            if arcade.check_for_collision(self.radius_ataki, self.igrok):
                self.udar = True
            else:
                self.udar = False

            if self.y_oglush:
                self.c_y = self.center_y
            # Последуещие 2 условия оглушают врага
            if self.oglush and self.s_oglush <= self.vr_oglush:
                self.y_oglush = False
                self.change_x = 0
                self.change_y = 0
                self.s_oglush += 1
                self.angle = -90
                self.center_y = 128
            if self.s_oglush > self.vr_oglush:
                self.y_oglush = True
                self.oglush = False
                self.s_oglush = 0
                self.angle = 0
                self.center_y = self.c_y

            # Последуещие 2 условия станят врага
            if self.stan and self.s_stan <= self.vr_stan:
                self.change_x = 0
                self.change_y = 0
                self.s_stan += 1
            if self.s_stan > self.vr_stan:
                self.stan = False
                self.s_stan = 0

            if self.otkid and self.s_otkid <= self.vr_otkid:
                #print(1)
                self.s_otkid += 1
                if self.storona == 0:
                    self.change_x = -10
                elif self.storona == 1:
                    self.change_x = 10
                self.change_y += 0.001
                if self.s_otkid > self.vr_otkid:
                    self.otkid = False
                    self.s_otkid = 0
            else:
                self.change_y = 0
        else:
            self.change_x = 0

    def update_animation(self, delta_time: float = 1 / 60):
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
            self.sch_walk_tex += 0.2
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[int(self.sch_walk_tex)][self.storona]


# На этот класс не обращайте внимания, так как
# в будущем планируется его переработка
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

    def update_animation(self, delta_time: float = 1 / 60):
        if self.udar and self.s1 >= 60:
            self.angle -= 5
        if self.angle <= -110:
            self.s1 = 0
            self.udar = False
            self.angle = -30

        if self.s1 < 60:
            self.s1 += 1


# GnevTora - это способность
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
        self.s = 0
        self.s1 = 0
        # Эта переменна указывает, поразило ли кого-нибудь
        self.udar = False
        # Возможно эту переменную надо будет удалить
        self.drav = False

    # Эта функция будет переделана, но переделать можешь и ты
    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.drav:
            arcade.draw_circle_filled(self.x, self.y, 220, arcade.color.WHITE)
            arcade.draw_circle_outline(self.x, self.y, 235, arcade.color.BLUE, 60)
            self.drav = False

    def on_update(self, delta_time: float = 1 / 60):
        self.radius.position = self.x, self.y

        self.s += 1
        # Последующие 2 условия проверяют одна ли целт или их несколько
        if self.sprite_list is not None:
            if arcade.check_for_collision_with_list(self.radius, self.sprite_list) and self.s >= 10 and self.udar:
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self.radius, sprite):
                        sprite.oglush = True
                        sprite.hp -= 20
                        self.udar = False
                self.s = 0

        self.s1 += 1
        if self.sprite is not None:
            if arcade.check_for_collision(self.radius, self.sprite) and self.s1 >= 10 and self.udar:
                self.s1 = 0
                self.sprite.hp -= 20
                self.udar = False


# Пролог
class IgraPrologViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((255, 182, 193))

        # Переменные для частиц
        self.chasti_list = []
        self.program = self.window.ctx.load_program(vertex_shader='shederi_igra/ver_shad_tl_ogon.glsl',
                                                    fragment_shader='shederi_igra/frag_shad_tl_ogon.glsl')
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        # Динамичные спрайты
        self.igrok = None
        self.brend = None

        # Списки динамичных спрайтов
        self.vrag_sil_list = None
        self.vrag_sred_list = None
        self.vrag_slab_list = None
        self.vrag_spec_list = None
        self.vrag_list = None

        # Списки статичных спрайтов
        self.walls_list = None
        self.platforms_list = None

        # Список целей для способностей
        self.celi_molnii_list = None
        self.fizika = None

        # Списки для анимации поражения врагов(анимаций нет, они
        # просто лежат на земле либо загараживая игрока, либо нет
        self.poverzhen_list1 = None
        self.poverzhen_list2 = None

        self.hill_zele_list = None
        self.palka_list = None
        self.gnevTora = None

        # Звуковые переменные
        self.music = None
        self.music_play = None
        self.jump_sound = None
        self.jump_sound_play = None
        self.gem_sound = None
        self.gem_sound_play = None

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
        self.nachalo = True
        self.kast_scena = False
        self.next = False
        self.dialog = True
        self.ne_fight = True
        self.stay = True
        self.nataran = False

        self.perv = 0

        # Счётчики
        self.f = 0
        self.f1 = 0
        self.s = 0
        self.s_taran = 240
        self.index = 0
        self.index1 = 0
        self.timer = 0
        self.kol_hill = 0
        self.volna = 0

        # Константы
        self.skorost_igroka = SKOROST_IGROKA_WALK

        self.t_main_patch = ':resources:images/tiles/'

    def setup(self):
        self.igrok = Igrok(0)

        self.kamera = arcade.Camera(W, H)

        main_sound = ':resources:sounds/'

        self.poverzhen_list1 = arcade.SpriteList()
        self.poverzhen_list2 = arcade.SpriteList()

        self.vrag_list = arcade.SpriteList()

        self.jump_sound = arcade.load_sound(f'{main_sound}jump5.wav')

        self.gem_sound = arcade.load_sound(f'{main_sound}coin1.wav')

        # Менеджер для иконок
        self.meneger2 = arcade.gui.UIManager()
        self.meneger2.enable()
        self.text_info2 = arcade.gui.UITextArea(text=f'x {self.kol_hill}', width=40, height=50, font_name='Impact',
                                                font_size=18)
        self.v_box1 = arcade.gui.UIBoxLayout()
        self.meneger2.add(arcade.gui.UIAnchorWidget(anchor_x='left', anchor_y='bottom', child=self.v_box1))
        textur = arcade.load_texture(':resources:images/items/gemRed.png')
        hill_textur = arcade.gui.UITextureButton(texture=textur, scale=0.5)
        self.v_box1.add(hill_textur.with_space_around(right=75, bottom=-50))
        self.v_box1.add(self.text_info2.with_space_around(bottom=30, left=30))

        self.music = arcade.load_sound('nuzhno/Naruto_OST.mp3')
        self.music_play = arcade.play_sound(self.music, 0, looping=True)

        # Менеджер для монолога
        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()
        self.text_info = arcade.gui.UITextArea(text=self.text, width=1100, height=350, font_size=24, font_name='Impact',
                                               x=250, y=-30)
        self.meneger.add(self.text_info)

        # Менеджер для дилогов
        self.meneger1 = arcade.gui.UIManager()
        self.text_info1 = arcade.gui.UITextArea(text='', width=1100, height=230, font_size=24, font_name='Impact',
                                                x=250)
        self.meneger1.enable()
        self.meneger1.add(self.text_info1)
        self.v_box = arcade.gui.UIBoxLayout()
        self.meneger1.add(arcade.gui.UIAnchorWidget(anchor_x='right', anchor_y='bottom', child=self.v_box))
        kn_next = arcade.gui.UIFlatButton(text='Дальше', width=100, height=50)
        self.v_box.add(kn_next)

        @kn_next.event('on_click')
        def on_click_settings(event):
            if self.next:
                self.text = ''
                self.index += 1

        self.hill_zele_list = arcade.SpriteList(True)
        self.celi_molnii_list = arcade.SpriteList()
        self.platforms_list = arcade.SpriteList()
        self.walls_list = arcade.SpriteList(True)
        self.palka_list = arcade.SpriteList()

        # Последующие 4-е списка обозначают силу врага
        self.vrag_spec_list = arcade.SpriteList()
        self.vrag_sil_list = arcade.SpriteList()
        self.vrag_sred_list = arcade.SpriteList()
        self.vrag_slab_list = arcade.SpriteList()

        self.brend = Vrag(self.igrok, True)
        self.brend.scale = 0.9
        self.brend.position = 4200, 185
        palka = Oruzhie(self.igrok, self.brend, True)
        self.palka_list.append(palka)
        self.platforms_list.append(self.brend)
        self.vrag_list.append(self.brend)

        hill = arcade.Sprite(':resources:images/items/gemRed.png')
        hill.scale = 0.5
        hill.position = 1200, 144
        self.hill_zele_list.append(hill)

        # Спавн лечебных зелей(hill)
        for x in range(1900, 4901, 3000):
            hill = arcade.Sprite(':resources:images/items/gemRed.png')
            hill.scale = 0.5
            hill.position = x, 144
            self.hill_zele_list.append(hill)

        vrag = Vrag(self.igrok, True)
        vrag.position = 2500, 192
        palka = Oruzhie(self.igrok, vrag, True)
        self.palka_list.append(palka)
        self.vrag_slab_list.append(vrag)
        self.vrag_list.append(vrag)

        # Cпавн врагов
        for x in range(2850, 3050, 100):
            vrag = Vrag(self.igrok, True)
            vrag.scale = 1.1
            vrag.position = x, 198
            palka = Oruzhie(self.igrok, vrag, True)
            self.palka_list.append(palka)
            self.vrag_sred_list.append(vrag)
            self.vrag_list.append(vrag)

        # Cпавн врагов
        for x in range(3379, 3679, 153):
            vrag = Vrag(self.igrok, True)
            vrag.position = x, 192
            palka = Oruzhie(self.igrok, vrag, True)
            self.palka_list.append(palka)
            self.vrag_slab_list.append(vrag)
            self.vrag_list.append(vrag)

        # Cпавн врагов
        for x in range(4400, 5150, 150):
            vrag = Vrag(self.igrok, True)
            vrag.scale = 0.9
            vrag.position = x, 185
            palka = Oruzhie(self.igrok, vrag, True)
            self.palka_list.append(palka)
            self.vrag_sil_list.append(vrag)
            self.vrag_list.append(vrag)

        self.v2rag = Vrag(self.igrok, True)
        self.v2rag.position = 300, 1000
        self.k = 0

        # Генерация ландшафта
        for x in range(-128, 15000, 128):
            zem = arcade.Sprite(f"{self.t_main_patch}grassMid.png")
            zem.center_x = x
            zem.center_y = 64
            self.walls_list.append(zem)

        self.fizika = arcade.PhysicsEnginePlatformer(self.igrok, self.platforms_list, walls=self.walls_list,
                                                      gravity_constant=GRAVITI)

        self.gnevTora = GnevTora(0, 0, self.celi_molnii_list)

        for vrag in self.vrag_list:
            self.celi_molnii_list.append(vrag)

    # Функция частиц для тлеющего(а может и не только для такого) огня
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

    def on_update(self, delta_time: float):
        self.gnevTora.on_update()
        self.gnevTora.x = self.igrok.center_x
        self.gnevTora.y = self.igrok.center_y

        if self.next:
            self.timer += 1
        if self.igrok.center_x >= 300 and self.nachalo:
            self.timer = 0
            self.nachalo = False
            self.text = ''

        for vrag in self.vrag_list:
            if arcade.check_for_collision(vrag, self.igrok.hitbox_igrok) and self.igrok.na_taran:
                vrag.otkid = True

        # Счётчик для напечатания букв
        self.s += 1

        # Собирание лечебных зелей
        for hill in self.hill_zele_list:
            if arcade.check_for_collision(self.igrok, hill):
                self.hill_zele_list.remove(hill)
                self.kol_hill += 1
                self.text_info2.text = f'x {self.kol_hill}'
                self.gem_sound_play = arcade.play_sound(self.gem_sound, volume=0.2)

        global V_VRAG
        # Это условие не даёт игроку бесконечно падать
        if self.igrok.center_y < 0:
            self.igrok.position = KOOR_X, KOOR_Y

        # Эти 4 условия проверяют, может ли ходить игрок
        if self.index1 > 11 and self.igrok.center_x <= 300 and self.nachalo:
            self.igrok.change_x = self.skorost_igroka
        elif self.nachalo:
            self.igrok.change_x = 0
        elif not self.kast_scena or not self.nachalo:
            if self.igrok.na_taran:
                if self.igrok.storona == 0:
                    self.igrok.change_x = 20
                elif self.igrok.storona == 1:
                    self.igrok.change_x = -20
            elif self.pravo and not self.levo:
                if self.beg:
                    self.igrok.change_x = BEG_IGROKA
                else:
                    self.igrok.change_x = self.skorost_igroka
            elif self.levo and not self.pravo:
                if self.beg:
                    self.igrok.change_x = -BEG_IGROKA
                else:
                    self.igrok.change_x = -self.skorost_igroka
            else:
                self.igrok.change_x = 0
        elif self.kast_scena:
            self.igrok.change_x = 0

        if not self.nachalo and self.k == 0:
            self.k += 1
            self.platforms_list.append(self.v2rag)

        # Это условие помогает сделать определённую сцену
        if self.ne_fight:
            for vrag in self.vrag_slab_list:
                vrag.on_update()
                if vrag == self.vrag_slab_list[0]:
                    if 2800 < self.igrok.center_x < 3901:
                        vrag.kast_scena = False
                        V_VRAG = 4
                        if self.f == 0:
                            self.platforms_list.append(vrag)
                            self.f += 1
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5

                if vrag == self.vrag_slab_list[1]:
                    if 3700 < self.igrok.center_x < 3901:
                        vrag.kast_scena = False
                        V_VRAG = 4
                        if self.f == 3:
                            self.f += 1
                            self.platforms_list.append(vrag)
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5

                if vrag == self.vrag_slab_list[2]:
                    if 3700 < self.igrok.center_x < 3901:
                        vrag.kast_scena = False
                        V_VRAG = 4
                        if self.f == 4:
                            self.f += 1
                            self.platforms_list.append(vrag)
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5

            for vrag in self.vrag_sred_list:
                vrag.on_update()
                if vrag == self.vrag_sred_list[0]:
                    if 3300 < self.igrok.center_x < 3901:
                        vrag.kast_scena = False
                        V_VRAG = 4
                        if self.f == 1:
                            self.f += 1
                            self.platforms_list.append(vrag)
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5

                if vrag == self.vrag_sred_list[1]:
                    if 3300 < self.igrok.center_x < 3901:
                        vrag.kast_scena = False
                        V_VRAG = 4
                        if self.f == 2:
                            self.f += 1
                            self.platforms_list.append(vrag)
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5

            t = 4300
            for vrag in self.vrag_sil_list:
                vrag.on_update()
                if self.f1 < 5:
                    self.platforms_list.append(vrag)
                    self.f1 += 1

                if self.igrok.center_x > 4000:
                    if vrag.center_x > t:
                        vrag.kast_scena = False
                        V_VRAG = 4
                    else:
                        vrag.kast_scena = True
                        V_VRAG = 5
                else:
                    vrag.kast_scena = True
                    V_VRAG = 5
                t += 75

        # Если это условие срабатывает, то начинается бой
        if not self.ne_fight:
            if not self.brend.oglush or not self.brend.stan:
                self.brend.on_update()
            self.brend.kast_scena = False

            if self.brend.udar and (not self.brend.oglush or not self.brend.stan):
                for palka in self.palka_list:
                    if palka.position == self.brend.position:
                        palka.udar = True

            if self.brend.oglush and self.brend in self.platforms_list:
                self.platforms_list.remove(self.brend)
            elif self.brend not in self.platforms_list and not self.brend.oglush:
                self.platforms_list.append(self.brend)

            if len(self.vrag_list) <= 6 and self.volna == 0:
                self.volna += 1
            if self.volna == 1:
                self.volna += 1
                f = 0
                szadi = 700
                speredi = 1200
                for vrag in range(10):
                    vrag = Vrag(self.igrok)
                    if f == 0:
                        f += 1
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_sil_list.append(vrag)
                    elif 0 < f < 3:
                        f += 1
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_slab_list.append(vrag)
                    else:
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_sred_list.append(vrag)

                    palka = Oruzhie(self.igrok, vrag)
                    self.palka_list.append(palka)
                    self.platforms_list.append(vrag)
                    self.celi_molnii_list.append(vrag)
                    self.vrag_list.append(vrag)

                    szadi += 50
                    speredi += 50

            if len(self.vrag_list) <= 8 and self.volna == 2:
                self.volna += 1

            if self.volna == 3:
                self.volna += 1
                f = 0
                szadi = 700
                speredi = 1200
                for vrag in range(10):
                    vrag = Vrag(self.igrok)
                    if f == 0:
                        f += 1
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_sil_list.append(vrag)
                    elif 0 < f < 4:
                        f += 1
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_slab_list.append(vrag)
                    else:
                        if random.randint(1, 2) == 1:
                            vrag.position = self.igrok.position[0] + speredi, 193
                        else:
                            vrag.position = self.igrok.position[0] - szadi, 193
                        self.vrag_sred_list.append(vrag)

                    palka = Oruzhie(self.igrok, vrag)
                    self.palka_list.append(palka)
                    self.platforms_list.append(vrag)
                    self.celi_molnii_list.append(vrag)
                    self.vrag_list.append(vrag)

                    szadi += 50
                    speredi += 50

            for palka in self.palka_list:
                palka.on_update()
                palka.kast_scena = False

            for vrag in self.vrag_sred_list:
                vrag.on_update()
                vrag.kast_scena = False

                if vrag.udar:
                    for palka in self.palka_list:
                        if vrag.position == palka.position:
                            palka.udar = True

                if vrag.oglush and vrag in self.platforms_list:
                    self.platforms_list.remove(vrag)
                elif vrag not in self.platforms_list and not vrag.oglush:
                    self.platforms_list.append(vrag)

                if vrag.hp <= 0:
                    vrag.angle = -90
                    vrag.center_y = 128
                    for palka in self.palka_list:
                        if palka.position == vrag.position:
                            self.palka_list.remove(palka)

                    if random.randint(1, 2) == 1:
                        self.poverzhen_list1.append(vrag)
                    else:
                        self.poverzhen_list2.append(vrag)

                    if self.celi_molnii_list:
                        self.celi_molnii_list.remove(vrag)
                    if vrag in self.platforms_list:
                        self.platforms_list.remove(vrag)
                    if vrag in self.vrag_list:
                        self.vrag_list.remove(vrag)
                    if vrag in self.vrag_sred_list:
                        self.vrag_sred_list.remove(vrag)

            for vrag in self.vrag_slab_list:
                vrag.on_update()
                vrag.kast_scena = False

                if vrag.udar:
                    for palka in self.palka_list:
                        if vrag.position == palka.position:
                            palka.udar = True

                if vrag.oglush and vrag in self.platforms_list:
                    self.platforms_list.remove(vrag)
                elif vrag not in self.platforms_list and not vrag.oglush:
                    self.platforms_list.append(vrag)

                if vrag.hp <= 0:
                    vrag.angle = -90
                    vrag.center_y = 128
                    for palka in self.palka_list:
                        if palka.position == vrag.position:
                            self.palka_list.remove(palka)

                    if random.randint(1, 2) == 1:
                        self.poverzhen_list1.append(vrag)
                    else:
                        self.poverzhen_list2.append(vrag)

                    if self.celi_molnii_list:
                        self.celi_molnii_list.remove(vrag)
                    if vrag in self.platforms_list:
                        self.platforms_list.remove(vrag)
                    if vrag in self.vrag_list:
                        self.vrag_list.remove(vrag)
                    if vrag in self.vrag_slab_list:
                        self.vrag_slab_list.remove(vrag)

            for vrag in self.vrag_sil_list:
                vrag.on_update()
                vrag.kast_scena = False

                if vrag.udar:
                    for palka in self.palka_list:
                        if vrag.position == palka.position:
                            palka.udar = True

                if vrag.oglush and vrag in self.platforms_list:
                    self.platforms_list.remove(vrag)
                elif vrag not in self.platforms_list and not vrag.oglush:
                    self.platforms_list.append(vrag)

                if vrag.hp <= 0:
                    vrag.angle = -90
                    vrag.center_y = 128
                    for palka in self.palka_list:
                        if palka.position == vrag.position:
                            self.palka_list.remove(palka)

                    if random.randint(1, 2) == 1:
                        self.poverzhen_list1.append(vrag)
                    else:
                        self.poverzhen_list2.append(vrag)

                    if self.celi_molnii_list:
                        self.celi_molnii_list.remove(vrag)
                    if vrag in self.platforms_list:
                        self.platforms_list.remove(vrag)
                    if vrag in self.vrag_list:
                        self.vrag_list.remove(vrag)
                    if vrag in self.vrag_sil_list:
                        self.vrag_sil_list.remove(vrag)

        # Если это условие срабатывает, то начинается каст сцена
        if self.igrok.center_x > 4000 and not self.kast_scena and self.dialog:
            self.kast_scena = True
            self.dialog = False

        self.fizika.update()
        for plat in self.platforms_list:
            plat.change_y = graviti_for_platform(plat, 128, 1, self.walls_list)

        temp_list = self.chasti_list.copy()
        for chast in temp_list:
            if time.time() - chast.start_time > MAX_TIME:
                self.chasti_list.remove(chast)

    def on_draw(self):
        self.clear()

        global MONOLOG
        global DIALOG1

        # Прорисовка домов
        for dom in range(2400, 8000, 700):
            arcade.draw_rectangle_filled(dom, 253, 300, 350, arcade.color.BROWN)

        for vrag in self.vrag_sred_list:
            vrag.update_animation()
        for vrag in self.vrag_sil_list:
            vrag.update_animation()
        for vrag in self.vrag_slab_list:
            vrag.update_animation()

        self.platforms_list.draw()
        self.celi_molnii_list.draw()
        self.brend.draw()
        self.brend.update_animation()
        self.poverzhen_list1.draw()

        self.igrok.draw()
        self.igrok.update_animation()

        self.hill_zele_list.draw()
        self.poverzhen_list2.draw()
        self.palka_list.draw()
        for palka in self.palka_list:
            palka.update_animation()

        self.walls_list.draw()

        # Это условие прорисовывает диалоговые окна
        if self.kast_scena:
            x = self.center_kamera_za_igrok(True)
            arcade.draw_rectangle_filled(x + 800, 150, 1200, 200, (0, 0, 0))
            self.meneger1.draw()
            # Каждые два кадра к менеджеру прибавляется одна буква
            if self.index > 13:
                self.kast_scena = False
                self.ne_fight = False
                return

            if self.s >= 2:
                self.s = 0
                for i in DIALOG1[self.index]:
                    self.text += i
                    self.text_info1.text = self.text
                    DIALOG1[self.index] = DIALOG1[self.index].replace(i, '', 1)
                    break

            if len(DIALOG1[self.index]) <= 0:
                self.next = True
            # Каждые два кадра к менеджеру прибавляется одна буква
            if self.s >= 2:
                self.s = 0
                for i in DIALOG1[self.index]:
                    self.text += i
                    self.text_info1.text = self.text
                    DIALOG1[self.index] = DIALOG1[self.index].replace(i, '', 1)
                    break

            if len(DIALOG1[self.index]) == 0:
                self.next = True

        if self.index >= 14:
            self.kast_scena = False
            if self.ne_fight:
                self.brend.vr_oglush = 600
                self.brend.oglush = True
            self.ne_fight = False

        self.tl_ogon(30, 60, r_x=15, r_y=15, min_t=0.1, max_t=0.4, dx=random.uniform(-0.1, 0.1), dy=random.uniform(0, 0.8))

        self.window.ctx.point_size = 10 * self.window.get_pixel_ratio()

        for chast in self.chasti_list:
            self.program['time'] = time.time() - chast.start_time
            chast.vao.render(self.program, mode=self.window.ctx.POINTS)

        self.gnevTora.draw()

        self.meneger2.draw()

        # Это условие прорисовывает монологовые окна.
        # Тот же принцип, как у диалоговых
        if self.nachalo:
            if self.index1 < 12:
                x = self.center_kamera_za_igrok(True)
                if self.index1 == 0:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (255, 0, 0))
                elif self.index1 == 1:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (200, 0, 0))
                elif self.index1 == 2:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (255, 165, 0))
                elif self.index1 == 3:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (255, 255, 0))
                elif self.index1 == 4:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (0, 255, 0))
                elif self.index1 == 5:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (0, 200, 0))
                elif self.index1 == 6:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (66, 170, 255))
                elif self.index1 == 7:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (0, 0, 255))
                elif self.index1 == 8:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (0, 0, 200))
                elif self.index1 == 9:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (139, 0, 255))
                elif self.index1 == 10:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (255, 255, 255))
                elif self.index1 == 11:
                    arcade.draw_rectangle_filled(800, 450, 1600, 900, (0, 0, 0))

                arcade.draw_rectangle_filled(x + 800, 200, 1200, 300, (20, 20, 20))
                self.meneger.draw()

                if len(MONOLOG[self.index1]) <= 0:
                    self.next = True
                    if self.timer >= 300:
                        self.text = ''
                        self.timer = 0
                        self.index1 += 1
                        self.next = False

                if self.index1 == 0:
                    g = 3
                else:
                    g = 2
                if self.s >= g:
                    self.s = 0
                    for i in MONOLOG[self.index1]:
                        self.text += i
                        self.text_info.text = self.text
                        MONOLOG[self.index1] = MONOLOG[self.index1].replace(i, '', 1)
                        break

            if self.index1 > 11:
                self.text = ''

                self.next = False
                return

        self.center_kamera_za_igrok()
        self.kamera.use()

    def on_key_press(self, symbol: int, modifiers: int):
        # С пмощью левого шифта используетя способность "Гнев Тора"
        if symbol == arcade.key.LSHIFT:
            if not self.ne_fight:
                self.gnevTora.udar = True

        if symbol == arcade.key.Q:
            self.igrok.na_taran = True

        dialog1 = []
        for i in DIALOG1:
            dialog1.append(i)

        # При нажатии на ENTER скипываютя монологи и диалоги
        if symbol == arcade.key.ENTER:
            if self.nachalo:
                self.timer = 0
                self.text = ''
                self.index1 += 1
            if self.kast_scena:
                if self.next:
                    self.text = ''
                    self.index += 1

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.levo = True
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.pravo = True

        if not self.nachalo:
            if not self.kast_scena:
                if symbol == arcade.key.W or symbol == arcade.key.UP:
                    if self.fizika.can_jump():
                        self.igrok.change_y = IG_JUMP_F
                        self.jump_sound_play = arcade.play_sound(self.jump_sound, volume=0.5)

        if symbol == arcade.key.RSHIFT:
            self.beg = True

        if symbol == arcade.key.ESCAPE:
            arcade.set_background_color(arcade.color.GRAY)
            global pause
            okno.show_view(pause)

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.levo = False
        elif _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pravo = False

        if _symbol == arcade.key.RSHIFT:
            self.beg = False

    # Эта функция позволяет камере, почти, всегда следовать за игроком
    def center_kamera_za_igrok(self, x=False, y=False):
        ekran_center_x = self.igrok.center_x - self.kamera.viewport_width / 3
        ekran_center_y = self.igrok.center_y - self.kamera.viewport_height / 2

        if ekran_center_y < 0:
            ekran_center_y = 0
        if ekran_center_x < 0:
            ekran_center_x = 0

        self.kamera.move_to((ekran_center_x, ekran_center_y), 0.1)

        if x:
            return ekran_center_x
        if y:
            return ekran_center_y


class MenyuStartaViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        # Менеджер для глав меню
        self.meneger = None
        self.v_box = None

        # Менеджер для настроек
        self.meneger1 = None
        self.v_box1 = None

        self.setting = False

    def on_show_view(self):
        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.meneger.add(arcade.gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.v_box))

        zag = arcade.gui.UITextArea(text='Игра', width=190, height=200, font_size=64, font_name='Impact',
                                    text_color=(0, 0, 0))
        self.v_box.add(zag.with_space_around(bottom=100))

        nachat = arcade.gui.UIFlatButton(text='Начать', width=400, height=80)
        self.v_box.add(nachat.with_space_around(bottom=40))
        setting = arcade.gui.UIFlatButton(text='Настройки', width=400, height=80)
        self.v_box.add(setting.with_space_around(bottom=40))
        viti = arcade.gui.UIFlatButton(text='Выйти', width=400, height=80)
        self.v_box.add(viti)

        @nachat.event('on_click')
        def knopka_nach(event):
            arcade.set_background_color((255, 182, 193))
            global igra_viev
            igra_viev.setup()
            okno.show_view(igra_viev)

        @setting.event('on_click')
        def knopka_setting(event):
            self.setting = not self.setting

        @viti.event('on_click')
        def knopka_viti(event):
            arcade.close_window()

        self.meneger1 = arcade.gui.UIManager()
        self.meneger1.enable()
        self.v_box1 = arcade.gui.UIBoxLayout()
        self.meneger1.add(arcade.gui.UIAnchorWidget(anchor_x='left', anchor_y='top', child=self.v_box1))

        nazad = arcade.gui.UIFlatButton(text='Назад', width=190, height=50, y=850)
        self.meneger1.add(nazad)

        zvuki = arcade.gui.UIFlatButton(text='Звуки и музыка', width=350, height=70)
        self.v_box1.add(zvuki.with_space_around(top=220))

        @nazad.event('on_click')
        def kn_nazad(event):
            self.setting = not self.setting

    def on_draw(self):
        self.clear()

        if self.setting:
            arcade.draw_rectangle_outline(975, 450, 1240, 890, (80, 80, 80), 10)
            self.meneger1.draw()
        else:
            self.meneger.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            arcade.set_background_color((255, 182, 193))
            global igra_viev
            igra_viev.setup()
            okno.show_view(igra_viev)


class PauseViev(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        # Менеджер для глав меню
        self.meneger = None
        self.v_box = None

        # Менеджер для настроек
        self.meneger1 = None
        self.v_box1 = None

        self.setting = False

    def on_show_view(self):
        self.meneger = arcade.gui.UIManager()
        self.meneger.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.meneger.add(arcade.gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.v_box))

        zag = arcade.gui.UITextArea(text='Пауза', width=215, height=200, font_size=64, font_name='Impact',
                                    text_color=(0, 0, 0))
        self.v_box.add(zag.with_space_around(bottom=100))

        nachat = arcade.gui.UIFlatButton(text='Начать', width=400, height=80)
        self.v_box.add(nachat.with_space_around(bottom=40))
        setting = arcade.gui.UIFlatButton(text='Настройки', width=400, height=80)
        self.v_box.add(setting.with_space_around(bottom=40))
        viti = arcade.gui.UIFlatButton(text='Выйти', width=400, height=80)
        self.v_box.add(viti)

        @nachat.event('on_click')
        def knopka_nach(event):
            arcade.set_background_color((255, 182, 193))
            global igra_viev
            okno.show_view(igra_viev)

        @setting.event('on_click')
        def knopka_setting(event):
            self.setting = not self.setting

        @viti.event('on_click')
        def knopka_viti(event):
            arcade.close_window()

        self.meneger1 = arcade.gui.UIManager()
        self.meneger1.enable()
        self.v_box1 = arcade.gui.UIBoxLayout()
        self.meneger1.add(arcade.gui.UIAnchorWidget(anchor_x='left', anchor_y='top', child=self.v_box1))

        nazad = arcade.gui.UIFlatButton(text='Назад', width=200, height=50, y=850)
        self.meneger1.add(nazad)

        zvuki = arcade.gui.UIFlatButton(text='Звуки и музыка', width=350, height=70)
        self.v_box1.add(zvuki.with_space_around(top=220))

        @nazad.event('on_click')
        def kn_nazad(event):
            self.setting = not self.setting

    def on_draw(self):
        self.clear()

        if self.setting:
            arcade.draw_rectangle_outline(975, 450, 1240, 890, (80, 80, 80), 10)
            self.meneger1.draw()
        else:
            self.meneger.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            arcade.set_background_color((255, 182, 193))
            global igra_viev
            igra_viev.setup()
            okno.show_view(igra_viev)


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


okno = arcade.Window(W, H, 'Igra')

igra_viev = IgraPrologViev()
menyu = MenyuStartaViev()
pause = PauseViev()

okno.show_view(menyu)
arcade.run()
