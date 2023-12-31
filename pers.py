import arcade
import hit_box_and_radius
import sposob
import arcade.gui
import random


KOOR_X = 100
KOOR_Y = 500
D_ZONE = 0.005

# ___Voyslav___
HP_VOYSLAV = 1200
MANA_VOYSLAV = 350
STAMINA_VOYSLAV = 200


# ___Balvanchik___
HP_BETA_BALVANCHIK = 10000
MANA_BETA_BALVANCHIK = 300
STAMINA_BETA_BALVANCHIK = 300
# ______________________


# ___Voin_Innocentii___
HP_V_I = 900
MANA_V_I = 100
STAMINA_V_I = 100
REAKCIYA_V_I = 65
# ______________________


# ___Gromila___
HP_GROMILA = 1500
STAMINA_GROMILA = 100
URON_GROMILA = 120
REAKCIYA_GROMILA = 10
# ______________________


# ___ZhitelInnocentii___
HP_ZHITEL_IN = 300
STAMINA_ZHITEL_IN = 30
REAKCIYA_ZHITEL_IN = 20
# ______________________


# ___Brend___
HP_BREND = 1200
STAMINA_BREND = 200
REAKCIYA_BREND = 70


class Pers(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list

        self.max_hp = 0
        self.hp = 0
        self.hp_print = 0
        self.max_mana = 0
        self.mana = 0
        self.mana_print = 0
        self.max_stamina = 0
        self.stamina = 0
        self.stamina_print = 0
        self.smert = False
        self.minus_hp = False

        self.mor = False
        self.s_mor = 0
        self.timer_for_s_mor = 600
        self.slabweak = False
        self.s_slabweak = 0
        self.timer_for_s_slabweak = 60

        self.oglush = False
        self.s_oglush = 0
        self.timer_for_s_oglush = 0

        self.reakciya = 0
        self.block = sposob.Block(self, self.sprite_list)
        self.sil = False
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
        self.block_list = arcade.SpriteList()
        self.sposob_list = arcade.SpriteList()

        self.pers = ''

        self.return_position = True
        self.tipo_return = False

    def update_harakteristiki(self, vivod=False):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp >= self.hp_print:
            self.minus_hp = False
        if self.hp <= 0:
            self.smert = True
            for oruzh in self.oruzh_list:
                oruzh.action = False
        elif self.hp < self.hp_print:
            self.hp_print = self.hp
            if vivod:
                print(f'{self.pers} hp:', self.hp)
            self.minus_hp = True
        elif self.hp > self.hp_print:
            self.hp_print = self.hp
        elif self.hp > 0:
            self.smert = False

        if self.mor:
            self.s_mor += 1
            if self.s_mor >= self.timer_for_s_mor:
                self.mor = False
        if self.mana < self.max_mana:
            if not self.mor:
                self.mana += 1 / 60
            else:
                self.mana += 0.5 / 60
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.mana < self.mana_print:
            self.mana_print = self.mana
            if vivod:
                print(f'{self.pers} mana:', round(self.mana), self.mor)
        elif self.mana > self.mana_print:
            self.mana_print = self.mana
        if self.mana < 0:
            self.hp -= 0.5 / 60
            self.s_mor = 0
            self.mor = True

        if self.slabweak:
            self.s_slabweak += 1
            if self.s_slabweak >= self.timer_for_s_slabweak:
                self.slabweak = False
        if self.stamina < self.max_stamina:
            if not self.slabweak:
                self.stamina += 1 / 60
            else:
                self.stamina += 0.2 / 60
        if self.stamina >= self.max_stamina:
            self.stamina = self.max_stamina
        if self.stamina < self.stamina_print:
            self.stamina_print = self.stamina
            if vivod:
                print(f'{self.pers} stamina:', round(self.stamina), self.slabweak)
        elif self.stamina > self.stamina_print:
            self.stamina_print = self.stamina
        if self.stamina < 0:
            self.slabweak = True
            self.mana -= 2 / 60
            self.stamina += 0.5 / 60
            self.s_slabweak = 0

    def harakteristiki(self):
        self.hp = self.hp_print = self.max_hp
        self.mana = self.mana_print = self.max_mana
        self.stamina = self.stamina_print = self.max_stamina

    def update_storona(self, dx, physics_engine):
        rf = False
        for block in self.block_list:
            if block.rf:
                rf = True
        if not rf:
            if dx < -D_ZONE and self.storona == 0:
                self.storona = 1
            elif dx > D_ZONE and self.storona == 1:
                self.storona = 0

            for sprite in self.sprite_list:
                for oruzh in self.oruzh_list:
                    if self.kvadrat_radius.check_collision(sprite) and abs(dx) < D_ZONE and sprite.hp > 0:
                        if self.center_x > sprite.center_x:
                            self.storona = 1
                        elif self.center_x < sprite.center_x:
                            self.storona = 0
                    if self.kvadrat_radius.check_collision(sprite) and oruzh.action and sprite.hp > 0:
                        if self.center_x > sprite.center_x:
                            self.storona = 1
                        elif self.center_x < sprite.center_x:
                            self.storona = 0

        self.is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometr += dx

    def udar_func(self):
        self.udar.udar_texture = self.udar_texture
        self.udar.on_update()
        if len(self.oruzh_list) == 0:
            if self.udar.action:
                self.tipo_return = True

    def block_func(self):
        block = False
        self.block.update_block()
        for oruzh in self.oruzh_list:
            if oruzh.tip // 100 == 1:
                block = False
                break
            else:
                block = True
        if (self.block.block or self.block.avto_block) and block:
            self.texture = self.block_texture[self.storona]
            self.hit_box._points = self.texture.hit_box_points

    def idle_animation(self, dx):
        if abs(dx) < D_ZONE:
            self.texture = self.idle_texture[self.storona]
            self.hit_box._points = self.texture.hit_box_points
            self.tipo_return = True

    def jump_animation(self, dy):
        if not self.is_on_ground:
            if dy > D_ZONE:
                self.texture = self.jump_texture[self.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.tipo_return = True
            elif dy < -D_ZONE:
                self.texture = self.fall_texture[self.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.tipo_return = True

    def walk_animation(self):
        if abs(self.x_odometr) > 15:
            self.x_odometr = 0
            self.sch_walk_tex += 1
            if self.sch_walk_tex > 7:
                self.sch_walk_tex = 0
            self.texture = self.walk_t[self.sch_walk_tex][self.storona]
            self.hit_box._points = self.texture.hit_box_points

    def return_position_func(self):
        return self.position

    def update_kvadrat_radius(self):
        self.kvadrat_radius.scale = self.scale
        self.kvadrat_radius.position = self.position

    def slabweak_func(self, force, friction):
        if self.slabweak:
            return (0, 0), 1
        else:
            return force, friction

    def smert_func(self):
        self.center_y = 128
        if random.randint(0, 1) == 0:
            self.angle = 90 * -1
        else:
            self.angle = 90 * 1

    def oglush_force(self, force, friction, a):
        if self.oglush:
            if self.s_oglush >= self.timer_for_s_oglush:
                return force, friction
            return (0, 0), friction * a
        return force, friction

    def oglush_update(self):
        if self.oglush:
            self.s_oglush += 1
            if self.s_oglush >= self.timer_for_s_oglush:
                self.oglush = False
                self.s_oglush = 0

    def update_sposob_list(self):
        for sposob1 in self.sposob_list:
            sposob1.sprite_list = self.sprite_list


class Voyslav(Pers):
    def __init__(self, sprite_list, fizika):
        super().__init__(sprite_list)
        self.pers = 'igrok'

        self.max_hp = HP_VOYSLAV
        self.max_mana = MANA_VOYSLAV
        self.max_stamina = STAMINA_VOYSLAV
        self.reakciya = 990
        self.harakteristiki()

        self.scale = 1

        main_patch = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_texture[0]

        self.fizika = fizika

        self.shchit = sposob.Shchit(self, self.sprite_list, 15, 5, self.fizika)
        self.sposob_list.append(self.shchit)
        self.block_list.append(self.shchit)
        self.oruzh_list.append(self.shchit)

        self.molniya = sposob.CepnayaMolniay(self, self.sprite_list)
        self.sposob_list.append(self.molniya)
        self.gnev_Tora = sposob.GnevTora(self, self.sprite_list)
        self.sposob_list.append(self.gnev_Tora)
        self.streliPeruna = sposob.StreliPeruna(self, self.sprite_list)
        self.sposob_list.append(self.streliPeruna)
        self.shar_mol = sposob.SharMolniay(self, self.sprite_list)
        self.sposob_list.append(self.shar_mol)
        self.udar_Zevsa = sposob.UdarZevsa(self, self.sprite_list)
        self.sposob_list.append(self.udar_Zevsa)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False
        if not self.smert and not self.oglush:
            self.update_storona(dx, physics_engine)

            self.block_func()
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
        self.update_harakteristiki(True)
        self.mana += 1 / 60

        self.update_sposob_list()
        self.update_kvadrat_radius()
        self.oglush_update()

        self.shchit.fizika = self.fizika
        self.shchit.on_update()

        self.gnev_Tora.on_update()
        self.shar_mol.on_update()
        self.shar_mol.update()
        self.udar_Zevsa.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.block.block or self.block.avto_block or self.shchit.action:
            self.shchit.draw()

        self.shchit.update_animation()

        if (self.shar_mol.udar and self.shar_mol.zaryad_b) or self.shar_mol.zaryad:
            self.shar_mol.draw()
        self.shar_mol.update_animation()
        self.molniya.update_animation()
        self.gnev_Tora.update_animation()
        self.streliPeruna.update_animation()
        self.udar_Zevsa.update_animation()


class BetaMaster(Pers):
    def __init__(self, sprite_list, fizika):
        super().__init__(sprite_list)
        self.max_hp = 10000
        self.max_mana = 500
        self.max_stamina = 500
        self.harakteristiki()

        self.reakciay = 1000

        self.center_x = 0
        self.center_y = 3000
        self.scale = 1

        main_patch = "nuzhno/male_adventurer/maleAdventurer"

        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_texture[0]

        self.shchit = sposob.Shchit(self, self.sprite_list, 10, 10, fizika)
        self.oruzh_list.append(self.shchit)

        self.mech = sposob.Mech(self, self.sprite_list, 10, 5)
        self.oruzh_list.append(self.mech)

        self.molniya = sposob.CepnayaMolniay(self, self.sprite_list)
        self.gnev_Tora = sposob.GnevTora(self, self.sprite_list)
        self.streliPeruna = sposob.StreliPeruna(self, self.sprite_list)
        self.veter_otalk = sposob.VeterOtalkivanie(self, self.sprite_list)
        self.kulak_gaia = sposob.KulakGaia(self, self.sprite_list)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False
        self.update_storona(dx, physics_engine)

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

    def on_update(self, delta_time: float = 1 / 60):
        self.update_harakteristiki()

        self.update_kvadrat_radius()

        self.mech.on_update()
        self.shchit.on_update()

        self.veter_otalk.on_update()
        self.veter_otalk.update()
        self.gnev_Tora.on_update()
        self.kulak_gaia.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.mech.action:
            self.mech.draw()
        if self.block.block or self.block.avto_block or self.shchit.action:
            self.shchit.draw()
        self.shchit.update_animation()
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
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(sprite_list)
        self.force_x = 0
        self.force_y = 0

        self.radius_vid = hit_box_and_radius.Radius(5)
        self.radius_ataki = hit_box_and_radius.Radius(0.25)

        self.igrok = igrok
        self.sprite_list.append(self.igrok)
        self.v_drug_list = v_drug_list

        self.walls_list = walls_list

        self.go = True
        self.d_zone = 25
        self.stop1 = False

        self.kast_scena = kast_scena
        self.tip = tip

        self.udar.sprite_list = self.sprite_list

    def ii(self, dx, physics_engine):
        self.update_kvadrat_radius()
        self.radius_vid.position = self.radius_ataki.position = self.position
        if not self.smert:
            self.update_storona(dx, physics_engine)

            if self.radius_vid.check_collision(self.igrok) and not self.kast_scena:
                if self.igrok.center_x < self.radius_vid.center_x:
                    if abs(self.igrok.right - self.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 1
                    else:
                        self.force_x = -15000
                        self.go = True
                        self.stop1 = False

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                elif self.igrok.center_x > self.radius_vid.center_x:
                    if abs(self.right - self.igrok.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 0
                    else:
                        self.force_x = 15000
                        self.go = True
                        self.stop1 = False

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
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
        if not self.smert and not self.kast_scena and not self.oglush:
            if len(self.oruzh_list) == 0:
                if self.radius_ataki.check_collision(self.igrok):
                    self.udar.action = True
                else:
                    self.udar.action = False
            elif len(self.oruzh_list) > 0:
                for oruzh in self.oruzh_list:
                    if self.radius_ataki.check_collision(self.igrok) and oruzh.tip == self.tip:
                        oruzh.action = True
                    else:
                        oruzh.action = False
                    oruzh.on_update()
                    oruzh.update()

    def return_force(self, xy: str):
        if not self.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y

    def oruzh_update_animation(self):
        if len(self.oruzh_list) > 0:
            for oruzh in self.oruzh_list:
                if oruzh.tip == self.tip:
                    if oruzh.action:
                        oruzh.draw()
                    oruzh.update_animation()
        else:
            if self.udar.action:
                self.udar.draw()
                self.udar.update_animation()


class BetaBalvanchik(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.pers = 'betabalvanchik'

        self.max_hp = HP_BETA_BALVANCHIK
        self.max_mana = MANA_BETA_BALVANCHIK
        self.max_stamina = STAMINA_BETA_BALVANCHIK
        self.harakteristiki()

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

        self.mech = sposob.Mech(self, self.sprite_list, 20, 60)
        self.sposob_list.append(self.mech)
        self.oruzh_list.append(self.mech)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert and not self.kast_scena and not self.oglush:
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
        self.update_harakteristiki()
        self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60):
        self.oruzh_update_animation()


class VoinInnocentii(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)

        self.max_hp = HP_V_I
        self.max_mana = MANA_V_I
        self.max_stamina = STAMINA_V_I
        self.reakciya = REAKCIYA_V_I
        self.harakteristiki()

        self.rivok_distanc = 800

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

        self.rivok_sposob = sposob.Rivok(self, sprite_list)

        self.pers = 'voin_innocentii'

        self.dvuruch_mech = sposob.DvuruchMech(self, self.sprite_list, 15, 60)
        self.sposob_list.append(self.dvuruch_mech)
        self.oruzh_list.append(self.dvuruch_mech)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert and not self.kast_scena and not self.oglush:
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
        self.update_harakteristiki()
        self.oglush_update()
        if not self.smert or not self.kast_scena or not self.oglush:
            self.rivok_sposob.update()
            self.rivok_sposob.on_update()
        self.update_udar()

        if self.rivok_sposob.stop1 or self.rivok_sposob.s >= self.rivok_sposob.timer_for_s:
            self.rivok_sposob.stop1 = False
            self.return_position = True
        else:
            self.return_position = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if not self.rivok_sposob.stop1 and self.rivok_sposob.action and self.rivok_sposob.s_kd >= 180:
            self.rivok_sposob.draw()

        if not self.smert and not self.kast_scena and not self.oglush:
            self.rivok_sposob.update_animation()
            self.oruzh_update_animation()

    def rivok_func(self):
        if not self.smert and not self.kast_scena and not self.oglush:
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
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_GROMILA
        self.max_stamina = STAMINA_GROMILA
        self.uron = URON_GROMILA
        self.harakteristiki()

        self.sil = True

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
        self.udar.minus_stamina = 5

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert and not self.kast_scena and not self.oglush:
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

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_harakteristiki()
        self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()


class ZhitelInnocentii(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=(0,0), kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_ZHITEL_IN
        self.max_stamina = STAMINA_ZHITEL_IN
        self.reakciya = REAKCIYA_ZHITEL_IN
        self.harakteristiki()

        self.scale = 0.9

        main_patch = ':resources:images/animated_characters/female_person/femalePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')
        self.udar_texture = arcade.load_texture_pair(f'{main_patch}climb0.png')
        self.texture = self.idle_texture[1]
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}walk{i}.png")
            self.walk_t.append(tex)

        self.pers = 'zhitel_innocentii'

        self.vila = sposob.Vila(self, self.sprite_list)
        self.sposob_list.append(self.vila)
        self.oruzh_list.append(self.vila)
        self.topor = sposob.Topor(self, self.sprite_list, 30, 20)
        self.sposob_list.append(self.topor)
        self.oruzh_list.append(self.topor)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert and not self.kast_scena and not self.oglush:
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

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_harakteristiki()
        self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()


class Brend(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=206, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_BREND
        self.max_stamina = STAMINA_BREND
        self.reakciya = REAKCIYA_BREND
        self.harakteristiki()

        main_patch = ':resources:images/animated_characters/male_adventurer/maleAdventurer'
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')
        self.scale = 1.05

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_t.append(tex)
        self.texture = self.idle_texture[self.storona]

        self.mech_Brenda = sposob.MechBrenda(self, self.sprite_list, 10, 10)
        self.sposob_list.append(self.mech_Brenda)
        self.oruzh_list.append(self.mech_Brenda)

        self.pers = 'Brend'

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        if not self.smert and not self.kast_scena and not self.oglush:
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

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_harakteristiki()
        self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()
