import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []

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
        # apparently i could make a def at settings for solving the problem and access through there but i am too lazy
        """-------"""

        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < h:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - scale), 0, scale, TEXTURE_SIZE
                )
                # pygame.transform.scale(surface, (width, height), surface)
                wall_column = pg.transform.scale(wall_column, (abs(scale), abs(int(proj_height)))) # don't know why proj_height gets negative value during resizing the window with x > y
                wall_pos = (ray * scale, half_height - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * h / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - scale), HALF_TEXTURE_SIZE - texture_height // 2, scale, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (abs(scale), abs(int(h))))
                wall_pos = (ray * scale, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):

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
        # apparently I could make a def at settings for solving the problem and access through there, but I am too lazy
        """-------"""

        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(num_rays):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # draw for debug

            # pg.draw.line(self.game.screen, 'yellow', (width * ox, height * oy),
            #              (width * ox + width * depth * cos_a, height * oy + height * depth * sin_a), 2)

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = screen_dist / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # draw walls
            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            # pg.draw.rect(self.game.screen, color,
            #              (ray * scale, half_height - proj_height // 2, scale, proj_height))

            ray_angle += delta_angle



    def update(self):
        self.ray_cast()
        self.get_objects_to_render()