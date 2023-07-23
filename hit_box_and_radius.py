import arcade


class Radius(arcade.Sprite):
    def __init__(self, razmer=0.2):
        super().__init__()

        self.rad = load_tex_pair('nuzhno/radius_porazheniya.png')

        self.scale = razmer

        self.texture = self.rad[1]

    def check_collision(self, sprite=None, sprite_list=None):
        if sprite_list is not None:
            if arcade.check_for_collision_with_list(self, sprite_list):
                collision = True
            else:
                collision = False
        elif sprite is not None:
            if arcade.check_for_collision(self, sprite):
                collision = True
            else:
                collision = False

        return collision


def load_tex_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
