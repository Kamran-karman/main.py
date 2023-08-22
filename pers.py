import arcade
import hit_box_and_radius
import sposob
import arcade.gui


KOOR_X = 100
KOOR_Y = 500
D_ZONE = 0.005

HP_VRAG = 250


class Voyslav(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list

        self.hp = 1000
        self.h = self.hp
        self.smert = False
        self.minus_hp = False

        self.reakciay = 1000

        self.block1 = False
        self.block = False
        self.s_block = 0

        self.udar = False
        self.s_udar = 10
        self.s1_udar = 0

        self.scale = 1
        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")

        self.idle_tex = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_tex = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_tex = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_tex = arcade.load_texture_pair(f'nuzhno/udar2.png')

        self.walk_t = []
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.is_on_ground = True
        self.x_odometr = 0

        self.rad = hit_box_and_radius.KvadratRadius(self.scale)
        self.dvig = False

        self.zashcita = False

        self.shcit = sposob.Shchit(self, self.sprite_list)
        if self.shcit.zashcita == 0:
            self.zashcita = True

        self.oruzh_list = arcade.SpriteList()

        self.molniya = sposob.Molniay(self.sprite_list, self)
        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)
        self.streliPeruna = sposob.StreliPeruna(self.sprite_list, self)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        for sprite in self.sprite_list:
            if self.rad.check_collision(sprite) and abs(dx) < D_ZONE:
                if self.center_x > sprite.center_x:
                    self.storona = 1
                elif self.center_x < sprite.center_x:
                    self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.zashcita:
            if self.s_block >= 30:
                self.s_block = 0
                self.block = False

            if self.block:
                self.s_block += 1
                self.texture = self.jump_tex[self.storona]
                return
        else:
            if self.s_block >= 30:
                self.s_block = 0
                self.shcit.block = False
                self.block = False

            if self.block:
                self.shcit.block = True
                self.s_block += 1

        if self.s_udar < 10:
            self.udar = False
            self.s_udar += 1

        if self.s1_udar >= 10:
            self.s1_udar = 0
            self.s_udar = 0
            self.s_udar = False

        if self.udar and self.s_udar >= 10:
            self.s1_udar += 1
            self.texture = self.udar_tex[self.storona]
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
        if self.hp >= self.h:
            self.minus_hp = False
        if self.hp < 0:
            self.smert = True
        elif self.hp < self.h:
            self.h = self.hp
            print('igrok:', self.hp)
            self.minus_hp = True
        elif self.hp > self.h:
            self.h = self.hp

        self.rad.position = self.position

        self.shcit.on_update()

        self.gnev_Tora.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.block or self.block1 or self.udar:
            self.shcit.draw()

        self.shcit.update_animation()

        self.molniya.update_animation()
        self.gnev_Tora.update_animation()
        self.streliPeruna.update_animation()


class BetaMaster(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list

        self.hp = 10000
        self.h = self.hp
        self.smert = False
        self.minus_hp = False

        self.reakciay = 1000

        self.block1 = False
        self.block = False
        self.s_block = 0

        self.udar = False
        self.s_udar = 10
        self.s1_udar = 0

        self.center_x = KOOR_X
        self.center_y = KOOR_Y
        self.scale = 1
        self.storona = 1

        self.sch_walk_tex = 0

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")

        self.idle_tex = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_tex = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_tex = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_tex = arcade.load_texture_pair(f'nuzhno/udar2.png')

        self.walk_t = []
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_tex[0]

        self.is_on_ground = True
        self.x_odometr = 0

        self.rad = hit_box_and_radius.KvadratRadius(self.scale)
        self.dvig = False

        self.zashcita = False

        self.shcit = sposob.Shchit(self, self.sprite_list)
        if self.shcit.zashcita == 0:
            self.zashcita = True

        self.oruzh_list = arcade.SpriteList()
        self.mech = sposob.Mech(self, self.sprite_list, self.storona, (10, 5))
        self.oruzh_list.append(self.mech)

        self.molniya = sposob.Molniay(self.sprite_list, self)
        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)
        self.streliPeruna = sposob.StreliPeruna(self.sprite_list, self)
        self.veter_otalk = sposob.VeterOtalkivanie(self, self.sprite_list)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        for sprite in self.sprite_list:
            if self.rad.check_collision(sprite) and abs(dx) < D_ZONE:
                if self.center_x > sprite.center_x:
                    self.storona = 1
                elif self.center_x < sprite.center_x:
                    self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

        if not self.zashcita:
            if self.s_block >= 30 or self.mech.udar:
                self.s_block = 0
                self.block = False

            if self.block:
                self.s_block += 1
                self.texture = self.jump_tex[self.storona]
                return
        else:
            if self.s_block >= 30 or self.mech.udar:
                self.s_block = 0
                self.shcit.block = False
                self.block = False

            if self.block:
                self.shcit.block = True
                self.s_block += 1

        if self.s_udar < 10:
            self.udar = False
            self.s_udar += 1

        if self.s1_udar >= 10:
            self.s1_udar = 0
            self.s_udar = 0
            self.s_udar = False

        if self.udar and self.s_udar >= 10:
            self.s1_udar += 1
            self.texture = self.udar_tex[self.storona]
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
        if self.hp >= self.h:
            self.minus_hp = False
        if self.hp < 0:
            self.smert = True
        elif self.hp < self.h:
            self.h = self.hp
            print('igrok:', self.hp)
            self.minus_hp = True
        elif self.hp > self.h:
            self.h = self.hp

        self.rad.position = self.position

        self.mech.storona = self.storona
        self.mech.on_update()
        self.shcit.on_update()

        self.veter_otalk.on_update()
        self.gnev_Tora.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.mech.udar:
            self.mech.draw()
        if self.block or self.block1 or self.udar:
            self.shcit.draw()
        self.shcit.update_animation()
        self.mech.update_animation()

        self.molniya.update_animation()
        self.gnev_Tora.update_animation()
        self.streliPeruna.update_animation()
        self.veter_otalk.draw()


