import pygame as pyg


IDLE = 0

NUMBER_OF_ANIMATION_TYPE = 1


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


class EntityAsset:

    def __init__(self, type, animation_frames, sprites_paths):
        self.type = type
        self.animations_frames = animations_frames
        self.sprites_paths = sprites_paths

    def get_type(self):
        return type

    def get_animations_frames(self):
        return self.animations_frames

    def get_sprites_paths(self):
        return self.sprites_paths


class Entity:

    def __init__(self, ent_id, pos, size):
        '''
        pos: coordinate all'interno dell'area
        size: size dello sprite
        '''
        self.ent_id = ent_id
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.curr_animation_type = IDLE
        self.assets = [EntityAsset(-1, [], []) for n in range(NUMBER_OF_ANIMATION_TYPE)]

        self.stats = Stats()

    def add_assets(self, type, animations_frames, sprites_paths):
        self.assets[type] = EntityAsset(type, animations_frames, sprites_paths)

    def get_sprites(self):
        assets_list = []
        for asset_type in self.assets:
            if asset_type.get_type() == -1:
                assets_list.append(None)
            else:
                assets_list.append( [pyg.image.load(sprite) for sprite in asset_type.get_sprites_paths()] )
        
        return assets_list

    def get_current_animation_info(self):
        return [self.curr_animation_type, self.assets[self.curr_animation_type].get_animations_frames()]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_ent_id(self):
        return self.ent_id

    def get_pos(self):
        return (self.x, self.y)

    def get_size(self):
        return self.size

    def update_stats(self):
        pass

