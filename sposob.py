import arcade
import hit_box_and_radius
import math
import random

MOL_BLUE = (44, 117, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

ZASHCHITA = 0
COLD_ORUZHIE = 1
DVURUCH_MECH = 1.1
DAL_ORUZH = 2
STIHIYA = 3
FIZ_SPOSOB = 4
RIVOK = 4.1

# ___SharMolniay___
SKOROST_SHAR_MOLNII = 20
URON_SHAR_MOL = 25
URON1_SHAR_MOL = 5

S_KD_SHAR_MOLNII = 300
MAX_S_ZARYAD = 420
MAX_BAF_S_ZARYAD = 300
S_DO_PROMAH = 45

VZRIV_BAF_URON = 1.5
PROMAH_DEBAF_URON = 1.5
BAF_URON = 19.067
# ______________________

# ___Rivok___
S_KD_RIVOK = 180
# ______________________

# ___Shcit___
URON_SHCHIT = 40
# ______________________

# ___DvuruchMech___
URON_DVURUCH_MECH = 100
# ______________________


class Sposob(arcade.Sprite):
    def __init__(self, pers, sprite_list):
        super().__init__()
        self.pers = pers
        self.sprite_list = sprite_list

        self.action = False

        self.timer_for_s = 0
        self.timer_for_s_kd = 0

        self.s = 0
        self.s_kd = 0

        self.tip = {}


class Mobilnost(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = {FIZ_SPOSOB: 0.0}

        self.scale = self.pers.scale


class Fight(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 0
        
        self.slovar = {}
        
    def update_slovar(self):
        if len(self.slovar) != len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})

        if not self.action:
            for i in self.slovar:
                self.slovar[i] = False

    def update_position(self):
        self.position = self.pers.position

    def udar(self, sprite):
        for i in self.slovar:
            if i == sprite and not self.slovar[i]:
                self.slovar[i] = True
                sprite.hp -= self.uron


class ColdOruzhie(Fight):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)
        self.tip = {COLD_ORUZHIE: 0}

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture0 = None
        self.udar_texture1 = None

    def kd_timer(self):
        self.s_kd += 1

        if self.s_kd <= self.timer_for_s_kd:
            self.action = False

        if self.action:
            self.s += 1
            if self.s > self.timer_for_s:
                self.action = False
                self.s_kd = 0
                self.s = 0


class FizSposobFight(Fight):
    def __init__(self, pers, sprite_list, uron, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)
        self.tip = {FIZ_SPOSOB: 0}

        self.uron = uron

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = self.pers.udar_texture

        self.scale = self.pers.scale

    def kd_timer(self):
        self.s_kd += 1

        if self.s_kd <= self.timer_for_s_kd:
            self.action = False

        if self.action:
            self.s += 1
            if self.s > self.timer_for_s:
                self.action = False
                self.s_kd = 0
                self.s = 0

    def update_scale(self):
        self.scale = self.pers.scale


