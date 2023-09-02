import arcade
import hit_box_and_radius
import sposob
import arcade.gui


KOOR_X = 100
KOOR_Y = 500
D_ZONE = 0.005

# ___Vrag___
HP_VRAG = 500

# ___Voin_Innocentii___
HP_V_I = 1000
REAKCIYA_V_I = 65

# ___Gromila___
HP_GROMILA = 2000

URON_GROMILA = 100

REAKCIYA_GROMILA = 10


class Pers(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list

        self.hp = 0
        self.h = self.hp
        self.smert = False
        self.minus_hp = False

        self.reakciya = 0
        self.block1 = False
        self.block = False
        self.s_block = 0
        self.timer_for_s_block = 30
        self.zashcita = False
        self.pariv = False

        self.storona = 1

        self.sch_walk_tex = 0

        self.idle_texture = None
        self.jump_texture = None
        self.fall_texture = None
        self.udar_texture = None
        self.block_texture = None
        self.smert_texture = None

        self.uron = 0
        self.udar = sposob.Udar(self, self.sprite_list, self.uron)

        self.walk_t = []

        self.is_on_ground = True
        self.x_odometr = 0

        self.kvadrat_radius = hit_box_and_radius.KvadratRadius(self.scale)

        self.oruzh_list = arcade.SpriteList()
        self.tip_slovar = {}

        self.pers = ''

        self.return_position = True
        self.rivok = False

        self.tipo_return = False

    def update_hp(self):
        if self.hp >= self.h:
            self.minus_hp = False
        if self.hp < 0:
            self.smert = True
        elif self.hp < self.h:
            self.h = self.hp
            print(f'{self.pers}:', self.hp)
            self.minus_hp = True
        elif self.hp > self.h:
            self.h = self.hp

    def update_storona(self, dx, physics_engine):
        if dx < -D_ZONE and self.storona == 0:
            self.storona = 1
        elif dx > D_ZONE and self.storona == 1:
            self.storona = 0

        for sprite in self.sprite_list:
            if self.kvadrat_radius.check_collision(sprite) and abs(dx) < D_ZONE:
                if self.center_x > sprite.center_x:
                    self.storona = 1
                elif self.center_x < sprite.center_x:
                    self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

    def block_func(self, zashchita=None):
        for tip in self.tip_slovar:
            if tip == 0:
                if self.s_block >= 30:
                    self.s_block = 0
                    zashchita.block = False
                    self.block = False

                if self.block:
                    zashchita.block = True
                    self.s_block += 1
            else:
                if self.s_block >= self.timer_for_s_block:
                    self.s_block = 0
                    self.block = False

                if self.block:
                    self.s_block += 1
                    self.texture = self.block_texture[self.storona]
                    self.tipo_return = True
            break

    def udar_func(self):
        self.udar.udar_texture = self.udar_texture
        self.udar.on_update()
        if len(self.oruzh_list) == 0:
            if self.udar.action:
                self.tipo_return = True
        # elif len(self.oruzh_list) > 0:
        #     for oruzh in self.oruzh_list:
        #         if self.udar.udar:
        #             oruzh.udar = True

    def idle_animation(self, dx):
        if abs(dx) < D_ZONE:
            self.texture = self.idle_texture[self.storona]
            self.tipo_return = True

    def jump_animation(self, dy):
        if not self.is_on_ground:
            if dy > D_ZONE:
                self.texture = self.jump_texture[self.storona]
                self.tipo_return = True
            elif dy < -D_ZONE:
                self.texture = self.fall_texture[self.storona]
                self.tipo_return = True

    def walk_animation(self):
        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]

    def return_position_func(self):
        return self.position


