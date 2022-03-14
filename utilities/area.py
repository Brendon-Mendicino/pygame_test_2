import sys
import math
import entities as ent
import pathlib


ROCKS = '#'
GRASS = '*'

# Bit-map for collision detection
TOP =   (1 << 0)
BOT =   (1 << 1)
LEFT =  (1 << 2)
RIGHT = (1 << 3)


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
        LEFT: (TOP|LEFT, BOT|LEFT),
        RIGHT: (TOP|RIGHT, BOT|RIGHT),
        TOP: (TOP|LEFT, TOP|RIGHT),
        BOT: (BOT|LEFT, BOT|RIGHT),
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

    def get_tile_pos_from_coord(self, coord) -> tuple:
        return (self.tile_len * (coord[0]//self.tile_len), self.tile_len * (coord[1]//self.tile_len))

    def get_tile_from_pos(self, pos) -> Tile:
        return self.tiles[self.tileset[pos[1]//(self.tile_len)][pos[0]//self.tile_len]]

    def detect_collision(self, entity):
        pos = entity.get_pos()
        size = entity.get_size()
        n_collisions = 0
        rect = {
            TOP|LEFT: False,
            TOP|RIGHT: False,
            BOT|LEFT: False,
            BOT|RIGHT: False,
            }

        if self.get_tile_from_pos(pos).is_solid():
            n_collisions += 1
            rect[TOP|LEFT] = True

        if self.get_tile_from_pos((pos[0]+size[0], pos[1])).is_solid():
            n_collisions += 1
            rect[TOP|RIGHT] = True

        if self.get_tile_from_pos((pos[0], pos[1]+size[1])).is_solid():
            n_collisions += 1
            rect[BOT|LEFT] = True

        if self.get_tile_from_pos((pos[0]+size[0], pos[1]+size[1])).is_solid():
            n_collisions += 1
            rect[BOT|RIGHT] = True

        return (n_collisions, rect)

    def get_side(self, rect, side):
        return (rect[self.sides[side][0]], rect[self.sides[side][1]])

    def fix_side(self, entity, rect):
        pos = entity.get_pos()
        size = entity.get_size()

        if self.get_side(rect, TOP) == (True, True):
            pos = (pos[0], self.get_tile_pos_from_coord(pos)[1]+self.tile_len)
            entity.set_pos(pos)

        if self.get_side(rect, BOT) == (True, True):
            pos = (pos[0], self.get_tile_pos_from_coord((pos[0], pos[1]+size[1]))[1]-size[1])
            entity.set_pos(pos)

        if self.get_side(rect, LEFT) == (True, True):
            pos = (self.get_tile_pos_from_coord(pos)[0]+self.tile_len, pos[1])
            entity.set_pos(pos)

        if self.get_side(rect, RIGHT) == (True, True):
            pos = (self.get_tile_pos_from_coord((pos[0]+size[0], pos[1]))[0]-size[0], pos[1])
            entity.set_pos(pos)

    def fix_vertex(self, entity, rect):
        pos = entity.get_pos()
        size = entity.get_size()
        # increse its module to avoid the previous postition to be inside the solid block
        negative_direction = (-entity.get_velocity()[0], -entity.get_velocity()[1])

        angle = 0
        for key, val in list(rect.items()):
            if val is True:
                angle = key

        if angle & TOP:
            if angle & LEFT:
                curr_pos = pos
            else:
                curr_pos = (pos[0]+size[0], pos[1])
        else:
            if angle & LEFT:
                curr_pos = (pos[0], pos[1]+size[1])
            else:
                curr_pos = (pos[0]+size[0], pos[1]+size[1])

        prev_pos = (curr_pos[0]+negative_direction[0], curr_pos[1]+negative_direction[1])

        # find intersection
        '''
           * ~> prev_pos
        +---\--+
        |    \ |
        |     *|~> curr_pos
        +------+

        The two * are the current point inside the block and the
        previous position.
        The alorithm finds the derction in which the intersection is and then
        it gets corrected in that direction.

        top-left |top| top-right
        ---------+---+----------
        left     |   | right
        ---------+---+----------
        bot-left |bot| bot-right
        '''

        tile_pos = self.get_tile_pos_from_coord(curr_pos)

        if prev_pos[1] < tile_pos[1]:
            ### top-left ###
            if prev_pos[0] < tile_pos[0]:
                # block on the left is solid
                if self.get_tile_from_pos((tile_pos[0]-self.tile_len, tile_pos[1])).is_solid():
                    pos = (pos[0], tile_pos[1]-size[1]-1)
                # block on the top is solid
                elif self.get_tile_from_pos((tile_pos[0], tile_pos[1]-self.tile_len)).is_solid():
                    pos = (tile_pos[0]-size[0]-1, pos[1])
                # no adjacent solid block
                else:
                    if angle is (BOT|RIGHT):
                        # calculte angular coeffiction
                        if (tile_pos[1]-prev_pos[1])/(tile_pos[0]-prev_pos[0]) > 1.0:
                            pos = (pos[0], tile_pos[1]-size[1]-1)
                        else:
                            pos = (tile_pos[0]-size[0]-1, pos[1])

                    elif angle is (TOP|RIGHT) or angle is (TOP|LEFT): 
                        pos = (tile_pos[0]-size[0]-1, pos[1])
                    else:
                        pos = (pos[0], tile_pos[1]-size[1]-1)

            ### top-right ###
            elif prev_pos[0] > tile_pos[0]+self.tile_len:
                # block on the right is solid
                if self.get_tile_from_pos((tile_pos[0]+self.tile_len, tile_pos[1])).is_solid():
                    pos = (pos[0], tile_pos[1]-size[1]-1)
                # block on the top is solid
                elif self.get_tile_from_pos((tile_pos[0], tile_pos[1]-self.tile_len)).is_solid():
                    pos = (tile_pos[0]+self.tile_len, pos[1])
                # no adjacent solid block
                else:
                    if angle is (BOT|LEFT):
                        # calculte angular coeffiction
                        if (tile_pos[1]-prev_pos[1])/(tile_pos[0]+self.tile_len-prev_pos[0]) < -1.0:
                            pos = (pos[0], tile_pos[1]-size[1]-1)
                        else:
                            pos = (tile_pos[0]+self.tile_len, pos[1])

                    elif angle is (TOP|LEFT) or angle is (TOP|RIGHT): 
                        pos = (tile_pos[0]+self.tile_len, pos[1])
                    else:
                        pos = (pos[0], tile_pos[1]-size[1]-1)
    
            ### top ###
            else: # tile_pos[0] < prev_pos[0] < tile_pos[0]+self.tile_len
                pos = (pos[0], tile_pos[1]-size[1]-1)
        
        elif prev_pos[1] > tile_pos[1]+self.tile_len:
            
            ### bot-left ###
            if prev_pos[0] < tile_pos[0]:
                # block on the left is solid
                if self.get_tile_from_pos((tile_pos[0]-self.tile_len, tile_pos[1])).is_solid():
                    pos = (pos[0], tile_pos[1]+self.tile_len)
                # block on the bot is solid
                elif self.get_tile_from_pos((tile_pos[0], tile_pos[1]+self.tile_len)).is_solid():
                    pos = (tile_pos[0]-size[0]-1, pos[1])
                # no adjacent solid block
                else:
                    if angle is (TOP|RIGHT):
                        # calculte angular coeffiction
                        if (tile_pos[1]+self.tile_len-prev_pos[1])/(tile_pos[0]-prev_pos[0]) < -1.0:
                            pos = (pos[0], tile_pos[1]+self.tile_len)
                        else:
                            pos = (tile_pos[0]-size[0]-1, pos[1])
                            
                    elif angle is (BOT|RIGHT) or angle is (BOT|LEFT):
                        pos = (tile_pos[0]-size[0]-1, pos[1])
                    else:
                        pos = (pos[0], tile_pos[1]+self.tile_len)

            ### bot-right ###
            elif prev_pos[0] > tile_pos[0]+self.tile_len:
                # block on the right is solid
                if self.get_tile_from_pos((tile_pos[0]+self.tile_len, tile_pos[1])).is_solid():
                    pos = (pos[0], tile_pos[1]+self.tile_len)
                # block on the bot is solid
                elif self.get_tile_from_pos((tile_pos[0], tile_pos[1]+self.tile_len)).is_solid():
                    pos = (tile_pos[0]+self.tile_len, pos[1])
                # no adjacent solid block
                else:
                    if angle is (TOP|LEFT):
                        if (tile_pos[1]+self.tile_len-prev_pos[1])/(tile_pos[0]+self.tile_len-prev_pos[0]) > 1.0:
                            pos = (pos[0], tile_pos[1]+self.tile_len)
                        else:
                            pos = (tile_pos[0]+self.tile_len, pos[1])

                    elif angle is (BOT|LEFT) or angle is (BOT|RIGHT):
                        pos = (tile_pos[0]+self.tile_len, pos[1])
                    else:
                        pos = (pos[0], tile_pos[1]+self.tile_len)

            ### bot ###
            else:
                pos = (pos[0], tile_pos[1]+self.tile_len)

        else: # tile_pos[1] < prev_pos[1] < tile_pos[1]+self.tile_len
            ### left ###
            if prev_pos[0] < tile_pos[0]:
                pos = (tile_pos[0]-size[0]-1, pos[1])
            ### right ###
            else:
                pos = (tile_pos[0]+self.tile_len, pos[1])

        entity.set_pos(pos)
        
    def fix_collions(self, entity):
        # different types of collision: vertex, side, angle,
        n_collisions, rect_of_collions = self.detect_collision(entity)

        if n_collisions > 1:
            self.fix_side(entity, rect_of_collions)
        
        if n_collisions == 1:
            self.fix_vertex(entity, rect_of_collions)

