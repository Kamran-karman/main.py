import arcade
import hit_box_and_radius
import math
import random

MOL_BLUE = (44, 117, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

ZASHCITA = 0
ORUZHIE = 1


# Стихия молнии
class Molniay(arcade.Sprite):
    def __init__(self, sprite_list, igrok):
        super().__init__()
        self.uron = 250
        self.d = 0

        self.radius = hit_box_and_radius.Radius()
        self.sprite_list = sprite_list
        self.igrok = igrok

        self.slovar = {}
        self.s1 = 0

        self.en_x = 0
        self.en_y = 0
        self.udar = False
        self.s = 0
        self.s_kd = 300

    def update_animation(self, delta_time: float = 1 / 60):
        statistika = []
        if self.s1 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s1 += 1

        self.radius.position = self.igrok.position
        self.s_kd += 1
        if self.s_kd < 300:
            self.udar = False

        if self.s <= 3 and self.udar and self.s_kd >= 300:
            spisok_rast = []
            spisok_xy = []
            spisok3 = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite=sprite):
                    poz_x, poz_y = abs(sprite.center_x - self.igrok.center_x), \
                        abs(sprite.center_y - self.igrok.center_y)
                    pozi = (poz_x, poz_y)
                    spisok_rast.append(pozi)
                    x, y = sprite.center_x, sprite.center_y
                    xy = (x, y)
                    spisok_xy.append(xy)
            if len(spisok_rast) == 0:
                self.en_x, self.en_y = self.igrok.position
            elif len(spisok_rast) > 0:
                stx, sty = self.igrok.position
                en = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[en]
                spisok3.append(spisok_xy[en])
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        for pos in self.slovar:
                            if pos == sprite and not self.slovar[pos]:
                                self.slovar[pos] = True
                                sprite.hp -= self.uron
                                self.d += 1
                                break

                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                arcade.draw_circle_filled(stx, sty, 50, MOL_BLUE)
                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, arcade.color.WHITE)
                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                w = 0
                print('111', spisok_rast, '|__|__|', spisok_xy, '|__|__|', spisok3, '111')
                while w < 3:
                    if radius.check_collision(sprite_list=self.sprite_list):
                        if self.igrok.position == (stx, sty):
                            pred_poz = 0, 0
                        else:
                            pred_poz = stx, sty
                        spisok_rast = []
                        spisok_xy = []
                        for sprite in self.sprite_list:
                            if radius.check_collision(sprite) and sprite.position != radius.position \
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
                                    spisok_rast.append(pozi)
                                    spisok_xy.append(xy)
                        print('222', spisok_rast, '|__|__|', spisok_xy, '|__|__|', spisok3, '222')
                        if len(spisok_rast) == 0:
                            if stx > enx:
                                self.en_x, self.en_y = enx - 150, eny + 50
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 150, eny + 50
                            break
                        elif w == 2 and len(spisok_rast) != 0:
                            en = spisok_rast.index(min(spisok_rast))
                            stx, sty = radius.position
                            enx, eny = spisok_xy[en]
                            for sprite in self.sprite_list:
                                if sprite.position == (enx, eny):
                                    for pos in self.slovar:
                                        if pos == sprite and not self.slovar[pos]:
                                            self.slovar[pos] = True
                                            sprite.hp -= self.uron
                                            #self.d += 1
                                            break

                            arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                            arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                            arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                            arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                            print('333', spisok_rast, '|__|__|', spisok_xy, '|__|__|', spisok3, '333')
                            if stx > enx:
                                self.en_x, self.en_y = enx - 150, eny + 50
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 150, eny + 50
                            break
                        else:
                            if len(spisok_rast) != 0:
                                en = spisok_rast.index(min(spisok_rast))
                                stx, sty = radius.position
                                enx, eny = spisok_xy[en]
                                spisok3.append(spisok_xy[en])
                                for sprite in self.sprite_list:
                                    if sprite.position == (enx, eny):
                                        for pos in self.slovar:
                                            if pos == sprite and not self.slovar[pos]:
                                                self.slovar[pos] = True
                                                sprite.hp -= self.uron
                                                #self.d += 1
                                                break

                                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                                arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                                arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                                radius.position = enx, eny
                                print('444', spisok_rast, '|__|__|', spisok_xy, '|__|__|', spisok3, '444')
                    w += 1

        if self.s > 3:
            print(self.d)
            print(statistika)
            self.udar = False
            self.s_kd = 0
        if self.udar and self.s_kd >= 300:
            self.s += 1
        elif not self.udar:
            self.s = 0
            for i in self.slovar:
                self.slovar[i] = False

    def koordinati(self):
        return (self.en_x, self.en_y)