class Stihiya(Fight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = {STIHIYA: 0}

        self.radius = None
        self.radius: hit_box_and_radius.Radius

        self.kd = True

    def update_radius_position(self):
        self.radius.position = self.position

    def kd_timer(self):
        self.s_kd += 1
        if self.s_kd > self.timer_for_s_kd:
            self.kd = False

        if self.kd:
            self.action = False

        if self.s > self.timer_for_s:
            self.kd = True
            self.action = False
            self.s = 0

        if self.action:
            self.s += 1
        if self.action and self.s == 1:
            self.s_kd = 0


class Molniya(Stihiya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.timer_for_s = 3


# Физические способности


class Rivok(Mobilnost):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip[FIZ_SPOSOB] = RIVOK

        self.rivok_tex = (
            arcade.load_texture_pair(':resources:images/animated_characters/male_person/malePerson_walk7.png'))

        self.texture = self.rivok_tex[1]

        self.radius_stop = hit_box_and_radius.KvadratRadius(self.scale)
        self.stop1 = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.s_kd += 1
        if self.s_kd < S_KD_RIVOK:
            self.action = False

        self.radius_stop.position = self.position
        if not self.action:
            self.position = self.pers.position

        for drug in self.pers.v_drug_list:
            if drug != self.pers:
                if (self.radius_stop.check_collision(drug.kvadrat_radius) and
                        abs(self.radius_stop.center_x - self.pers.igrok.center_x) >
                        abs(drug.center_x - self.pers.igrok.center_x)):
                    self.stop1 = True
                    self.action = False
                    self.change_x = 0

        if (self.radius_stop.check_collision(sprite_list=self.pers.sprite_list)
                or self.radius_stop.check_collision(self.pers.igrok)):
            self.stop1 = True
            self.action = False
            self.change_x = 0

        if self.stop1:
            self.s_kd = 0
            self.change_x = 0
            self.action = False
            self.s = 0

        if self.pers.storona == 0 and self.action:
            self.change_x = 50
            self.stop1 = False
        elif self.pers.storona == 1 and self.action:
            self.change_x = -50
            self.stop1 = False

        if self.action:
            self.s += 1
        if self.s > 20:
            self.s_kd = 0
            self.change_x = 0
            self.stop1 = True
            self.action = False
            self.s = 0

        self.pers.rivok = self.action

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.rivok_tex[self.pers.storona]

    def return_positoin(self):
        return self.position


class Udar(FizSposobFight):
    def __init__(self, pers, sprite_list, uron, timer_for_s=10, timer_for_s_kd=30):
        super().__init__(pers, sprite_list, uron, timer_for_s, timer_for_s_kd)

        self.s_kd = self.timer_for_s_kd + 5

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_scale()
        self.update_position()
        self.update_slovar()

        self.kd_timer()

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar(sprite)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.udar_texture[self.pers.storona]


# Стихия молнии


class CepnayaMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 250

        self.en_x = 0
        self.en_y = 0

        self.radius = hit_box_and_radius.Radius()

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_slovar()
        self.update_radius_position()

        self.kd_timer()

        if self.action:
            spisok_rast = []
            spisok_xy = []
            spisok3 = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite=sprite):
                    poz_x, poz_y = abs(sprite.center_x - self.pers.center_x), \
                        abs(sprite.center_y - self.pers.center_y)
                    pozi = (poz_x, poz_y)
                    spisok_rast.append(pozi)
                    x, y = sprite.center_x, sprite.center_y
                    xy = (x, y)
                    spisok_xy.append(xy)
            if len(spisok_rast) == 0:
                self.en_x, self.en_y = self.pers.position
            elif len(spisok_rast) > 0:
                stx, sty = self.pers.position
                en = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[en]
                spisok3.append(spisok_xy[en])
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        self.udar(sprite)

                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                arcade.draw_circle_filled(stx, sty, 50, MOL_BLUE)
                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, arcade.color.WHITE)
                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                w = 0

                while w < 3:
                    if radius.check_collision(sprite_list=self.sprite_list):
                        if self.pers.position == (stx, sty):
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
                                    self.udar(sprite)

                            arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                            arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                            arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                            arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
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
                                        self.udar(sprite)

                                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                                arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                                arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                                radius.position = enx, eny
                    w += 1

    def return_position(self):
        return (self.en_x, self.en_y)


