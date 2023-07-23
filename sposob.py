import arcade
import hit_box_and_radius

MOL_BLUE = (44, 117, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Molniay(arcade.Sprite):
    def __init__(self, sprite_list, igrok):
        super().__init__()
        self.radius = hit_box_and_radius.Radius()
        self.sprite_list = sprite_list
        self.igrok = igrok
        self.en_x = 0
        self.en_y = 0
        self.udar = False
        self.s = 0
        self.s_kd = 300

    def update_animation(self, delta_time: float = 1 / 60):
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
            if len(spisok) > 0:
                stx, sty = self.igrok.position
                en = spisok.index(min(spisok))
                enx, eny = spisok2[en]
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.s == 0:
                        sprite.hp -= 30
                spisok3.append(spisok2[en])
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                arcade.draw_circle_filled(stx, sty, 50, MOL_BLUE)
                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                arcade.draw_line(stx, sty, enx, eny, WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, WHITE)
                arcade.draw_circle_filled(enx, eny, 25, WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                w = 0
                while w < 4:
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
                            arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                            arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                            arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                            arcade.draw_line(stx, sty, enx, eny, WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, WHITE)
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

    def koordinati(self):
        return self.en_x, self.en_y


class GnevTora(arcade.Sprite):
    def __init__(self, sprite_list, pers):
        super().__init__()
        # Эта переменная указывает список целей
        self.sprite_list = sprite_list

        # Эта переменая - радиус поражения
        self.radius = hit_box_and_radius.Radius()
        self.pers = pers

        # Счётчики
        self.s2 = 0
        self.s = 301

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

        for sprite in self.sprite_list:
            if arcade.check_for_collision(self.radius, sprite):
                sprite.hp -= 20
