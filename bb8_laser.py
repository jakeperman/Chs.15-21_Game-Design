# Sign your name:________________

# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade
import timeit
import time

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 10
bullet_scale = 1
SP = 4
SW = 800
SH = 600


class Bullet(arcade.Sprite):
    def __init__(self, x, y, dy):
        super(Bullet, self).__init__("Images/bullet.png", bullet_scale)
        self.center_x, self.center_y = x, y
        self.change_x = dy
        self.angle = 90
        self.lifetime = time.perf_counter()

    def update(self):
        self.center_y += self.change_x


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("Images/bb8.png", BB8_scale)
        self.center_x, self.center_y = x, y
        self.bullets = arcade.SpriteList()
        self.cooldown_time = 10  # in a unit of time
        self.lives = 3

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right >= SW + 7:
            self.left = 5
        elif self.left <= -7:
            self.right = SW - 5
        elif self.bottom <= 0:
            self.center_y = self.width / 2
        elif self.top >= SH:
            self.center_y = SH - self.width / 2

        if self.bullets:
            for bullet in self.bullets:
                bullet.update()
                if bullet.center_y > SH:
                    self.bullets.remove(bullet)
                    bullet.kill()

    def shoot_laser(self, speed):
        if self.bullets:
            cooldown = (5 / 60) * (self.bullets[-1].center_y - self.top)
            if cooldown > self.cooldown_time:
                self.bullets.append(Bullet(self.center_x, self.top, speed))
        else:
            self.bullets.append(Bullet(self.center_x, self.top, speed))

    def set_x(self, x):
        self.change_x = x

    def set_y(self, y):
        self.change_y = y


class Trooper(arcade.Sprite):
    def __init__(self, x, y, dy):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.center_x, self.center_y = x, y
        self.change_y = dy

    def update(self):
        self.center_y += self.change_y


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # setup variables
        self.trooper_list = self.players = self.player = None

        # set background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.set_vsync(True)

        # set score
        self.score = 0
        self.setup()

        self.set_mouse_visible(True)

    def setup(self):

        # initialize sprite lists
        self.trooper_list = arcade.SpriteList()
        self.players = arcade.SpriteList()

        # create the player
        self.player = Player(SW / 2, 50)
        self.players.append(self.player)
        self.game_over = False

        # setup the controls
        self.controls = {
            'w': {'func': self.player.shoot_laser, 'param': 5},
            'a': {'func': self.player.set_x, 'param': -3},
            'd': {'func': self.player.set_x, 'param': 3}
        }
        self.keys_pressed = []
        # generate enemies at random points on screen
        for trooper in range(trooper_count):
            x, y = random.randint(0, SW), random.randint(SH - 100, SH)
            self.trooper_list.append(Trooper(x, y, -1))

        # setup score
        self.score = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"Score: {self.score}", SW / 2, SH - 50, arcade.color.BLACK, 25)
        self.players.draw()
        self.player.bullets.draw()
        self.trooper_list.draw()
        arcade.draw_text(f"Lives Remaining:{self.player.lives}", 50, SH - 50, arcade.color.RED, 25)
        if self.game_over:
            arcade.draw_text("GAME OVER", SW / 2, SW / 2, arcade.color.BLACK, 50, anchor_x="center")

    def on_update(self, dt):
        self.player.update()
        self.key_change()
        self.trooper_list.update()

        collisions = arcade.check_for_collision_with_list(self.player, self.trooper_list)
        if collisions:
            self.player.lives -= 1
            collisions[0].kill()
            # for trooper in collisions:
            #     pass
        if not self.player.lives:
            self.game_over = True
        if self.player.bullets:
            for bullet in self.player.bullets:
                hits = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if hits:
                    self.score += 1
                    bullet.kill()
                    hits[0].kill()

        for trooper in self.trooper_list:
            if trooper.center_y < 0:
                self.game_over = True

        if len(self.trooper_list) == 0:
            self.setup()

    def key_change(self):
        for key in self.keys_pressed:
            action = self.controls[key]
            action['func'](action['param'])

    def add_trooper(self, count):
        self.trooper_list.append(Trooper(10, 10, -2))

    def on_key_press(self, symbol: int, modifiers: int):
        key = chr(symbol)
        if key in list(self.controls.keys()):
            self.keys_pressed.append(key)

    def on_key_release(self, symbol: int, modifiers: int):
        key = chr(symbol)
        if key in list(self.controls.keys()):
            if key in 'ad':
                self.player.change_x = 0
            elif key in 'ws':
                self.player.change_y = 0
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # self.BB8.shoot()
        pass


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