class Vrag(arcade.Sprite):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False):
        super().__init__()

        self.hp = HP_VRAG
        self.h = HP_VRAG
        self.smert = False
        self.reakciay = 10
        self.block = False
        self.s_block = 0
        self.pariv = False
        self.minus_hp = False

        self.force_x = 0
        self.force_y = 0

        self.scale = 1.2
        self.storona = 1

        self.radius_vid = hit_box_and_radius.Radius(5)
        self.radius_ataki = hit_box_and_radius.Radius(0.25)
        self.radius_prig = hit_box_and_radius.KvadratRadius(self.scale)

        self.sprite_list = sprite_list
        self.igrok = igrok
        self.igrok_list = arcade.SpriteList()
        self.igrok_list.append(igrok)
        self.v_drug_list = v_drug_list

        self.udar = False
        self.go = True
        self.d_zone = 25
        self.s = 0

        self.kast_scena = kast_scena

        self.sch_walk_tex = 0

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_tex = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_tex = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.smert_tex = arcade.load_texture_pair('nuzhno/smert.png')

        self.walk_t = []
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle[0]

        self.is_on_ground = True
        self.x_odometr = 0

        self.oruzh_list = arcade.SpriteList()
        self.mech = sposob.Mech(self, self.igrok_list, self.storona, (60, 20))
        self.oruzh_list.append(self.mech)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.hp >= self.h:
            self.minus_hp = False
        if not self.smert:
            if self.hp <= 0:
                self.smert = True
            elif self.hp < self.h:
                self.h = self.hp
                self.minus_hp = True
                print(self.hp)
            elif self.hp > self.h:
                self.h = self.hp

            self.radius_vid.position = self.radius_ataki.position = self.radius_prig.position = self.position

            if dx < -D_ZONE and self.storona == 0:
                self.storona = 1
            elif dx > D_ZONE and self.storona == 1:
                self.storona = 0

            if self.radius_prig.check_collision(self.igrok):
                if self.center_x > self.igrok.center_x:
                    self.storona = 1
                elif self.center_x < self.igrok.center_x:
                    self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)

            if not self.go:
                self.s += 1

            if self.radius_vid.check_collision(self.igrok) and not self.kast_scena:

                if self.igrok.center_x < self.radius_vid.center_x:
                    if abs(self.igrok.right - self.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                    else:
                        self.force_x = -15000
                        self.go = True

                        if (self.radius_prig.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if self.radius_prig.check_collision(sprite):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                elif self.igrok.center_x > self.radius_vid.center_x:
                    if abs(self.right - self.igrok.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                    else:
                        self.force_x = 15000
                        self.go = True

                        if (self.radius_prig.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if self.radius_prig.check_collision(sprite):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                for drug in self.v_drug_list:
                    if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone and not drug.go
                            and self.igrok.center_x > self.center_x):
                        self.go = False
                        self.force_x, self.force_y = 0., 0.
                        break
                    elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone and not drug.go
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

            if self.s_block >= 30:
                self.s_block = 0
                self.block = False

            if self.block:
                self.texture = self.jump_tex[self.storona]

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
        self.radius_prig.position = self.position
        self.mech.storona = self.storona
        if self.radius_ataki.check_collision(self.igrok):
            self.mech.udar = True
        else:
            self.mech.udar = False
        self.mech.on_update()

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.mech.udar:
            self.mech.draw()

    def update_animation(self, delta_time: float = 1 / 60):
        self.mech.update_animation()

    def return_force(self, xy=str()):
        if not self.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y