class GnevTora(arcade.Sprite):
    def __init__(self, sprite_list, pers):
        super().__init__()
        self.uron = 300

        # Эта переменная указывает список целей
        self.sprite_list = sprite_list

        self.slovar = {}
        self.s3 = 0

        # Эта переменая - радиус поражения
        self.radius = hit_box_and_radius.Radius(0.5)
        self.pers = pers

        # Счётчики
        self.s2 = 0
        self.s = 301
        self.s1 = 0

        # Эта переменна указывает, поразило ли кого-нибудь
        self.udar = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.s += 1
        if self.s <= 300:
            self.udar = False
        if self.udar and self.s2 < 3 and self.s > 300:
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 250, MOL_BLUE)
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, arcade.color.WHITE)

        if self.s2 >= 3:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s2 += 1
        elif not self.udar:
            self.s2 = 0

    def on_update(self, delta_time: float = 1 / 60):
        self.radius.position = self.pers.position

        if self.s3 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s3 += 1

        for sprite in self.sprite_list:
            if arcade.check_for_collision(self.radius, sprite) and self.udar:
                for i in self.slovar:
                    if i == sprite and not self.slovar[i]:
                        self.slovar[i] = True
                        sprite.hp -= self.uron

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False


class StreliPeruna(arcade.Sprite):
    def __init__(self, sprite_list, igrok):
        self.uron = 100

        super().__init__()
        self.sprite_list = sprite_list
        self.igrok = igrok

        self.slovar = {}
        self.s2 = 0

        self.rad = hit_box_and_radius.Radius(2.5)

        self.s = 0
        self.s1 = 180

        self.udar = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.rad.position = self.igrok.position
        if self.s2 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s2 += 1

        self.s1 += 1
        if self.s1 < 300:
            self.udar = False

        if self.udar and arcade.check_for_collision_with_list(self.rad, self.sprite_list):
            spis_pos = []
            spis1 = []
            spis_xy = []
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self.rad, sprite):
                    spis_pos.append(sprite.position)
                    rx = abs(self.igrok.center_x - sprite.center_x)
                    ry = abs(self.igrok.center_y - sprite.center_y)
                    rast = math.hypot(rx, ry)
                    spis_xy.append((rx, ry))
                    spis1.append(rast)

            for i in spis1:
                if len(spis1) > 5:
                    index = spis1.index(max(spis1))
                    spis_pos.pop(index)
                    spis1.remove(max(spis1))
                    spis_xy.pop(index)
                elif len(spis1) < 1:
                    return
                else:
                    break

            stx, sty = self.rad.position

            while len(spis1) >= 1:
                enx, eny = min(spis_pos)
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.s == 0 and self.udar:
                        for i in self.slovar:
                            if i == sprite and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= self.uron
                                break

                spis1.remove(spis1[spis_pos.index(min(spis_pos))])
                spis_pos.remove(min(spis_pos))

        if self.s >= 4:
            self.udar = False
            self.s1 = 0
        if self.udar:
            self.s += 1
        elif not self.udar:
            for i in self.slovar:
                self.slovar[i] = False
            self.s = 0


