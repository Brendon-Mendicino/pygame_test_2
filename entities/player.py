from entities.entity import Entity
import pathlib

ASSETS_PATH = pathlib.Path(__file__).parent.absolute().__str__()+'/../assets/'

class Player(Entity):
    
    def __init__(self, ent_id, pos):
        super().__init__(ent_id, pos, (30, 30))
        super().add_assets(0, [0, 1, 2, 3],
                [ASSETS_PATH+'player/player_main_'+end for end in ['front.png', 'left.png', 'right.png', 'back.png']])

    def get_input_speed(self, speed):
        super().move(speed[0], speed[1])
