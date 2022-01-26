from entity import Entity


class Player(Entity):
    
    def __init__(self, ent_id, x, y):
        super().__init__( ent_id, x, y)

