import arcade


class Win(arcade.Window):
    def __init__(self):
        super().__init__()
        self.ig = arcade.Sprite(':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png')
        self.ig.position = 200, 100
        self.vr = arcade.Sprite(':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png', 1.5)
        self.wal_lis = arcade.SpriteList()
        self.l = False
        self.p = False
        self.fi = None

    def setup(self):
        for x in (-64, 864, 64):
            print(x)
            wal = arcade.Sprite(':resources:images/tiles/grassMid.png')
            wal.position = x, 64
            self.wal_lis.append(wal)

        self.fi = arcade.PymunkPhysicsEngine((0, -1000), 0.7)
        self.fi.add_sprite(self.ig, max_horizontal_velocity=3000, max_vertical_velocity=1200, collision_type='player')
        self.fi.add_sprite_list(self.wal_lis, collision_type='wall', body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_draw(self):
        self.clear()
        self.ig.draw()
        self.wal_lis.draw()

    def on_update(self, delta_time: float):
        if self.l and not self.p:
            force = (-2000, 0)
            self.fi.apply_force(self.ig, force)
            self.fi.set_friction(self.ig, 0)

        self.fi.step()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            self.l = False
            self.p = True
        elif symbol == arcade.key.LEFT:
            self.p = False
            self.l = True

win = Win()
win.setup()
arcade.run()

