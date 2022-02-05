import os
import pathlib
import math
import pygame as pyg
import entities as ent
import utilities.area as area
from utilities.area import Area

import cmath
import math



ROCKS = '#'
GRASS = '*'

TILESET_LOOKUP_TABLE = {
        '#': ( 0, 0),
        '*': (30, 0),
        }

TILE_LEN = 30
TILE_ON_SCREEN_W = 16
TILE_ON_SCREEN_H = 9

SCREEN_RESOLUTIONS = {
        0: (1920, 1080),
        1: (1600,  900),
        2: (1440,  810),
        3: (1280,  720),
        4: ( 480,  270),
        }


ASSETS_PATH = pathlib.Path(__file__).parent.absolute().__str__()+'/../assets/'


def downsize( size, scale):
    return (size[0]//scale, size[1]//scale)



class Screen:

    def __init__(self):
        self.info = pyg.display.Info()
        self.DESKTOP_WIDTH  = self.info.current_w
        self.DESKTOP_HEIGHT = self.info.current_h

        self.display_size = SCREEN_RESOLUTIONS[3]
        self.scale_factor = self.display_size[0] / (TILE_LEN * TILE_ON_SCREEN_W)
        self.tile_len_scaled = math.floor( TILE_LEN * self.scale_factor)

        self.display_x_offset = 0
        self.display_y_offset = 0
        self.display_dx = 0
        self.display_dy = 0

        flags = pyg.FULLSCREEN
        self.display = pyg.display.set_mode(self.display_size)

        self.entities = { 0: ent.Player(0, (0, 0)), }  # for testing
        self.sprites_list = {} 
        self.ent_to_draw = []  # [>id [>anim_type [>frame, ...], ...], ...]

        self.current_area = None
        self.tileset = {}
        self.load_tileset_assets()
        
        

    # TODO: test, first try for blitting images
    def load_tileset_assets(self):
        rocks = pyg.image.load(ASSETS_PATH+'tiles/rocks.png')
        grass = pyg.image.load(ASSETS_PATH+'tiles/grass.png')

        self.tileset = {
                ROCKS: self.scale_surface(rocks),
                GRASS: self.scale_surface(grass),
                }

    def display_offset_speed(self, speed):
        self.display_dx += speed[0]
        self.display_dy += speed[1]

    def display_offset_speed_reset(self):
        self.display_dx, self.display_dy = 0, 0

    def set_area(self, curr_area: Area):
        self.current_area = curr_area

    def get_area(self):
        return self.current_area

    def scale_surface(self, sprite: pyg.Surface):
        return pyg.transform.scale(sprite,
                (math.floor(sprite.get_size()[0]*self.scale_factor), math.floor(sprite.get_size()[1]*self.scale_factor)))

    def add_entity(self, entity: ent.Entity):
        # TODO: push this to the handler
        entity.set_scale(self.scale_factor)
        # -------------------
        self.entities[entity.get_ent_id()] = entity
        sprites_scaled = []
        for s_list in entity.get_sprites():
            sprites_scaled.append([self.scale_surface(s) for s in s_list])
        self.sprites_list[entity.get_ent_id()] = sprites_scaled

    def get_entities(self):
        return self.entities

    def is_inside_display(self, pos, size):
        disp_x_len = self.display_x_offset + self.display_size[0]
        disp_y_len = self.display_y_offset + self.display_size[1]

        if self.display_x_offset < pos[0]+size[0] and disp_x_len > pos[0]:
            if self.display_y_offset < pos[1]+size[1] and disp_y_len > pos[1]:
                return True
        return False

    def update_entities_to_draw(self):
        self.ent_to_draw.clear()
        for enty in list(self.entities.values()):
            if self.is_inside_display(enty.get_pos(), enty.get_size()):
                self.ent_to_draw.append(enty.get_ent_id())

    def get_sprite_by_id(self, id):
        sprite_id = self.entities[id].get_current_sprite_info()
        return self.sprites_list[id][sprite_id[0]][sprite_id[1]]

    def center_sprite_pos(self, pos):
        return (pos[0]-self.display_x_offset, pos[1]-self.display_y_offset)

    def update_display_position(self, new_center):
        self.display_x_offset = new_center[0] - self.display_size[0] // 2
        self.display_y_offset = new_center[1] - self.display_size[1] // 2

    def draw(self):
        self.display.fill((0, 0, 0))
        # Area drawing -----------------
        x_start = self.display_x_offset // self.tile_len_scaled
        y_start = self.display_y_offset // self.tile_len_scaled
        x_off = self.display_x_offset % self.tile_len_scaled
        y_off = self.display_y_offset % self.tile_len_scaled

        # The display can't go above the 0 limit of the matrix
        for i, row in enumerate(self.current_area.get_tiles()[y_start:y_start+TILE_ON_SCREEN_H+1]):
            for j, tile_id in enumerate(row[x_start:x_start+TILE_ON_SCREEN_W+1]):
                self.display.blit(
                        self.tileset[tile_id],
                        (j*self.tile_len_scaled-x_off, i*self.tile_len_scaled-y_off))

        # Entity drawing ------------------
        for id in self.ent_to_draw:
            self.display.blit(
                    self.get_sprite_by_id(id),
                    self.center_sprite_pos(self.entities[id].get_pos()))
        
        #self.window_surface.blit(pyg.transform.scale(self.display, self.window_size), (0, 0))
        pyg.display.update()


