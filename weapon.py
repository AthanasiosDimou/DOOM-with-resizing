from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        """-------"""
        # changed settings
        w, h = pg.display.get_window_size()
        half_width = w // 2
        half_height = h // 2
        num_rays = w // 2
        half_num_rays = num_rays // 2
        screen_dist = half_width / math.tan(HALF_FOV)
        scaLe = w // num_rays
        delta_angle = FOV / num_rays
        # couldn't put them out of def due to not open window so, I have put them to its one separately
        # apparently I could make a def at settings for solving the problem and access through there, but I am too lazy
        """-------"""
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
             for img in self.images])
        self.weapon_pos = (half_width - self.images[0].get_width() // 2, h - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()