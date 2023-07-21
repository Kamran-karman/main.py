import arcade
import hit_box_and_radius
import sposob

KOOR_X = 100
KOOR_Y = 300


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

        self.molniya = sposob.Molniay(sprite_list, self)
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


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
