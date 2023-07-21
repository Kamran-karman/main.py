import arcade
import hit_box_and_radius
import sposob

KOOR_X = 100
KOOR_Y = 500

STOP = 11


class IgrokVoyslav(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.hp = 100

        self.center_x = KOOR_X
        self.center_y = KOOR_Y
        self.scale = 1
        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")

        self.idle_tex = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.hit_box = self.texture.hit_box_points
        self.is_on_ground = True
        self.x_odometr = 0

        self.sprite_list = sprite_list
        self.molniya = sposob.Molniay(self.sprite_list, self)
        self.molniya_atak = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < 0 and self.storona == 0:
            self.storona = 1
        elif dx > 0 and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > 0:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < 0:
                self.texture = self.fall_tex[self.storona]
                return

        if dx == 0:
            self.texture = self.idle_tex[self.storona]
            return

        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]

    def on_update(self, delta_time: float = 1 / 60):
        #self.molniya.update_animation()
        if self.molniya_atak:
            self.molniya.udar = True
            self.molniya_atak = False
        self.molniya.update_animation()


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

        self.scale = 1.2
        self.storona = 1
        # Эта переменная, которая указывает
        # радиус перемещения врага к игроку
        self.radius_vid = hit_box_and_radius.Radius(0.4)
        # Эта переменная указывает радиус, в котором враг атакует цель
        self.radius_ataki = hit_box_and_radius.Radius(0.03)
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
        self.is_on_ground = True
        self.x_odometr = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < 0 and self.storona == 0:
            self.storona = 1
        elif dx > 0 and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > 0:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < 0:
                self.texture = self.fall_tex[self.storona]
                return

        if dx == 0:
            self.texture = self.idle[self.storona]
            return

        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