class GnevTora(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 300

        self.radius = hit_box_and_radius.Radius(0.5)

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

    def update_animation(self, delta_time: float = 1 / 60):
        if self.action and not self.kd:
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 250, MOL_BLUE)
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, arcade.color.WHITE)

    def on_update(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_slovar()
        self.update_radius_position()

        self.kd_timer()

        for sprite in self.sprite_list:
            if self.radius.check_collision(sprite) and self.action:
                self.udar(sprite)


class StreliPeruna(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 100

        self.radius = hit_box_and_radius.Radius(2.5)

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_slovar()

        self.kd_timer()

        if self.action and self.radius.check_collision(sprite_list=self.sprite_list):
            spis_pos = []
            spis1 = []
            spis_rast = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite):
                    spis_pos.append(sprite.position)
                    rx = abs(self.pers.center_x - sprite.center_x)
                    ry = abs(self.pers.center_y - sprite.center_y)
                    rast = math.hypot(rx, ry)
                    spis_rast.append((rx, ry))
                    spis1.append(rast)

            for i in spis1:
                if len(spis1) > 5:
                    index = spis1.index(max(spis1))
                    spis_pos.pop(index)
                    spis1.remove(max(spis1))
                    spis_rast.pop(index)
                elif len(spis1) < 1:
                    return
                else:
                    break

            stx, sty = self.radius.position

            while len(spis1) >= 1:
                enx, eny = min(spis_pos)
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.action:
                        self.udar(sprite)

                spis1.remove(spis1[spis_pos.index(min(spis_pos))])
                spis_pos.remove(min(spis_pos))


class SharMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = URON_SHAR_MOL
        self.uron1 = URON1_SHAR_MOL

        self.tex_shar = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.texture = self.tex_shar[1]
        self.scale = 0.01

        self.radius = hit_box_and_radius.Radius()
        self.radius1 = hit_box_and_radius.Radius()

        self.zaryad = False
        self.zaryad_b = False
        self.vzriv = False
        self.promah = False
        self.baf_uron = 1

        self.s_zaryad = 0
        self.timer_for_s_kd = S_KD_SHAR_MOLNII
        self.s_kd = self.timer_for_s_kd + 1
        self.s_do_promah = 0
        self.s_change_x = 0
        self.s = 0
        self.atak = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        uron = self.uron

        self.s_kd += 1
        self.update_radius_position()
        self.radius1.position = self.position
        if self.s_kd <= self.timer_for_s_kd:
            self.zaryad = False

        if self.change_x == 0:
            self.update_position()

        self.update_slovar()

        if self.zaryad:
            self.action = False
            self.zaryad_b = True
            self.s_zaryad += 1
            if self.s_zaryad <= MAX_BAF_S_ZARYAD:
                self.scale += 0.05 / MAX_BAF_S_ZARYAD
                self.baf_uron += BAF_URON / MAX_BAF_S_ZARYAD

        if self.s_zaryad > MAX_S_ZARYAD:
            self.vzriv = True
            self.atak = True
            self.pers.hp -= uron * VZRIV_BAF_URON * round(self.baf_uron, 2)
            self.radius1.scale = self.scale * 1.5
            for sprite in self.sprite_list:
                if self.radius1.check_collision(sprite):
                    self.action = False
                    for i in self.slovar:
                        if sprite == i and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= uron * VZRIV_BAF_URON * round(self.baf_uron, 2)
            self.s_zaryad = 0
            self.zaryad = False
            self.s_kd = 0

        if (self.action and self.zaryad_b) or self.atak:
            self.zaryad = False
            self.s_do_promah += 1
            self.s_zaryad = 0
            if self.s_change_x == 0:
                self.s_kd = 0
                self.s_change_x = 1
                if self.pers.storona == 0:
                    self.change_x = SKOROST_SHAR_MOLNII
                else:
                    self.change_x = -SKOROST_SHAR_MOLNII

            if arcade.check_for_collision_with_list(self, self.sprite_list):
                self.atak = True
                self.radius1.scale = self.scale * 1.5
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite):
                        self.action = False
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron, 2)

            if self.s_do_promah >= S_DO_PROMAH:
                self.promah = True
                self.action = False
                self.atak = True
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite):
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron, 2) / PROMAH_DEBAF_URON

        elif not self.action and not self.atak:
            self.s_do_promah = 0
            self.change_x = 0
            for i in self.slovar:
                self.slovar[i] = False
            if not self.zaryad:
                self.baf_uron = 1
                self.zaryad_b = False
                self.scale = 0.01
                self.s_change_x = 0

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        uron1 = self.uron1
        if self.atak or self.zaryad or self.action:
            arcade.draw_circle_filled(self.center_x, self.center_y, 90, (44, 117, 255, 50), 5)
        if self.atak:
            self.s += 1
            if self.s > self.timer_for_s:
                self.atak = False
                self.promah = False
                self.vzriv = False
                self.s = 0
            spisok_rast = []
            spisok_xy = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite):
                    rast = (abs(self.radius.center_x - sprite.center_x),
                            abs(self.radius.center_y - sprite.center_y))
                    xy = sprite.position
                    spisok_rast.append(rast)
                    spisok_xy.append(xy)

            if len(spisok_rast) > 5:
                while len(spisok_rast) > 5:
                    max_index = spisok_rast.index(max(spisok_rast))
                    spisok_rast.remove(spisok_rast[max_index])
                    spisok_xy.remove(spisok_xy[max_index])

            stx, sty = self.position
            while len(spisok_rast) >= 1:
                min_index = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[min_index]
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                if self.vzriv:
                                    sprite.hp -= uron1 * VZRIV_BAF_URON * round(self.baf_uron, 2)
                                elif self.promah:
                                    sprite.hp -= uron1 * round(self.baf_uron, 2) / PROMAH_DEBAF_URON
                                else:
                                    sprite.hp -= uron1 * round(self.baf_uron, 2)
                spisok_rast.remove(spisok_rast[min_index])
                spisok_xy.remove(spisok_xy[min_index])


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

        self.force_x = 3000
        self.force_y = 5000

        #self.rad = hit_box_and_radius.Radius(0.5)
        self.tex = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.scale = 0.5
        self.texture = self.tex[1]

        self.max = 5

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
            if self.change_x == 0:
                self.position = start

            if self.igrok.storona == 0 and not self.atak:
                self.atak = True
                self.change_x = 10
            elif self.igrok.storona == 1 and not self.atak:
                self.atak = True
                self.change_x = -10
        else:
            self.d = False
            self.atak = False
            self.change_x = 0
            self.s = 0

        if self.s >= 120:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s += 1

        for sprite in self.sprite_list:
            if arcade.check_for_collision(sprite, self) and self.udar:
                for i in self.slovar:
                    if i == sprite and not self.slovar[i]:
                        self.slovar[i] = True
                        sprite.hp -= self.uron

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.tex[self.igrok.storona]

    def return_force(self, mass, xy: str):
        force_x = self.force_x
        force_y = self.force_y
        if xy == 'x':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                force_x -= procent_x * (mass / procent_max)
                if self.igrok.storona == 1:
                    return force_x
                else:
                    return -force_x
            else:
                return 0
        elif xy == 'y':
            if mass < self.max:
                procent_max = self.max / 100
                procent_y = force_y / 100
                force_y -= procent_y * (mass / procent_max)
                return force_y
            else:
                return 0
        elif xy == 'xy':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                procent_y = force_y / 100
                force_x -= procent_x * (mass / procent_max)
                force_y -= procent_y * (mass / procent_max)
                return (force_x, force_y)
            else:
                return 0


