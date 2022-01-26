
class Stats:

    def __init__(self,
            max_hp = 1,
            hp  = 1,
            atk = 1,
            mag = 1,
            defs = 1,
            mdef = 1,
            spd = 1
            ):
        self.max_hp = max_hp
        self.hp = hp
        self.atk = atk
        self.mag = mag
        self.defs = defs
        self.mdef = mdef
        self.spd = spd

            


class Entity:

    def __init__(self,
            ent_id,
            x,
            y,
            front_anim_path,
            back_anim_path,
            left_anim_path,
            right_anim_path):
        self.ent_id = ent_id
        self.x = x
        self.y = y

        self.front_anim_path = frot_anim_path
        self.back_anim_path = back_anim_path
        self.left_anim_path = left_anim_path
        self.right_anim_path = right_anim_path

        self.stats = Stats()


    def move(self, dx, dy):
        self.x += dx
        sefl.y += dy


    def get_ent_id(self):
        return self.ent_id

    def get_pos(self):
        return (self.x, self.y)

    def update_stats(self):
        pass
