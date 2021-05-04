#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade
import timeit

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
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

    def update(self):
        self.center_y += self.change_x


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("Images/bb8.png", BB8_scale)
        self.center_x, self.center_y = x, y
        self.bullets = arcade.SpriteList()
        self.cooldown = 1
        self.cooldown_timer = 0

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
            self.center_y = SH - self.width/2

        if self.bullets:
            for bullet in self.bullets:
                bullet.update()
                if bullet.bottom > SH:
                    bullet.kill()

    def shoot(self):
        if self.bullets:
            if self.bullets[-1].bottom > self.top + 100:
                self.bullets.append(Bullet(self.center_x, self.top, 5))
        else:
            self.bullets.append(Bullet(self.center_x, self.top, 5))

    def set_x(self, x):
        self.change_x = x

    def set_y(self, y):
        self.change_y = y


class Trooper(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.center_x, self.center_y = x, y


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # setup variables
        self.trooper_list = self.players = self.BB8 = None

        # set background color
        arcade.set_background_color(arcade.color.SKY_BLUE)



        # set score
        self.score = 0
        self.setup()

        self.set_mouse_visible(True)

    def setup(self):

        # initialize sprite lists
        self.trooper_list = arcade.SpriteList()
        self.players = arcade.SpriteList()

        # create the player
        self.BB8 = Player(SW / 2, SH / 2)
        self.players.append(self.BB8)

        # setup the controls
        self.controls = {'w': self.BB8.shoot, 'a': self.BB8.set_x, 's': self.BB8.set_y, 'd': self.BB8.set_x}
        self.speeds = {'a': -3, 'd': 3}
        self.keys_pressed = []
        # generate enemies at random points on screen
        for trooper in range(trooper_count):
            x, y = random.randint(0, SW), random.randint(0, SH)
            self.trooper_list.append(Trooper(x, y))

        # setup score
        self.score = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"Score: {self.score}", SW/2, SH-50, arcade.color.BLACK, 25)
        self.players.draw()
        self.BB8.bullets.draw()
        self.trooper_list.draw()

    def on_update(self, dt):
        self.BB8.update()
        self.key_change()

        collisions = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if collisions:
            self.score += len(collisions)
            for trooper in collisions:
                self.trooper_list.remove(trooper)

        if len(self.trooper_list) == 0:
            self.setup()

    def key_change(self):
        for key in self.keys_pressed:
            func = self.controls[key]
            if key in 'ad':
                func(self.speeds[key])
            if key == 'w':
                func()





    def on_key_press(self, symbol: int, modifiers: int):
        key = chr(symbol)
        if key in list(self.controls.keys()):
            self.keys_pressed.append(key)



    def on_key_release(self, symbol: int, modifiers: int):
        key = chr(symbol)
        if key in list(self.controls.keys()):
            if key in 'ad':
                self.BB8.change_x = 0
            elif key in 'ws':
                self.BB8.change_y = 0
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # self.BB8.shoot()
        pass

#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    arcade.run()

#------Run Main Function-----
if __name__ == "__main__":
    main()