# Стихия земли


class KulakGaia(arcade.Sprite):
    def __init__(self, pers, sprite_list=None, sprite=None):
        super().__init__()
        self.sprite_list = sprite_list
        self.sprite = sprite
        self.radius = hit_box_and_radius.Radius()
        self.pers = pers
        self.s2 = 0
        self.s = 301
        self.udar = False
        self.drav = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.s += 1
        if self.s <= 300:
            self.udar = False
            return
        if self.udar and self.s2 < 3 and self.s > 300:
            arcade.draw_rectangle_filled(self.pers.center_x, self.pers.center_y, 128, 128, arcade.color.BROWN)
            arcade.draw_rectangle_filled(self.pers.center_x, self.pers.center_y + 45, 128, 40, arcade.color.GREEN)

        if self.s2 >= 3:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s2 += 1
        elif not self.udar:
            self.s2 = 0

    def on_update(self, delta_time: float = 1 / 60):
        self.radius.position = self.pers.position

        if self.sprite_list is not None:
            if arcade.check_for_collision_with_list(self.radius, self.sprite_list) and self.s2 == 1 and self.udar:
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self.radius, sprite):
                        sprite.hp -= 30

        if self.sprite is not None:
            if arcade.check_for_collision(self.radius, self.sprite) and self.s2 == 1 and self.udar:
                self.sprite.hp -= 30


# Ближний юой


class Mech(arcade.Sprite):
    def __init__(self, pers, sprite_list, v_ataki=(30, 10)):
        super().__init__()
        self.tip = {COLD_ORUZHIE: 0}

        self.uron = 50

        self.pers = pers
        self.sprite_list = sprite_list

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
                            if not block_func(sprite, self.pers):
                                self.slovar[i] = True
                                sprite.hp -= self.uron

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


