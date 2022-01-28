import os
import pathlib
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

ASSETS_PATH = pathlib.Path(__file__).parent.absolute().__str__()+'/../assets/'



def downsize( size, resize):
    return (size[0]//resize, size[1]//resize)


class Screen:

    def __init__(self):
        self.entities = {}
        self.ent_assets = []

        self.current_area = None
        self.tileset = {}
        #self.tileset_path = ASSETS_PATH+'tiles/tileset.png'
        self.load_tileset_assets()
        
        self.info = pyg.display.Info()
        self.DESKTOP_WIDTH  = self.info.current_w
        self.DESKTOP_HEIGHT = self.info.current_h

        self.window_size = (self.DESKTOP_WIDTH*2//3, self.DESKTOP_HEIGHT*2//3)
        self.display_size = (16*TILE_LEN, 9*TILE_LEN)

        self.display_x_offset = 0
        self.display_y_offset = 0

        flags = pyg.FULLSCREEN
        self.window_surface = pyg.display.set_mode(self.window_size)
        self.display = pyg.Surface(self.display_size)
        

    # TODO: test, first try for blitting images
    def load_tileset_assets(self):
        self.tileset = {
                ROCKS: pyg.image.load(ASSETS_PATH+'tiles/rocks.png'),
                GRASS: pyg.image.load(ASSETS_PATH+'tiles/grass.png'),
                }

    def update_display_offset(self, offset):
        self.display_y_offset += offset[0]
        self.display_y_offset += offset[1]

    def set_area(self, curr_area: Area):
        self.current_area = curr_area

    def get_area(self):
        return self.current_area

    def add_entity(self, entity: ent.Entity):
        self.entities[entity.get_ent_id()] = entity

    def get_entities(self):
        return self.entities

    def draw_on_display(self):
        pass

    def draw(self):
        self.window_surface.fill((0, 0, 0))
    
        # Display drawing -----------------
        x_start, y_start = self.display_x_offset // TILE_LEN, self.display_y_offset // TILE_LEN
        x_off, y_off = self.display_x_offset % TILE_LEN, self.display_y_offset % TILE_LEN
        for i, row in enumerate(self.current_area.get_tiles()[y_start:y_start+10]):
            for j, tile in enumerate(row[x_start:x_start+17]):
                self.display.blit(
                        self.tileset[tile],
                        (j*TILE_LEN-x_off, i*TILE_LEN-y_off))

        self.window_surface.blit(pyg.transform.scale(self.display, self.window_size), (0, 0))
        pyg.display.flip()


