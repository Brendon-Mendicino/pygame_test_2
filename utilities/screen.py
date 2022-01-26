import pygame as pyg
import entities as ent

class Screen:

    def __init__(self):
        self.entities = {}
        
        self.info = pyg.display.Info()
        self.DESKTOP_WIDTH  = self.info.current_w
        self.DESKTOP_HEIGHT = self.info.current_h
        self.size = ( self.DESKTOP_WIDTH//2, self.DESKTOP_HEIGHT//2)

        flags = pyg.FULLSCREEN
        self.window_surface = pyg.display.set_mode(self.size)


    def add_entity(self, entity: ent.Entity):
        self.entities[entity.get_ent_id()] = entity

    def get_entities(self):
        return self.entities

    def draw(self):
        self.window_surface.fill((0, 0, 0))

        pyg.display.update()