class DvuruchMech(arcade.Sprite):
    def __init__(self, pers, sprite_list, v_ataki=(60, 20)):
        super().__init__()
        self.tip = {COLD_ORUZHIE: DVURUCH_MECH}

        self.uron = URON_DVURUCH_MECH

        self.pers = pers
        self.sprite_list = sprite_list

        self.kd = v_ataki[0]
        self.kd1 = v_ataki[1]
        self.s = 0
        self.s1 = self.kd1
        self.s2 = 0

        self.slovar = {}

        self.udar_tex0 = arcade.load_texture_pair('nuzhno/udar.png')
        self.udar_tex1 = arcade.load_texture_pair('nuzhno/udar1.png')
        self.texture = self.udar_tex0[1]
        self.scale = 2

        self.udar = False
        self.s_udar = 0

        self.probit_block = False
        self.kombo = False
        for i in self.pers.tip_slovar:
            if i == 4 and self.pers.tip_slovar[i] == 4.1:
                self.kombo = True

    def on_update(self, delta_time: float = 1 / 60):
        if self.probit_block:
            self.s2 += 1
        if self.s2 > 15:
            self.s2 = 0
            self.probit_block = False

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

        if self.kombo and self.pers.rivok:
            self.probit_block = True
            self.s2 = 0

        if self.udar:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and not sprite.block1 and not self.probit_block:
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            if not block_func(sprite, self.pers):
                                self.slovar[i] = True
                                sprite.hp -= self.uron
                elif arcade.check_for_collision(self, sprite) and self.probit_block:
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= self.uron

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
        self.tip = {ZASHCHITA: 0}

        self.uron = URON_SHCHIT

        self.pers = pers
        self.sprite_list = sprite_list
        self.scale = 0.5
        self.tex_shcit = arcade.load_texture_pair('nuzhno/shcit.png')
        self.tex_udar = arcade.load_texture_pair('nuzhno/shcit_udar.png')
        self.texture = self.tex_shcit[1]

        self.block = False
        self.block1 = False
        self.sila = False
        self.udar = False
        self.s = 0
        self.s1 = 15

        self.slovar = {}

        self.s = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.s1 += 1
        if self.s1 <= 15:
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

        if self.s > 10:
            self.udar = False
            self.s1 = 0
            self.s = 0

        if self.udar:
            self.s += 1
            self.block = self.block1 = False
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            if not block_func(sprite, self.pers):
                                self.slovar[i] = True
                                sprite.hp -= self.uron
            return

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

        if self.pers.block1:
            self.block1 = True
        else:
            self.block1 = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.udar:
            self.block = self.block1 = False
            self.texture = self.tex_udar[self.pers.storona]
            return

        if self.block or self.block1:
            self.texture = self.tex_shcit[self.pers.storona]


def block_func(pers, sprite, force=None):
    r = 10
    if sprite.block1:
        return True
    if sprite.reakciya < pers.reakciya and force is None:
        if sprite.reakciya * r <= pers.reakciya:
            pers.block = True
            return True
        else:
            r -= 0.1
            shanc = 99
            while r > 1:
                if sprite.reakciya * (r + 0.1) < sprite.reakciya * r <= pers.reakciya:
                    break
                r -= 0.1
                shanc -= 1

            shanc1 = shanc
            while shanc >= shanc1:
                if random.randint(1, 100) == shanc:
                    pers.block = True
                    return True
                shanc -= 1

            return False
    elif sprite.reakciya > pers.reakciya and force is None:
        if pers.reakciya * r <= sprite.reakciya:
            return False
        else:
            r -= 0.1
            shanc = 99
            while r > 1:
                if sprite.reakciya * (r + 0.1) < sprite.reakciya * r <= pers.reakciya:
                    break
                r -= 0.1
                shanc -= 1

            shanc1 = shanc
            while shanc >= shanc1:
                if random.randint(1, 100) == shanc:
                    return False
                shanc -= 1

            pers.block = True
            return True
    elif sprite.reakciya == pers.reakciya and force is None:
        if random.randint(1, 2) == 1:
            pers.block = True
            return True
        else:
            return False

    if force is not None:
        if pers.storona == 0:
            return force
        else:
            return -force
