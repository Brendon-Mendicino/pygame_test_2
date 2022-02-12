from entities.entity import Entity
import pygame as pyg
import pathlib

ASSETS_PATH = pathlib.Path(__file__).parent.absolute().__str__()+'/../assets/'

DIR_COMPLEX = {
        pyg.K_UP: 0 - 1j,
        pyg.K_DOWN: 0 + 1j,
        pyg.K_RIGHT: 1 + 0j,
        pyg.K_LEFT: -1 + 0j,
        }

class Player(Entity):

    velocity = 0.4
    direction_table = {
            pyg.K_UP: False,
            pyg.K_DOWN: False,
            pyg.K_LEFT: False,
            pyg.K_RIGHT: False,
            }
    
    def __init__(self, ent_id, pos):
        super().__init__(ent_id, pos, (30, 30))
        super().add_assets(0, 10, [0, 1, 2, 3],
                [ASSETS_PATH+'player/player_main_'+end for end in ['front.png', 'left.png','back.png', 'right.png']])


    def set_input_direction(self, direction):
        if self.direction_table[direction] is False:
            self.direction_table[direction] = True
        else:
            self.direction_table[direction] = False
        self.update_velocity_vector()

    def normalize(self, vec):
        if abs(vec) ==  0:
            return 0.0
        return vec / abs(vec)

    def update_velocity_vector(self):
        vel_vector = 0j
        for d, val in list(self.direction_table.items()):
            if val is True:
                vel_vector += DIR_COMPLEX[d]
            
        vel_vector = self.normalize(vel_vector)*self.velocity
        super().set_offset_speed((vel_vector.real, vel_vector.imag))

