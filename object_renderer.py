import pygame as pg
from settings import *


class ObjectRenderer:

    def __init__(self, game):
        """-------"""
        # changed settings
        w, h = pg.display.get_window_size()
        half_width = w // 2
        half_height = h // 2
        num_rays = w // 2
        # couldn't put them out of def due to not open window so, I have put them to its one separately
        # apparently i could make a def at settings for solving the problem and access through there but i am too lazy
        """-------"""
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (w, half_height))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        """-------"""
        # changed settings
        w, h = pg.display.get_window_size()
        half_width = w // 2
        half_height = h // 2
        num_rays = w // 2
        half_num_rays = num_rays // 2
        screen_dist = half_width / math.tan(HALF_FOV)
        scale = w // num_rays
        delta_angle = FOV / num_rays
        # couldn't put them out of def due to not open window so, I have put them to its one separately
        """-------"""
        if w > h:
            self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % w
            self.screen.blit(self.sky_image, (-self.sky_offset, 0))
            self.screen.blit(self.sky_image, (-self.sky_offset + w, 0))
        elif h > w:
            self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % h
            self.screen.blit(self.sky_image, (-self.sky_offset, 0))
            self.screen.blit(self.sky_image, (-self.sky_offset + h, 0))

        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, half_height, w, h))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png')
        }