import utilities as util
import pygame as pyg
import math

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
        self.size = (size[0]*self.scale, size[1]*self.scale)
        self.scale_factor = 1 * self.scale
        self.previous_scale_factor = self.scale_factor

        self.curr_animation_type = IDLE
        self.curr_sprite_to_show = 0
        self.curr_sprite_vector_len = 0
        self.sprite_frames_per_sec = 10
        self.time_sum_ms = 0
        self.assets = [self.sentinel_asset for n in range(NUMBER_OF_ANIMATION_TYPE)]

        self.stats = Stats()

    def get_ent_id(self):
        return self.ent_id

    def get_pos(self) -> tuple:
        return (self.x//self.scale, self.y//self.scale)

    def get_size(self) -> tuple:
        return (self.size[0]//self.scale, self.size[1]//self.scale)

    def get_center_pos(self) -> tuple:
        return ((self.x+self.size[0])//self.scale, (self.y+self.size[1])//self.scale)

    def set_scale(self, scale: float):
        # the scale factore is scaled to 100 to eliminte the float type and use int calculus
        self.previous_scale_factor = self.scale_factor
        self.scale_factor = math.floor(scale*self.scale)
        self.update_to_new_scale()

    def set_offset_speed(self, velocity):
        '''
        The velocity is equal to: 100 mpx/s
        ~> 100 millipixel/second
        '''
        self.delta_vx = math.floor(velocity[0]*self.scale_factor)
        self.delta_vy = math.floor(velocity[1]*self.scale_factor)

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
        return [self.curr_animation_type, self.curr_sprite_to_show]

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def set_animation_type(self, type):
        self.curr_animation_type = type
        self.curr_sprite_to_show = 0
        self.curr_sprite_vector_len = len(self.assets[type].get_animation_frames())

    def update_sprite_frame(self, delta_t):
        self.time_sum_ms += delta_t
        n_frames = self.time_sum_ms * self.sprite_frames_per_sec // 1000
        # time_sum_ms % [ 1000frame / (1frame/ms) ] = [ 1frame / (1frame/s) ]
        self.time_sum_ms = self.time_sum_ms % (1000 // self.sprite_frames_per_sec)
        self.curr_sprite_to_show = (self.curr_sprite_to_show + n_frames) % self.curr_sprite_vector_len

    def update_position(self, delta_t):
        # time in 'ms'
        self.x += self.delta_vx * delta_t >> 3
        self.y += self.delta_vy * delta_t >> 3
        # division by 8: faster than dividing by 10 with int division

    def update_to_new_scale(self):
        self.x = self.x * self.scale_factor // self.previous_scale_factor
        self.y = self.y * self.scale_factor // self.previous_scale_factor
        self.size = (self.size[0]*self.scale_factor//self.previous_scale_factor,
                    self.size[1]*self.scale_factor//self.previous_scale_factor)

    def update_stats(self):
        pass