class Voyslav(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)
        self.pers = 'igrok'

        self.hp = 1000

        self.reakciya = 990

        self.s_udar = 10

        self.scale = 1

        main_patch = (":resources:images/animated_characters/male_adventurer/maleAdventurer")

        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_texture[0]

        self.shchit = sposob.Shchit(self, self.sprite_list)
        self.tip_slovar.update(self.shchit.tip)

        self.oruzh_list.append(self.shchit)

        self.molniya = sposob.CepnayaMolniay(self, self.sprite_list)
        self.gnev_Tora = sposob.GnevTora(self, self.sprite_list)
        self.streliPeruna = sposob.StreliPeruna(self, self.sprite_list)
        self.shar_mol = sposob.SharMolniay(self, self.sprite_list)

        for i in self.tip_slovar:
            if i == 0:
                self.zashcita = True

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False
        self.update_storona(dx, physics_engine)

        self.block_func(self.shchit)
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return

        self.idle_animation(dx)
        if self.tipo_return:
            return

        self.walk_animation()
        if self.tipo_return:
            return

    def on_update(self, delta_time: float = 1 / 60):
        self.update_hp()
        self.kvadrat_radius.position = self.position

        self.shchit.on_update()

        self.gnev_Tora.on_update()
        self.shar_mol.on_update()
        self.shar_mol.update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.block or self.block1 or self.shchit.udar:
            self.shchit.draw()

        self.shchit.update_animation()

        if (self.shar_mol.udar and self.shar_mol.zaryad_b) or self.shar_mol.zaryad:
            self.shar_mol.draw()
        self.shar_mol.update_animation()
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

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

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

        self.zashcita = False

        self.shcit = sposob.Shchit(self, self.sprite_list)
        if self.shcit.tip == 0:
            self.zashcita = True

        self.oruzh_list = arcade.SpriteList()
        self.mech = sposob.Mech(self, self.sprite_list, (10, 5))
        self.oruzh_list.append(self.mech)

        self.molniya = sposob.CepnayaMolniay(self.sprite_list, self)
        self.gnev_Tora = sposob.GnevTora(self.sprite_list, self)
        self.streliPeruna = sposob.StreliPeruna(self.sprite_list, self)
        self.veter_otalk = sposob.VeterOtalkivanie(self, self.sprite_list)
        self.kulak_gaia = sposob.KulakGaia(self, self.sprite_list)

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

        self.mech.on_update()
        self.shcit.on_update()

        self.veter_otalk.on_update()
        self.veter_otalk.update()
        self.gnev_Tora.on_update()
        self.kulak_gaia.on_update()

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
        if self.veter_otalk.s > 0:
            pass
            #self.veter_otalk.draw()
        self.veter_otalk.update_animation()
        self.kulak_gaia.draw()
        self.kulak_gaia.update_animation()


class Vrag(Pers):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False):
        super().__init__(sprite_list)
        self.force_x = 0
        self.force_y = 0

        self.radius_vid = hit_box_and_radius.Radius(5)
        self.radius_ataki = hit_box_and_radius.Radius(0.25)

        self.igrok = igrok
        self.igrok_list = arcade.SpriteList()
        self.igrok_list.append(igrok)
        self.v_drug_list = v_drug_list

        self.go = True
        self.d_zone = 25
        self.stop1 = False

        self.kast_scena = kast_scena

        self.udar.sprite_list = self.igrok_list

    def ii(self, dx, physics_engine):
        self.radius_vid.position = self.radius_ataki.position = self.kvadrat_radius.position = self.position
        if not self.smert:
            self.update_storona(dx, physics_engine)

            if self.radius_vid.check_collision(self.igrok) and not self.kast_scena:

                if self.igrok.center_x < self.radius_vid.center_x:
                    if abs(self.igrok.right - self.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                    else:
                        self.force_x = -15000
                        self.go = True
                        self.stop1 = False

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if self.kvadrat_radius.check_collision(sprite):
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
                        self.stop1 = False

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for sprite in self.sprite_list:
                                if self.kvadrat_radius.check_collision(sprite):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                for drug in self.v_drug_list:
                    if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone and not drug.go
                            and self.igrok.center_x > self.center_x):
                        self.go = False
                        self.force_x = 0.
                        self.stop1 = True
                        break
                    elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone and not drug.go
                          and self.igrok.center_x < self.center_x):
                        self.go = False
                        self.force_x = 0.
                        self.stop1 = True
                        break
                    else:
                        self.stop1 = False
            else:
                self.stop1 = False
                self.go = False
                self.force_x, self.force_y = 0., 0.

    def update_udar(self):
        if len(self.oruzh_list) == 0:
            if self.radius_ataki.check_collision(self.igrok):
                self.udar.action = True
            else:
                self.udar.action = False
        elif len(self.oruzh_list) > 0:
            for oruzh in self.oruzh_list:
                if self.radius_ataki.check_collision(self.igrok):
                    oruzh.udar = True
                else:
                    oruzh.udar = False
                oruzh.on_update()

    def return_force(self, xy: str):
        if not self.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y


