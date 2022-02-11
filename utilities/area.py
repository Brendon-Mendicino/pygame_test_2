import sys
import math
import entities as ent
import pathlib


ROCKS = '#'
GRASS = '*'


class Tile:

    def __init__(self, id, size, solid):
        self.id = id
        self.size = size
        self.solid = solid

    def get_id(self):
        return self.id

    def get_size(self):
        return self.size

    def is_solid(self):
        return self.solid



class Area:

    tile_len = 30 #pixel
    tiles = {
        ROCKS: Tile(ROCKS, (30, 30), True),
        GRASS: Tile(GRASS, (30, 30), False),
        }


    def __init__(self, path_name):
        self.tileset = []
        self.path_name = path_name
        self.scale = 1

        with open(path_name, 'r') as input_file:
            for line in input_file.readlines():
                self.tileset.append(line.replace('\n', ''))

    def get_tileset(self):
        return self.tileset

    def set_scale(self, scale):
        self.scale = scale
        # TODO: calculate previous scale
        self.tile_len = math.floor(self.tile_len*self.scale)

    def get_tile_from_pos(self, pos):
        print((pos[0], pos[1]))
        print((pos[0]//self.tile_len, pos[1]//self.tile_len))
        return self.tiles[self.tileset[pos[1]//(self.tile_len)][pos[0]//self.tile_len]]

    def check_collision(self, entity):
        pos = entity.get_pos()
        size = entity.get_size()
        if self.get_tile_from_pos(pos).is_solid():
            return True
        if self.get_tile_from_pos((pos[0]+size[0], pos[1])).is_solid():
            return True
        if self.get_tile_from_pos((pos[0], pos[1]+size[1])).is_solid():
            return True
        if self.get_tile_from_pos((pos[0]+size[0], pos[1]+size[1])).is_solid():
            return True
        return False
        

