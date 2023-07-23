import arcade
import hit_box_and_radius
import sposob

KOOR_X = 100
KOOR_Y = 500
D_ZONE = 0.005

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

        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > D_ZONE:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < -D_ZONE:
                self.texture = self.fall_tex[self.storona]
                return

        if abs(dx) < D_ZONE:
            self.texture = self.idle_tex[self.storona]
            return

        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]

    def update_animation(self, delta_time: float = 1 / 60):
        self.molniya.update_animation()

        self.gnev_Tora.update_animation()


class BetaMaster(arcade.Sprite):
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

        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > D_ZONE:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < -D_ZONE:
                self.texture = self.fall_tex[self.storona]
                return

        if abs(dx) < D_ZONE:
            self.texture = self.idle_tex[self.storona]
            return

        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]

    def update_animation(self, delta_time: float = 1 / 60):
        self.molniya.update_animation()

        self.gnev_Tora.update_animation()


class Vrag(arcade.Sprite):
    def __init__(self, igrok, object, kast_scena=False, vr_stan=150, vr_oglush=150):
        super().__init__()
        self.hp = 100

        self.force = (0., 0.)

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

        self.radius_vid = hit_box_and_radius.Radius(0.4)
        self.radius_ataki = hit_box_and_radius.Radius(0.03)

        self.object = object
        self.igrok = igrok

        self.udar = False

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
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.is_on_ground:
            if dy > D_ZONE:
                self.texture = self.jump_tex[self.storona]
                return
            elif dy < -D_ZONE:
                self.texture = self.fall_tex[self.storona]
                return

        if abs(dx) < D_ZONE:
            self.texture = self.idle[self.storona]
            return

        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]

    def on_update(self, delta_time: float = 1 / 60):
        self.radius_vid.position = self.radius_ataki = self.position

        if arcade.check_for_collision(self.igrok, self.radius_vid) and not self.kast_scena:
            if self.igrok.center_x < self.radius_vid.center_x:
                if self.left - self.igrok.right <= 30:
                    self.force = (0., 0.)
                else:
                    self.force = (-11000, 0)
            elif self.igrok.center_x > self.radius_vid.center_x:
                if self.igrok.left - self.right <= 30:
                    self.force = (0., 0.)
                else:
                    self.force = (11000, 0)

            if self.igrok.center_y > self.radius_vid.center_y and self.is_on_ground and self.force[0] == 0:
                self.force = (0, 50000)
        else:
            self.force = (0., 0.)

    def return_force(self):
        return self.force


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
