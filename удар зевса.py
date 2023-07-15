import random

import arcade
import math


class WW(arcade.Window):
    def __init__(self):
        super().__init__(1600, 900)
        self.background_color = (255, 255, 255)
        self.spisok_tochek = [(100, 100), (200, 200), (300, 100)]
        self.s = 0
        self.kk = random.randint(50, 126)
        self.ugl = random.randint(60, 85)
        self.s2 = 0
        self.spis = []
        self.pora = False
        self.r = None

    def gipotenuza(self, katet, ugl):
        gipot = katet / math.sin(math.radians(ugl))
        return gipot

    def katet(self, gipot, katet):
        katet2 = (gipot ** 2 - katet ** 2) ** 0.5
        return katet2

    def kk_gg(self, k1, k2):
        self.kk = random.randint(k1, k2)
        self.ugl = random.randint(60, 85)
        self.r = random.randint(0, 15)

    def on_draw(self):
        self.clear()

        a = 11
        if self.pora:
            self.kk_gg(50, 126)
        gg = self.gipotenuza(self.kk, self.ugl)
        kk2 = self.katet(gg, self.kk)
        stx, sty = 0, 300
        srx, sry = stx + self.kk, sty
        enx, eny = srx, sry + kk2
        spis = [(stx, sty), (enx, eny)]
        while a > 0:
            if sty < eny:
                if self.s2 == 0:
                    stx, sty = enx, eny
                    srx, sry = stx, sty - kk2
                    enx, eny = srx + self.kk, sry
                    spis.append((stx, sty))
                    spis.append((enx, eny))
                    a -= 1
                else:
                    self.kk_gg(50, 126)
                    stx, sty = enx, eny
                    srx, sry = stx, sty - kk2
                    enx, eny = srx + self.kk, sry
                    spis.append((stx, sty))
                    spis.append((enx, eny))
                    a -= 1
            elif sty > eny:
                if self.s2 == 0:
                    stx, sty = enx, eny
                    srx, sry = stx + self.kk, sty
                    enx, eny = srx, sry + kk2
                    spis.append((stx, sty))
                    spis.append((enx, eny))
                    a -= 1
                else:
                    self.kk_gg(50, 126)
                    stx, sty = enx, eny
                    srx, sry = stx + self.kk, sty
                    enx, eny = srx, sry + kk2
                    spis.append((stx, sty))
                    spis.append((enx, eny))
                    a -= 1
            elif stx > enx:
                break

        if self.pora and self.s2 == 1:
            self.spis = spis
            arcade.draw_line_strip(self.spis, (0, 0, 150), 10)
            self.pora = False
        elif self.s2 == 0:
            arcade.draw_line_strip(spis, (0, 0, 150), 10)
        else:
            arcade.draw_line_strip(self.spis, (0, 0, 150), 10)

        a = 11
        kk = 100
        ugl = 50
        gg = self.gipotenuza(kk, ugl)
        kk2 = self.katet(gg, kk)
        if self.pora:
            self.kk_gg(0, 0)
        stx, sty = 0, 100
        srx, sry = stx + kk, sty
        enx, eny = srx + 5, sry + kk2
        spisok = [(stx, sty), (enx - self.r, eny)]
        while a > 0:
            if sty < eny:
                stx, sty = enx - self.r, eny
                srx, sry = stx, sty - kk2
                enx, eny = srx + 5 + kk, sry
                spisok.append((stx, sty))
                spisok.append((enx - self.r, eny))
                a -= 1
            elif sty > eny:
                stx, sty = enx - self.r, eny
                srx, sry = stx + kk, sty
                enx, eny = srx + 5, sry + kk2
                spisok.append((stx, sty))
                spisok.append((enx - self.r, eny))
                a -= 1

        arcade.draw_line_strip(spisok, (0, 0, 255), 10)

        gg = self.gipotenuza(200, 60)
        kk2 = self.katet(gg, 200)
        stx, sty = 800, 450
        srx, sry = stx - 200, sty
        enx, eny = srx, sry + kk2
        spis = [(stx, sty), (enx, eny)]
        arcade.draw_line_strip(spis, (0, 0, 0), 3)
        stx, sty = 800, 450
        sx, sy = abs(enx - stx), abs(eny - sty)
        enx, eny = enx + sx / 2, eny - sy / 2
        arcade.draw_line(stx, sty, enx, eny, (255, 0, 0), 7)
        gg = self.gipotenuza(200, 60)
        kk2 = self.katet(gg, 200)
        stx, sty = 800, 450
        srx, sry = stx - 200, sty
        enx, eny = srx, sry - kk2
        spis = [(stx, sty), (enx, eny)]
        arcade.draw_line_strip(spis, (0, 0, 0), 3)
        stx, sty = 800, 450
        sx, sy = abs(enx - stx), abs(eny - sty)
        enx, eny = enx + sx / 2, eny + sy / 2
        arcade.draw_line(stx, sty, enx, eny, (255, 0, 0), 7)
        gg = self.gipotenuza(200, 60)
        kk2 = self.katet(gg, 200)
        stx, sty = 800, 450
        srx, sry = stx + 200, sty
        enx, eny = srx, sry - kk2
        spis = [(stx, sty), (enx, eny)]
        arcade.draw_line_strip(spis, (0, 0, 0), 3)
        stx, sty = 800, 450
        sx, sy = abs(enx - stx), abs(eny - sty)
        enx, eny = enx - sx / 2, eny + sy / 2
        arcade.draw_line(stx, sty, enx, eny, (255, 0, 0), 7)
        gg = self.gipotenuza(200, 60)
        kk2 = self.katet(gg, 200)
        stx, sty = 800, 450
        srx, sry = stx + 200, sty
        enx, eny = srx, sry + kk2
        spis = [(stx, sty), (enx, eny)]
        arcade.draw_line_strip(spis, (0, 0, 0), 3)
        stx, sty = 800, 450
        sx, sy = abs(enx - stx), abs(eny - sty)
        enx, eny = enx - sx / 2, eny - sy / 2
        arcade.draw_line(stx, sty, enx, eny, (255, 0, 0), 7)
        gg = self.gipotenuza(math.hypot(sx / 2, sy / 2), 60)
        k2 = self.katet(gg, math.hypot(sx / 2, sy / 2))

        if self.pora:
            self.kk_gg(0, 0)
        stx, sty = 0, 450
        enxx, enyy = 1400, 750
        f = True
        w = random.randrange(-1, 2, 2)
        l = 10
        while f:
            if enxx - stx == 1400 and enyy - sty == 300:
                print(1)
                if w < 0:
                    enx, eny = stx + 100 + random.randint(0, 50), sty + (50 + random.randint(0, 10)) * -1 # + (40 + random.randint(20, 30)) * random.randrange(-1, 2, 2)
                    arcade.draw_line(stx, sty, enx, eny, (255, 0, 255), 25)
                    stx, sty = enx, eny
                    w *= -1
                elif w > 0:
                    enx, eny = stx + 100 + random.randint(0, 50), sty + 50 + random.randint(0, 10) * 1  # + (40 + random.randint(20, 30)) * random.randrange(-1, 2, 2)
                    arcade.draw_line(stx, sty, enx, eny, (255, 0, 255), 25)
                    stx, sty = enx, eny
                    w *= -1
            elif math.hypot(enxx - stx, enyy - sty) <= 200:
                print(2)
                arcade.draw_line(stx, sty, enxx, enyy, (255, 0, 255), 25)
                f = False
            else:
                print(3)
                if w < 0:
                    print(3.1)
                    stx, sty = enx, eny
                    enx, eny = stx + 100 + random.randint(0, 50), sty + (50 + random.randint(0, 10)) * -1
                    arcade.draw_line(stx, sty, enx, eny, (255, 0, 255), 25)
                    w *= -1
                elif w > 0:
                    print(3.2)
                    stx, sty = enx, eny
                    enx, eny = stx + 100 + random.randint(0, 50), sty + 50 + random.randint(0, 10) * 1
                    arcade.draw_line(stx, sty, enx, eny, (255, 0, 255), 25)
                    w *= -1
            l -= 1
            if l < 0:
                f = False

    def update(self, delta_time: float):
        if self.s == 1 and self.s2 == 0:
            self.s = 0
            self.s2 += 1
            self.pora = True
        elif self.s == 120:
            self.s = 0
            self.pora = True
        self.s += 1



w = WW()
arcade.run()
