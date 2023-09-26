import arcade
import hit_box_and_radius
import math
import random

MOL_BLUE = (44, 117, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

ZASHCHITA = 100
SHCHIT = 101

COLD_ORUZHIE = 200
MECH = 201
DVURUCH_MECH = 202
VILA = 204
TOPOR = 205
MECH_BRENDA = 206

DAL_ORUZH = 300

STIHIYA = 400
CEPNAYA_MOLNIYA = 401
GNEV_TORA = 402
STRELI_PERUNA = 403
SHAR_MOLNIYA = 404
UDAR_ZEVSA = 405

FIZ_SPOSOB = 500
UDAR = 501
RIVOK = 502


# ___SharMolniay___
SKOROST_SHAR_MOLNII = 20
URON_SHAR_MOL = 25
URON1_SHAR_MOL = 5

S_KD_SHAR_MOL = 300
MAX_S_ZARYAD_SHAR_MOL = 420
MAX_BAF_S_ZARYAD_SHAR_MOL = 300
S_DO_PROMAH_SHAR_MOL = 45

VZRIV_BAF_URON_SHAR_MOL = 1.5
PROMAH_DEBAF_URON_SHAR_MOL = 1.5
BAF_URON_SHAR_MOL = 19.067
# ______________________


# ___UdarZevsa___
URON_UDAR_ZEVSA = 10

S_KD_UDAR_ZEVSA = 600
S_UDAR_ZEVSA = 300

BAF_URON_UDAR_ZEVSA = 1.5
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


# ___Vila___
URON_VILA = 30
# ______________________


# ___Topor___
URON_TOPOR = 40
# ______________________


# ___MechBrenda___
URON_MECH_BRENDA = 150


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

    def update_action(self):
        if self.pers.hp <= 0:
            self.action = False


class Block(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.block = False
        self.avto_block = False
        self.s_avto_block = 0
        self.timer_for_s_ab = 30

    def block_func(self, sprite1):
        if sprite1.storona == self.pers.storona:
            return False
        r = 10
        for sprite in self.sprite_list:
            if sprite == sprite1:
                if sprite.block.block:
                    return True

                if self.pers.reakciya > sprite.reakciya:
                    if sprite.reakciya * r <= self.pers.reakciya:
                        return False
                    else:
                        r -= 0.1
                        shanc = 1
                        while r >= 0.1:
                            if sprite.reakciya * (r - 0.1) < sprite.reakciya * r <= self.pers.reakciya:
                                break
                            r -= 0.1
                            shanc += 1

                        while shanc > 0:
                            if random.randint(1, 200) == shanc:
                                return False
                            shanc -= 1

                        sprite.block.avto_block = True
                        return True
                elif self.pers.reakciya < sprite.reakciya:
                    if sprite.reakciya >= self.pers.reakciya * r:
                        sprite.block.avto_block = True
                        return True
                    else:
                        r -= 0.1
                        shanc = 1
                        while r >= 0.1:
                            if self.pers.reakciya * (r - 0.1) < self.pers.reakciya * r <= sprite.reakciya:
                                break
                            r -= 0.1
                            shanc += 1

                        while shanc > 0:
                            if random.randint(1, 200) == shanc:
                                sprite.block.avto_block = True
                                return True
                            shanc -= 1

                        return False
                else:
                    if random.randint(0, 1) == 1:
                        sprite.block.avto_block = True
                        return True
                    else:
                        return False

    def update_block(self):
        if self.avto_block:
            self.s_avto_block += 1

        if self.s_avto_block >= self.timer_for_s_ab:
            self.avto_block = False
            self.s_avto_block = 0


class Mobilnost(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)

        self.scale = self.pers.scale
        self.minus_stamina = 0

    def stamina(self, minus_stamina):
        if self.pers.stamina >= minus_stamina:
            return True
        else:
            return False


class Fight(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 0
        
        self.slovar = {}

        self.kd = False
        
    def update_slovar(self, a):
        if a == 1:
            if len(self.slovar) != len(self.sprite_list):
                for sprite in self.sprite_list:
                    self.slovar.update({sprite: False})

        elif a == 2:
            if not self.action:
                for i in self.slovar:
                    self.slovar[i] = False

    def update_position(self):
        self.position = self.pers.position

    def udar(self, sprite):
        for i in self.slovar:
            if i == sprite and not self.slovar[i]:
                self.slovar[i] = True
                sprite.hp -= round(self.uron)

    def kd_timer1(self):
        self.s_kd += 1
        if self.s_kd <= self.timer_for_s_kd and self.s > self.timer_for_s:
            self.kd = True
        elif self.s_kd > self.timer_for_s_kd:
            self.kd = False

        if self.kd:
            self.action = False

        if self.s > self.timer_for_s:
            self.action = False
            self.s = 0

        if self.action:
            self.s += 1
        if self.action and self.s == 1:
            self.s_kd = 0

    def kd_timer0(self):
        self.s_kd += 1

        if self.s_kd <= self.timer_for_s_kd:
            self.action = False

        if self.action:
            self.s += 1

        if self.s > self.timer_for_s:
            self.action = False
            self.s_kd = 0
            self.s = 0


class ColdOruzhie(Fight):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = None

        self.block = Block(pers, sprite_list)

        self.minus_stamina = 0

    def udar_and_block(self, sprite):
        for i in self.slovar:
            if not self.block.block_func(sprite) and i == sprite and not self.slovar[i]:
                self.slovar[i] = True
                sprite.hp -= round(self.uron)

    def update_storona(self):
        self.texture = self.udar_texture[self.pers.storona]
        self.hit_box._points = self.texture.hit_box_points

    def stamina(self, minus_stamina):
        if self.pers.stamina >= minus_stamina:
            return True
        else:
            return False


class FizSposobFight(Fight):
    def __init__(self, pers, sprite_list, uron, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)

        self.uron = uron

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = self.pers.udar_texture

        self.scale = self.pers.scale

        self.block = Block(pers, sprite_list)

        self.minus_stamina = 0

    def update_scale(self):
        self.scale = self.pers.scale

    def udar_and_block(self, sprite):
        for i in self.slovar:
            if not self.block.block_func(sprite) and i == sprite and not self.slovar[i]:
                self.slovar[i] = True
                sprite.hp -= self.uron

    def stamina(self, minus_stamina):
        if self.pers.stamina >= minus_stamina:
            return True
        else:
            return False


class Stihiya(Fight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)

        self.radius = None
        self.radius: hit_box_and_radius.Radius

        self.minus_mana = 0

    def update_radius_position(self):
        self.radius.position = self.position

    def mana(self, minus_mana):
        if self.pers.mana >= minus_mana:
            return True
        else:
            return False

    def update_mor(self):
        if self.pers.mor:
            self.uron *= 2 / 3


class Zashchita(Fight):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd, fizika):
        super().__init__(pers, sprite_list)

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = None
        self.block_texture = None

        self.block = Block(pers, sprite_list)

        self.force = 0
        self.s_return_force = 0
        self.rf = False

        self.fizika = fizika

        self.sposob_list = arcade.SpriteList()

        self.minus_stamina = 0

    def udar_or_block_animation(self):
        if self.action:
            self.block.block = self.block.avto_block = False
            self.texture = self.udar_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points
            return

        if self.block.block or self.block.avto_block:
            self.texture = self.block_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points

    def update_avto_block(self):
        if self.pers.block.avto_block:
            self.block.avto_block = True
        else:
            self.block.avto_block = False

    def udar_and_block(self, sprite):
        for i in self.slovar:
            if not self.block.block_func(sprite) and i == sprite and not self.slovar[i]:
                self.slovar[i] = True
                sprite.hp -= self.uron

    def return_force(self, fizika):
        self.force = 2500
        if not self.rf:
            self.s_return_force = 0
        else:
            self.s_return_force += 1
        for sprite in self.sprite_list:
            for sposob in sprite.oruzh_list:
                if (arcade.check_for_collision(sposob, self) and (self.block.block or self.block.avto_block)
                        and sposob.action and self.s_return_force <= 2):
                    self.pers.stamina -= 2
                    self.rf = True
                    if self.pers.storona == 0:
                        fizika.apply_force(self.pers, (-self.force, 0))
                    elif self.pers.storona == 1:
                        fizika.apply_force(self.pers, (self.force, 0))
                    fizika.set_friction(self.pers, 1)
                    if sposob not in self.sposob_list:
                        self.sposob_list.append(sposob)
            for sposob1 in self.sposob_list:
                if not self.block.avto_block and not sposob1.action:
                    self.rf = False
                    self.sposob_list.remove(sposob1)

    def stamina(self, minus_stamina):
        if self.pers.stamina >= minus_stamina:
            return True
        else:
            return False


class Molniya(Stihiya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.timer_for_s = 3


# Физические способности


class Rivok(Mobilnost):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = RIVOK

        self.rivok_tex = (
            arcade.load_texture_pair(':resources:images/animated_characters/male_person/malePerson_walk7.png'))

        self.texture = self.rivok_tex[1]

        self.radius_stop = hit_box_and_radius.KvadratRadius(self.scale)
        self.stop1 = False

        self.timer_for_s = 50
        self.timer_for_rivok = 30

        self.minus_stamina = 25

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.s_kd += 1
        if self.s_kd < S_KD_RIVOK:
            self.action = False

        if self.action:
            self.s += 1
            if self.s == 1:
                if not self.stamina(self.minus_stamina):
                    self.action = False
                    self.stop1 = True
                else:
                    self.pers.stamina -= self.minus_stamina
        if self.s > self.timer_for_s:
            self.s_kd = 0
            self.change_x = 0
            self.action = False
            self.stop1 = True
            self.s = 0

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

        if self.s <= self.timer_for_rivok and self.action:
            self.pers.kast_scena = True
        else:
            self.pers.kast_scena = False

        if self.pers.storona == 0 and self.action and self.timer_for_s >= self.s > self.timer_for_rivok:
            self.change_x = 40
            self.stop1 = False
        elif self.pers.storona == 1 and self.action and self.timer_for_s >= self.s > self.timer_for_rivok:
            self.change_x = -40
            self.stop1 = False

        if self.stop1:
            print(1)

        self.pers.rivok = self.action

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.rivok_tex[self.pers.storona]

    def return_positoin(self):
        return self.position


class Udar(FizSposobFight):
    def __init__(self, pers, sprite_list, uron, timer_for_s=10, timer_for_s_kd=30):
        super().__init__(pers, sprite_list, uron, timer_for_s, timer_for_s_kd)
        self.tip = UDAR

        self.s_kd = self.timer_for_s_kd + 5

        self.probit_block = False
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if self.pers.sil:
            self.probit_block = True

        self.uron = self.pers.uron

        self.update_scale()
        self.update_position()
        self.update_slovar(1)

        self.kd_timer0()

        if self.action and self.stamina(self.minus_stamina):
            if self.s == 1:
                self.pers.stamina -= self.minus_stamina
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    if not self.probit_block:
                        self.udar_and_block(sprite)
                    else:
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= self.uron

        self.update_slovar(2)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.udar_texture[self.pers.storona]


# Стихия молнии


class CepnayaMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = CEPNAYA_MOLNIYA

        self.uron = 1

        self.minus_mana = 20

        self.en_x = 0
        self.en_y = 0

        self.radius = hit_box_and_radius.Radius()

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

        self.tp = False

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_slovar(1)
        self.update_radius_position()
        self.update_action()
        self.update_mor()

        self.kd_timer1()

        if self.s == 1:
            if self.mana(self.minus_mana):
                self.pers.mana -= self.minus_mana
                self.tp = True
            else:
                self.action = False
                self.s = 0
        else:
            self.tp = False

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
                w = 1

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

        self.update_slovar(2)

    def return_position(self):
        if self.tp:
            return self.en_x, self.en_y


class GnevTora(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = GNEV_TORA
        self.uron = 300

        self.radius = hit_box_and_radius.Radius(0.5)

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

        self.minus_mana = 20

    def update_animation(self, delta_time: float = 1 / 60):
        if self.action and self.s <= self.timer_for_s:
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 250, MOL_BLUE)
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, arcade.color.WHITE)

    def on_update(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_slovar(1)
        self.update_radius_position()
        self.update_action()
        self.update_mor()

        self.kd_timer1()

        for sprite in self.sprite_list:
            if self.radius.check_collision(sprite) and self.action and self.mana(self.minus_mana):
                self.udar(sprite)

        if self.s == 1:
            if self.mana(self.minus_mana):
                self.pers.mana -= self.minus_mana

        self.update_slovar(2)


class StreliPeruna(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = STRELI_PERUNA
        self.uron = 100

        self.radius = hit_box_and_radius.Radius(2.5)

        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd

        self.minus_mana = 4

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_slovar(1)
        self.update_action()
        self.update_mor()

        self.kd_timer1()

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

            mnozh = len(spis1)

            while len(spis1) >= 1:
                enx, eny = min(spis_pos)
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.action and self.mana(self.minus_mana * mnozh):
                        self.udar(sprite)

                spis1.remove(spis1[spis_pos.index(min(spis_pos))])
                spis_pos.remove(min(spis_pos))

            if self.s == 1:
                if self.mana(self.minus_mana * mnozh):
                    self.pers.mana -= self.minus_mana * mnozh

        self.update_slovar(2)


class SharMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = SHAR_MOLNIYA

        self.uron = URON_SHAR_MOL
        self.uron1 = URON1_SHAR_MOL
        self.minus_mana = 1

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
        self.timer_for_s_kd = S_KD_SHAR_MOL
        self.s_kd = self.timer_for_s_kd + 1
        self.s_do_promah = 0
        self.s_change_x = 0
        self.s = 0
        self.atak = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_mor()
        uron = self.uron
        self.update_action()

        self.s_kd += 1
        self.update_radius_position()
        self.radius1.position = self.position
        if self.s_kd <= self.timer_for_s_kd:
            self.zaryad = False

        if self.change_x == 0:
            self.update_position()

        self.update_slovar(1)

        if self.zaryad:
            self.action = False
            self.zaryad_b = True
            self.s_zaryad += 1
            if self.s_zaryad < MAX_BAF_S_ZARYAD_SHAR_MOL:
                self.scale += 0.05 / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.baf_uron += BAF_URON_SHAR_MOL / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.minus_mana += 99 / MAX_BAF_S_ZARYAD_SHAR_MOL
                if not self.mana(self.minus_mana):
                    self.zaryad = False
                    self.s_zaryad = 0
                    self.vzriv = True
                    self.atak = True
                    self.pers.mana -= round(self.minus_mana * 1.2)

        if self.s_zaryad > MAX_S_ZARYAD_SHAR_MOL:
            self.vzriv = True
            self.atak = True
            self.pers.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
            self.radius1.scale = self.scale * 1.5
            for sprite in self.sprite_list:
                if self.radius1.check_collision(sprite):
                    self.action = False
                    for i in self.slovar:
                        if sprite == i and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
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
                                sprite.hp -= uron * round(self.baf_uron)

            if self.s_do_promah >= S_DO_PROMAH_SHAR_MOL:
                self.promah = True
                self.action = False
                self.atak = True
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite):
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL

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
                self.minus_mana = 1

        self.update_slovar(2)

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
                                    sprite.hp -= uron1 * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
                                elif self.promah:
                                    sprite.hp -= uron1 * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL
                                else:
                                    sprite.hp -= uron1 * round(self.baf_uron)
                spisok_rast.remove(spisok_rast[min_index])
                spisok_xy.remove(spisok_xy[min_index])

        if self.s == 1:
            if self.vzriv:
                if self.mana(self.minus_mana * 1.2):
                    self.pers.mana -= round(self.minus_mana * 1.2)
            else:
                if self.mana(self.minus_mana):
                    self.pers.mana -= self.minus_mana


class UdarZevsa(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = UDAR_ZEVSA
        self.uron = URON_UDAR_ZEVSA
        self.d = 0

        self.timer_for_s_kd = S_KD_UDAR_ZEVSA
        self.s_kd = self.timer_for_s_kd + 5

        self.timer_for_s = S_UDAR_ZEVSA

        self.radius = hit_box_and_radius.Radius(1.5)

        self.rast = 0
        self.slovar_rast = {}
        self.s1 = 0
        self.line_width = 15
        self.minus_mana = 2

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_position()
        self.update_radius_position()
        self.update_slovar(1)
        self.update_action()
        self.update_mor()

        self.kd_timer0()

        if self.s == 1:
            if self.mana(self.minus_mana):
                self.pers.mana -= self.minus_mana

        if self.action:
            self.s1 = 1
            if self.s % 30 == 0:
                self.timer_for_s_kd += 30
                self.uron *= BAF_URON_UDAR_ZEVSA
                self.minus_mana *= 1.35
                if not self.mana(self.minus_mana):
                    self.action = False
                    self.pers.mana -= round(self.minus_mana)
                else:
                    self.pers.mana -= round(self.minus_mana)
                self.line_width *= 1.1
                for i in self.slovar:
                    self.slovar[i] = False

            if len(self.slovar_rast) == 0:
                for sprite in self.sprite_list:
                    if self.radius.check_collision(sprite):
                        rast_x = abs(sprite.center_x - self.pers.center_x)
                        rast_y = abs(sprite.center_y - self.pers.center_y)
                        rast = math.hypot(rast_x, rast_y)
                        self.slovar_rast.update({sprite: rast})

            self.rast = min(self.slovar_rast.values())
            for sprite in self.slovar_rast:
                if sprite.hp <= 0:
                    self.action = False
                    break
                if self.slovar_rast[sprite] == self.rast:
                    self.udar(sprite)
        else:
            if self.s1 == 1:
                self.s_kd = 0
                self.s1 -= 1
            if self.s_kd > self.timer_for_s_kd:
                self.timer_for_s_kd = S_KD_UDAR_ZEVSA
            self.rast = 0
            self.slovar_rast.clear()
            self.uron = URON_UDAR_ZEVSA
            self.line_width = 15
            self.minus_mana = 2

        self.update_slovar(2)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.action:
            for sprite in self.slovar_rast:
                if self.slovar_rast[sprite] == self.rast:
                    arcade.draw_line(self.pers.center_x, self.pers.center_y, sprite.center_x, sprite.center_y,
                                     MOL_BLUE, self.line_width)
                    break


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


class Mech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = MECH
        self.uron = 50

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60):
        self.update_slovar(1)
        self.update_action()

        self.kd_timer0()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_and_block(sprite)

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

        self.update_slovar(2)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class DvuruchMech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = DVURUCH_MECH

        self.uron = URON_DVURUCH_MECH

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 2

        self.probit_block = False
        self.s_probit_block = 0
        self.kombo = False
        for oruzh in self.pers.oruzh_list:
            if oruzh.tip == 502:
                self.kombo = True

    def on_update(self, delta_time: float = 1 / 60):
        self.update_action()
        if self.probit_block:
            self.s_probit_block += 1
        if self.s_probit_block > 15:
            self.s_probit_block = 0
            self.probit_block = False

        self.update_slovar(1)

        self.kd_timer0()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.kombo and self.pers.rivok:
            self.probit_block = True
            self.s_probit_block = 0

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and not self.probit_block:
                    self.udar_and_block(sprite)
                elif arcade.check_for_collision(self, sprite) and self.probit_block:
                    self.udar(sprite)

        self.update_slovar(2)

        self.position = self.pers.position

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Shchit(Zashchita):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd, fizika):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd, fizika)
        self.tip = SHCHIT
        self.uron = URON_SHCHIT

        self.scale = 0.5
        self.block_texture = arcade.load_texture_pair('nuzhno/shcit.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/shcit_udar.png')
        self.texture = self.block_texture[1]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.return_force(self.fizika)
        self.update_action()

        if self.pers.block.block:
            self.block.block = True
        else:
            self.block.block = False

        self.update_slovar(1)

        self.kd_timer0()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        self.center_y = self.pers.center_y
        if not self.action:
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

        if self.action:
            self.s += 1
            self.block.block = self.block.avto_block = False
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    self.udar_and_block(sprite)

        self.update_slovar(2)

        self.update_avto_block()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.udar_or_block_animation()
        

class Vila(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s=50, timer_for_s_kd=20):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = VILA
        self.uron = URON_VILA

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/vila.png')
        self.texture = self.udar_texture[0]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_slovar(1)
        self.update_action()

        self.kd_timer0()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if self.pers.storona == 0:
                if self.s < self.timer_for_s // 2:
                    self.change_x = 3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = -3
            elif self.pers.storona == 1:
                if self.s < self.timer_for_s // 2:
                    self.change_x = -3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = 3

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.s < 30:
                    self.udar_and_block(sprite)

        self.update_slovar(2)

        if not self.action:
            self.center_y = self.pers.center_y
            if self.pers.storona == 0:
                self.center_x = self.pers.center_x + 20
            elif self.pers.storona == 1:
                self.center_x = self.pers.center_x - 20

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Topor(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = TOPOR
        self.uron = URON_TOPOR

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/topor0.png')
        self.texture = self.udar_texture[0]
        self.angle = 10

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_slovar(1)
        self.update_position()
        self.update_action()

        self.kd_timer0()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if 10 <= self.s < 20:
                if self.pers.storona == 1:
                    self.change_angle = -12
                else:
                    self.change_angle = 12
            else:
                self.change_angle = 0
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_and_block(sprite)
        else:
            self.angle = 10

        self.update_slovar(2)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class MechBrenda(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = MECH_BRENDA
        self.uron = URON_MECH_BRENDA

        self.udar_texture = arcade.load_texture_pair('nuzhno/mech_Brenda0.png')
        self.texture = self.udar_texture[0]

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_slovar(1)
        self.update_action()

        self.kd_timer0()
        if self.s % 4 == 0 and self.action:
            self.pers.stamina -= self.minus_stamina
            for i in self.slovar:
                self.slovar[i] = False

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_and_block(sprite)

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

        self.update_slovar(2)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
