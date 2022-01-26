import sys
import pygame as pyg
import entities as ent
import utilities.area as area
from utilities.area import Area



def resize( size, resize):
    return (size[0]//resize, size[1]//resize)

class Screen:


    def __init__(self):
        self.entities = {}
        self.ent_assets = []

        self.current_area = None
        
        self.info = pyg.display.Info()
        self.DESKTOP_WIDTH  = self.info.current_w
        self.DESKTOP_HEIGHT = self.info.current_h
        self.size = ( self.DESKTOP_WIDTH//2, self.DESKTOP_HEIGHT//2)

        flags = pyg.FULLSCREEN
        self.window_surface = pyg.display.set_mode(self.size)

        grass = pyg.transform.scale( pyg.image.load('assets/tiles/grass.png'), resize(self.size, 10))
        rocks = pyg.transform.scale( pyg.image.load('assets/tiles/rocks.png'), resize(self.size, 10))
        self.table = {
                area.GRASS: grass,
                area.ROCKS: rocks
                }


    def set_area(self, curr_area: Area):
        self.current_area = curr_area

    def get_area(self):
        return self.current_area


    def add_entity(self, entity: ent.Entity):
        self.entities[entity.get_ent_id()] = entity

    def get_entities(self):
        return self.entities

    def draw(self):
        self.window_surface.fill((0, 0, 0))

        for i, rows in enumerate(self.current_area.get_tiles()):
            for j, tile in enumerate(rows):
                self.window_surface.blit(
                        self.table[tile],
                        (i * self.table[tile].get_size()[0], j * self.table[tile].get_size()[1]))

        pyg.display.update()


