import sys


GRASS = '*'
ROCKS = '#'


class Area:

    def __init__(self, path_name):
        self.tiles = []
        self.path_name = path_name

        with open(path_name, 'r') as input_file:
            for line in input_file.readlines():
                self.tiles.append(line.replace('\n', ''))

    def get_tiles(self):
        return self.tiles
