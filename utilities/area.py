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

    sides = {
        'left': ('topl', 'botl'),
        'right': ('topr', 'botr'),
        'top': ('topl', 'topr'),
        'bot': ('botl', 'botr'),
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

    def get_tile_pos_from_coord(self, coord):
        return (self.tile_len * (coord[0]//self.tile_len), self.tile_len * (coord[1]//self.tile_len))

    def get_tile_from_pos(self, pos):
        return self.tiles[self.tileset[pos[1]//(self.tile_len)][pos[0]//self.tile_len]]

    def detect_collision(self, entity):
        pos = entity.get_pos()
        size = entity.get_size()
        n_collisions = 0
        rect = {
            'topl': False,
            'topr': False,
            'botl': False,
            'botr': False,
            }

        if self.get_tile_from_pos(pos).is_solid():
            n_collisions += 1
            rect['topl'] = True
        if self.get_tile_from_pos((pos[0]+size[0], pos[1])).is_solid():
            n_collisions += 1
            rect['topr'] = True
        if self.get_tile_from_pos((pos[0], pos[1]+size[1])).is_solid():
            n_collisions += 1
            rect['botl'] = True
        if self.get_tile_from_pos((pos[0]+size[0], pos[1]+size[1])).is_solid():
            n_collisions += 1
            rect['botr'] = True

        return (n_collisions, rect)

    def get_side(self, rect, side):
        return (rect[self.sides[side][0]], rect[self.sides[side][1]])

    def fix_side(self, entity, rect):
        pos = entity.get_pos()
        size = entity.get_size()

        if self.get_side(rect, 'top') == (True, True):
            pos = (pos[0], self.get_tile_pos_from_coord(pos)[1]+self.tile_len)
            entity.set_pos(pos)

        if self.get_side(rect, 'bot') == (True, True):
            pos = (pos[0], self.get_tile_pos_from_coord((pos[0], pos[1]+size[1]))[1]-size[1])
            entity.set_pos(pos)

        if self.get_side(rect, 'left') == (True, True):
            pos = (self.get_tile_pos_from_coord(pos)[0]+self.tile_len, pos[1])
            entity.set_pos(pos)

        if self.get_side(rect, 'right') == (True, True):
            pos = (self.get_tile_pos_from_coord((pos[0]+size[0], pos[1]))[0]-size[0], pos[1])
            entity.set_pos(pos)

    def fix_vertex(self, entity, rect):
        pass
        
    def fix_collions(self, entity):
        # different types of collision: vertex, side, angle,
        n_collisions, rect = self.detect_collision(entity)

        if n_collisions > 1:
            self.fix_side(entity, rect)
        
        if n_collisions == 1:
            self.fix_vertex(entity, rect)

