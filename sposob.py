import arcade
import hit_box_and_radius
import math

MOL_BLUE = (44, 117, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Стихия молнии
class Molniay(arcade.Sprite):
    def __init__(self, sprite_list, igrok):
        super().__init__()
        self.uron = 250

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
        if self.s1 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s1 += 1

        self.radius.position = self.igrok.position
        self.s_kd += 1
        if self.s_kd < 300:
            self.udar = False

        if self.s <= 3 and self.udar and self.s_kd >= 300:
            spisok = []
            spisok2 = []
            spisok3 = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite=sprite):
                    poz_x, poz_y = abs(sprite.center_x - self.igrok.center_x), \
                        abs(sprite.center_y - self.igrok.center_y)
                    pozi = (poz_x, poz_y)
                    spisok.append(pozi)
                    x, y = sprite.center_x, sprite.center_y
                    xy = (x, y)
                    spisok2.append(xy)
            if len(spisok) == 0:
                self.en_x, self.en_y = self.igrok.position
            elif len(spisok) > 0:
                stx, sty = self.igrok.position
                en = spisok.index(min(spisok))
                enx, eny = spisok2[en]
                spisok3.append(spisok2[en])
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        for pos in self.slovar:
                            if pos == sprite and not self.slovar[pos]:
                                self.slovar[pos] = True
                                sprite.hp -= self.uron

                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                arcade.draw_circle_filled(stx, sty, 50, MOL_BLUE)
                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                arcade.draw_line(stx, sty, enx, eny, WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, WHITE)
                arcade.draw_circle_filled(enx, eny, 25, WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                w = 0
                while w < 3:
                    if radius.check_collision(sprite_list=self.sprite_list):
                        if self.igrok.position == (stx, sty):
                            pred_poz = 0, 0
                        else:
                            pred_poz = stx, sty
                        spisok = []
                        spisok2 = []
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
                                    spisok.append(pozi)
                                    spisok2.append(xy)
                        if len(spisok) == 0:
                            if stx > enx:
                                self.en_x, self.en_y = enx - 150, eny + 50
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 150, eny + 50
                            break
                        elif w == 2 and len(spisok) != 0:
                            en = spisok.index(min(spisok))
                            stx, sty = radius.position
                            enx, eny = spisok2[en]
                            for sprite in self.sprite_list:
                                if sprite.position == (enx, eny):
                                    for pos in self.slovar:
                                        if pos == sprite and not self.slovar[pos]:
                                            self.slovar[pos] = True
                                            sprite.hp -= self.uron

                            arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                            arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                            arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                            arcade.draw_line(stx, sty, enx, eny, WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, WHITE)
                            if stx > enx:
                                self.en_x, self.en_y = enx - 150, eny + 50
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 150, eny + 50
                            break
                        else:
                            if len(spisok) != 0:
                                en = spisok.index(min(spisok))
                                stx, sty = radius.position
                                enx, eny = spisok2[en]
                                spisok3.append(spisok2[en])
                                for sprite in self.sprite_list:
                                    if sprite.position == (enx, eny):
                                        for pos in self.slovar:
                                            if pos == sprite and not self.slovar[pos]:
                                                self.slovar[pos] = True
                                                sprite.hp -= self.uron

                                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                                arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                                arcade.draw_line(stx, sty, enx, eny, WHITE, 20)
                                arcade.draw_circle_filled(stx, sty, 25, WHITE)
                                arcade.draw_circle_filled(enx, eny, 25, WHITE)
                                radius.position = enx, eny
                    w += 1

        if self.s > 3:
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
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, WHITE)

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
                arcade.draw_line(stx, sty, enx, eny, WHITE, 15)
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


# Оружие
class Mech(arcade.Sprite):
    def __init__(self, pers, sprite_list, shcit, storona, angle=15):
        super().__init__()
        self.uron = 50

        self.pers = pers
        self.sprite_list = sprite_list
        self.shchit = shcit
        self.storona = storona
        self.ugl = angle

        self.s = 0
        self.s1 = 30

        self.slovar = {}

        self.udar_tex0 = arcade.Sprite('nuzhno/udar.png', 1.5)
        self.udar_tex1 = arcade.Sprite('nuzhno/udar.png', 1.5, flipped_horizontally=True)

        self.udar = False
        self.s_udar = 0

    def on_update(self, delta_time: float = 1 / 60):
        if self.s == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s += 1
        if self.s1 <= 30:
            self.udar = False
        if self.udar:
            self.s_udar += 1
        if self.s_udar > 10:
            self.s_udar = 0
            self.udar = False
            self.s1 = 0

        if self.udar:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self.udar_tex1, sprite) and self.storona == 1:
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= self.uron
                elif arcade.check_for_collision(self.udar_tex0, sprite) and self.storona == 0:
                    for i in self.slovar:
                        if i == sprite and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= self.uron

        self.udar_tex0.left, self.udar_tex0.bottom = self.pers.center_x - 12, self.pers.center_y - 40
        self.udar_tex1.right, self.udar_tex1.bottom = self.pers.center_x + 12, self.pers.center_y - 40

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

        self.s1 += 1

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.s1 <= 30:
            self.udar = False
        if self.udar:
            if self.storona == 0:
                self.udar_tex0.angle = -self.ugl
                self.udar_tex0.draw()
            elif self.storona == 1:
                self.udar_tex1.angle = self.ugl
                self.udar_tex1.draw()


class Shchit(arcade.Sprite):
    pass


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]


