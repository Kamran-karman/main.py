import arcade


class Vrag(arcade.Sprite):
    def __init__(self, igrok, kast_scena=False):
        super().__init__()
        self.hp = 100

        # Переменные для контроля игрока
        self.stan = False
        self.s_stan = 0
        self.oglush = False
        self.s_oglush = 0
        self.c_y = None
        self.y_oglush = True

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
        # Это условие проверяет: есть ли игрко в радиусе перемещения врага, находится ли враг в стне и в оглушении
        if arcade.check_for_collision(self.radius_vid, self.igrok) and not self.stan and not self.oglush:
            # Это условие проверяет, есть ли щас каст сцена
            if not self.kast_scena:
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
        else:
            self.change_x = 0

        if not self.kast_scena:
            # Это условие проверяет, попал ли враг по цели
            if arcade.check_for_collision(self.radius_ataki, self.igrok):
                self.udar = True
            else:
                self.udar = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.y_oglush:
            self.c_y = self.center_y

        # Последуещие 2 условия оглушают врага
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

        # Последуещие 2 условия станят врага
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
            self.sch_walk_tex += 0.2
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[int(self.sch_walk_tex)][self.storona]


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