class BetaBalvanchik(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, kast_scena)
        self.pers = 'betabalvanchik'

        self.hp = HP_VRAG

        self.scale = 1.2

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.smert_texture = arcade.load_texture_pair('nuzhno/smert.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_texture[0]

        self.mech = sposob.Mech(self, self.igrok_list, (60, 20))
        self.oruzh_list.append(self.mech)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert:
            self.ii(dx, physics_engine)

            self.block_func()
            if self.tipo_return:
                return
            self.udar_func()
            if self.tipo_return:
                return

            self.jump_animation(dy)
            if self.tipo_return:
                return
            self.idle_animation(dx)
            if self.tipo_return:
                return
            self.walk_animation()

    def on_update(self, delta_time: float = 1 / 60):
        self.update_hp()
        self.update_udar()

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


class VoinInnocentii(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, kast_scena)

        self.hp = HP_V_I
        self.reakciya = REAKCIYA_V_I

        self.rivok_distanc = 450

        self.scale = 1.1

        main_patch = ':resources:images/animated_characters/male_person/malePerson'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)

        self.texture = self.idle_texture[self.storona]

        self.rivok_sposob = sposob.Rivok(self, self.sprite_list)
        self.tip_slovar.update(self.rivok_sposob.tip)

        self.pers = 'voin_innocentii'

        self.dvuruch_mech = sposob.DvuruchMech(self, self.igrok_list)
        self.oruzh_list.append(self.dvuruch_mech)
        self.tip_slovar.update(self.dvuruch_mech.tip)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert:
            self.ii(dx, physics_engine)

            self.block_func()
            if self.tipo_return:
                return
            self.udar_func()
            if self.tipo_return:
                return

            self.rivok_func()
            if self.tipo_return:
                return

            self.jump_animation(dy)
            if self.tipo_return:
                return
            self.idle_animation(dx)
            if self.tipo_return:
                return
            self.walk_animation()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_hp()
        self.rivok_sposob.update()
        self.rivok_sposob.on_update()
        self.update_udar()

        if self.rivok_sposob.stop1:
            self.rivok_sposob.stop1 = False
            self.return_position = True
        else:
            self.return_position = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if not self.rivok_sposob.stop1 and self.rivok_sposob.action and self.rivok_sposob.s_kd >= 180:
            self.rivok_sposob.draw()
        self.rivok_sposob.update_animation()

        if self.dvuruch_mech.udar:
            self.dvuruch_mech.draw()
        self.dvuruch_mech.update_animation()

    def rivok_func(self):
        if self.radius_vid.check_collision(self.igrok) and not self.kast_scena:
            if self.igrok.center_x > self.radius_vid.center_x:
                if 150 < abs(self.igrok.left - self.right) <= self.rivok_distanc and not self.stop1:
                    self.rivok_sposob.action = True
            elif self.igrok.center_x < self.radius_vid.center_x:
                if 150 < abs(self.igrok.right - self.left) <= self.rivok_distanc and not self.stop1:
                    self.rivok_sposob.action = True

    def return_position_func(self):
        return self.rivok_sposob.return_positoin()


class Gromila(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, kast_scena)
        self.hp = HP_GROMILA
        self.uron = URON_GROMILA

        self.reakciya = REAKCIYA_GROMILA

        self.scale = 2

        main_patch = ':resources:images/animated_characters/male_person/malePerson'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/gronila_udar.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)

        self.texture = self.idle_texture[self.storona]

        self.pers = 'gromila'

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert:
            self.ii(dx, physics_engine)

            self.block_func()
            if self.tipo_return:
                return
            self.udar_func()
            if self.tipo_return:
                return

            self.jump_animation(dy)
            if self.tipo_return:
                return
            self.idle_animation(dx)
            if self.tipo_return:
                return
            self.walk_animation()
            if self.tipo_return:
                return

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_hp()

        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.udar.action:
            self.udar.draw()
        self.udar.update_animation()
