import utilities as util
import pygame as pyg

# TODO: set a table for all possible animations
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

    def __init__(self, type, frames_speed, animation_frames, sprites_paths):
        '''
        type: animation type
        frames_speed: number of frames showed every second
        animation_frames: 
        sprites_paths: absolute path of the current sprites path
        '''
        self.type = type
        self.frames_speed = frames_speed        # frames showed every second
        self.animation_frames = animation_frames
        self.sprites_paths = sprites_paths

    def get_type(self):
        return type

    def get_animation_frames(self):
        return self.animation_frames

    def get_frames_speed(self):
        return self.frames_speed

    def get_sprites_paths(self):
        return self.sprites_paths


class Entity:
    scale = 100
    sentinel_asset = EntityAsset(-1, 0, [], [])

    def __init__(self, ent_id, pos, size):
        '''
        pos: coordinate all'interno dell'area
        size: size dello sprite
        '''
        self.ent_id = ent_id
        self.x = pos[0]*self.scale
        self.y = pos[1]*self.scale
        self.delta_vx = 0
        self.delta_vy = 0
        self.size = size

        self.curr_animation_type = IDLE
        self.curr_sprite_show = 0
        self.curr_sprite_vector_len = 0
        self.assets = [self.sentinel_asset for n in range(NUMBER_OF_ANIMATION_TYPE)]

        self.stats = Stats()

    def add_assets(self, type, frames_speed, animation_frames, sprites_paths):
        self.assets[type] = EntityAsset(type, frames_speed, animation_frames, sprites_paths)

    def get_sprites(self):
        assets_list = []
        for asset_type in self.assets:
            if asset_type == self.sentinel_asset:
                assets_list.append(None)
            else:
                assets_list.append( [pyg.image.load(sprite) for sprite in asset_type.get_sprites_paths()] )
        
        return assets_list

    def get_current_animation_info(self):
        return [self.curr_animation_type, self.assets[self.curr_animation_type].get_animation_frames()]

    def get_current_sprite_info(self):
        return [self.curr_animation_type, self.curr_sprite_show]

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def get_ent_id(self):
        return self.ent_id

    def set_animation_type(self, type):
        self.curr_animation_type = type
        self.curr_sprite_show = 0
        self.curr_sprite_vector_len = len(self.assets[type].get_animation_frames())

    def update_sprite(self):
        self.curr_sprite_show = (self.curr_sprite_show + 1) % self.curr_sprite_vector_len

    def get_pos(self) -> tuple:
        return (self.x//self.scale, self.y//self.scale)

    def get_size(self) -> tuple:
        return self.size

    def get_center(self) -> tuple:
        return (self.x//self.scale+self.size[0], self.y//self.scale+self.size[1])

    def update_position(self, delta_t):
        # time in 'ms'
        self.x += self.delta_vx * delta_t >> 3
        self.y += self.delta_vy * delta_t >> 3
        # division by 8, a bit faster than dividing by 10

    def set_offset_speed(self, velocity):
        '''
        The velocity is equal to: 100 mpx/s
        ~> 100 millipixel/second
        '''
        self.delta_vx += velocity[0]
        self.delta_vy += velocity[1]

    def update_stats(self):
        pass