class SharMolniay(arcade.Sprite):
    def __init__(self, igrok, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list
        self.igrok = igrok


# Стихия ветра
class VeterOtalkivanie(arcade.Sprite):
    def __init__(self, igok, sprite_list):
        super().__init__()
        self.uron = 4

        self.igrok = igok
        self.sprite_list = sprite_list
        self.slovar = {}
        self.s3 = 0

        self.udar = False
        self.atak = False
        self.d = True
        self.s = 0
        self.s1 = 300

        self.rad = hit_box_and_radius.Radius(0.5)
        platfo = arcade.SpriteList()
        platfo.append(self.rad)
        for i in range(100):
            rad = hit_box_and_radius.Radius(0.5)
            platfo.append(rad)
        i = arcade.Sprite('nuzhno/radius_porazheniya.png')
        self.fizika = arcade.PhysicsEnginePlatformer(i, platfo)

    def on_update(self, delta_time: float = 1 / 60):
        if self.s3 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s3 += 1

        self.s1 += 1

        if self.s1 < 300 and not self.d:
            self.udar = False
        else:
            self.d = True

        if self.s1 >= 300 and self.s == 1:
            self.s1 = 0

        if self.udar:
            start = self.igrok.position
            if self.rad.change_x == 0:
                self.rad.position = start

            if self.igrok.storona == 0 and not self.atak:
                self.atak = True
                self.rad.change_x = 10
            elif self.igrok.storona == 1 and not self.atak:
                self.atak = True
                self.rad.change_x = -10
        else:
            self.d = False
            self.atak = False
            self.rad.change_x = 0
            self.s = 0

        if self.s >= 120:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s += 1

        for sprite in self.sprite_list:
            if arcade.check_for_collision(self.rad, sprite) and self.udar:
                for i in self.slovar:
                    if i == sprite and not self.slovar[i]:
                        self.slovar[i] = True
                        sprite.hp -= self.uron

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

        self.fizika.update()

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.s > 0:
            self.rad.draw()


# Ближний юой
class Mech(arcade.Sprite):
    def __init__(self, pers, sprite_list, storona, v_ataki=(30, 10)):
        super().__init__()
        self.uron = 50

        self.pers = pers
        self.sprite_list = sprite_list
        self.storona = storona

        self.s = 0
        self.s1 = 30
        self.kd = v_ataki[0]
        self.kd1 = v_ataki[1]

        self.slovar = {}

        self.udar_tex0 = arcade.load_texture_pair('nuzhno/udar.png')
        self.udar_tex1 = arcade.load_texture_pair('nuzhno/udar1.png')
        self.texture = self.udar_tex0[1]
        self.scale = 1.5

        self.udar = False
        self.s_udar = 0

    def on_update(self, delta_time: float = 1 / 60):
        if self.s == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s += 1
        if self.s1 <= self.kd or self.pers.minus_hp:
            self.udar = False
        if self.udar:
            self.s_udar += 1
        if self.s_udar > self.kd1:
            self.s_udar = 0
            self.udar = False
            self.s1 = 0

        if self.udar:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and not sprite.block1:
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            r = 10
                            if sprite.reakciay < self.pers.reakciay:
                                if sprite.reakciay * r <= self.pers.reakciay:
                                    self.slovar[i] = True
                                    sprite.hp -= self.uron
                                else:
                                    r -= 0.1
                                    shanc = 100
                                    while r > 0:
                                        if sprite.reakciay * r <= self.pers.reakciay < sprite.reakciay * r + 0.1:
                                            if random.randint(1, shanc) == 2:
                                                self.slovar[i] = True
                                                sprite.hp -= self.uron
                                            else:
                                                sprite.block = True
                                        r -= 0.1
                                        shanc -= 1
                            elif sprite.reakciay > self.pers.reakciay:
                                if self.pers.reakciay * r <= sprite.reakciay:
                                    sprite.block = True
                                else:
                                    r -= 0.1
                                    shanc = 100
                                    while r > 0:
                                        if self.pers.reakciay * r <= sprite.reakciay < self.pers.reakciay * r + 0.1:
                                            if random.randint(1, shanc) == 2:
                                                sprite.block = True
                                            else:
                                                self.slovar[i] = True
                                                sprite.hp -= self.uron
                                        r -= 0.1
                                        shanc -= 1

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

        self.s1 += 1

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.pers.storona == 0:
            self.texture = self.udar_tex0[0]
        else:
            self.texture = self.udar_tex1[0]


class Shchit(arcade.Sprite):
    def __init__(self, pers, sprite_list):
        super().__init__()
        self.pers = pers
        self.sprite_list = sprite_list
        self.scale = 0.5
        self.tex_shcit = arcade.load_texture_pair('nuzhno/shcit.png')
        self.tex_udar = arcade.load_texture_pair('nuzhno/shcit_udar.png')
        self.texture = self.tex_shcit[1]
        self.zashcita = ZASHCITA

        self.block = False
        self.block1 = False
        self.sila = False
        self.udar = False

        self.slovar = {}

        self.s = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if self.pers.udar:
            self.udar = True
        else:
            self.udar = False

        self.center_y = self.pers.center_y
        if not self.udar:
            self.center_y = self.pers.center_y
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 10
            else:
                self.center_x = self.pers.center_x + 10
        else:
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 50
            else:
                self.center_x = self.pers.center_x + 50

        if self.s == 0:
            self.s += 1
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})

        if len(self.slovar) < len(self.sprite_list):
            self.slovar.clear()
            self.s = 0

        if self.udar:
            self.block = self.block1 = False
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= 40
            return

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

        if self.block1:
            self.pers.block1 = True
        else:
            self.pers.block1 = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.udar:
            self.block = self.block1 = False
            self.texture = self.tex_udar[self.pers.storona]

        if self.block or self.block1:
            self.texture = self.tex_shcit[self.pers.storona]


class Block:
    def __init__(self, pers):
        pass



