
class Stats:

    def __init__(self,
            hp  = 1,
            atk = 1,
            mag = 1,
            defs = 1,
            mdef = 1,
            spd = 1
            ):
        self.hp = hp
        self.atk = atk
        self.mag = mag
        self.defs = defs
        self.mdef = mdef
        self.spd = spd


class Entity:

    def __init__(self, ent_id, x, y):
        self.x = x
        self.y = y
        self.ent_id = ent_id

    def move(self, dx, dy):
        self.x += dx
        sefl.y += dy

    def get_ent_id(self):
        return self.ent_id

    def get_pos(self):
        return (self.x, self.y)
