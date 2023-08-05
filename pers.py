import arcade
import hit_box_and_radius
import sposob
import arcade.gui

KOOR_X = 100
KOOR_Y = 500
D_ZONE = 0.005

STOP = 11

HP_VRAG = 1000


class IgrokVoyslav(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.hp = 1000

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
        self.hp = 1000

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

        self.mech = sposob.Mech(self, self.sprite_list, None, self.storona)

        self.molniya = sposob.Molniay(self.sprite_list, self)
        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)
        self.streliPeruna = sposob.StreliPeruna(self.sprite_list, self)
        self.veter_otalk = sposob.VeterOtalkivanie(self, self.sprite_list)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if self.mech.udar:
            return

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

    def on_update(self, delta_time: float = 1 / 60):
        self.mech.storona = self.storona
        self.mech.on_update()

        self.veter_otalk.on_update()
        self.gnev_Tora.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        self.mech.draw()

        self.molniya.update_animation()
        self.gnev_Tora.update_animation()
        self.streliPeruna.update_animation()
        self.veter_otalk.draw()


class Vrag(arcade.Sprite):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False, vr_stan=150, vr_oglush=150, drav=False):
        super().__init__()

        self.hp = HP_VRAG
        self.h = HP_VRAG
        self.smert = False

        self.force_x = 0
        self.force_y = 0

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

        self.radius_vid = hit_box_and_radius.Radius(5)
        self.radius_ataki = hit_box_and_radius.Radius(0.25)
        self.radius_prig = hit_box_and_radius.KvadratRadius(self.scale)

        self.sprite_list = sprite_list
        self.igrok = igrok
        self.v_drug_list = v_drug_list

        self.udar = False
        self.go = True
        self.d_zone = 40
        self.drav = drav

        self.kast_scena = kast_scena

        self.sch_walk_tex = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle = load_tex_pair(f"{main_patch}_idle.png")
        self.jump_tex = load_tex_pair(f"{main_patch}_jump.png")
        self.fall_tex = load_tex_pair(f"{main_patch}_fall.png")
        self.smert_tex = load_tex_pair('nuzhno/smert.png')

        self.walk_t = []
        for i in range(8):
            tex = load_tex_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle[0]

        self.hit_box = self.texture.hit_box_points
        self.is_on_ground = True
        self.x_odometr = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if not self.smert:
            if self.hp < 0:
                self.smert = True
            elif self.hp < self.h:
                self.h = self.hp
                print(self.hp)
            elif self.hp > self.h:
                self.h = self.hp

            self.radius_vid.position = self.radius_ataki.position = self.radius_prig.position = self.position

            if dx < -D_ZONE and self.storona == 0:
                self.storona = 1
            elif dx > D_ZONE and self.storona == 1:
                self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            if arcade.check_for_collision(self.igrok, self.radius_vid) and not self.kast_scena:

                if self.igrok.center_x < self.radius_vid.center_x:
                    if abs(self.igrok.right - self.left) <= 50:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                    else:
                        self.force_x = -15000
                        self.go = True

                        if (arcade.check_for_collision_with_list(self.radius_prig, self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if arcade.check_for_collision(self.radius_prig, sprite):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                elif self.igrok.center_x > self.radius_vid.center_x:
                    if abs(self.right - self.igrok.left) <= 50:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                    else:
                        self.force_x = 15000
                        self.go = True

                        if (arcade.check_for_collision_with_list(self.radius_prig, self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if arcade.check_for_collision(self.radius_prig, sprite):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                for drug in self.v_drug_list:
                    if (drug.center_x > self.center_x and abs(self.right - drug.left) <= 50 and not drug.go
                            and self.igrok.center_x > self.center_x):
                        self.go = False
                        self.force_x, self.force_y = 0., 0.
                        break
                    elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= 50 and not drug.go
                            and self.igrok.center_x < self.center_x):
                        self.go = False
                        self.force_x, self.force_y = 0., 0.
                        break
                    elif (abs(self.right - drug.left) <= self.d_zone and drug.center_x > self.center_x
                          and self.igrok.center_x > self.center_x):
                        self.force_x = 0.
                        break
                    elif (abs(self.left - drug.right) <= self.d_zone and drug.center_x < self.center_x
                          and self.igrok.center_x < self.center_x):
                        self.force_x = 0.
                        break
            else:
                self.go = False
                self.force_x, self.force_y = 0., 0.

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

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.drav:
            self.radius_prig.draw()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.smert:
            self.storona = 0
            self.texture = self.smert_tex[self.storona]
            self.angle = 40

    def return_force(self, xy=str()):
        if not self.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
