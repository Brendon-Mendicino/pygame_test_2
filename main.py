#!/bin/python3

import time
import threading as th
import pygame as pyg
import utilities as uts
import entities as ent


class Handler:
    def __init__(self):
        pass

    def game_events(self, event: pyg.event.Event):
        if event.type == pyg.QUIT:
            loop = False
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                loop = False
            else:
                pp.set_offset_speed(event_key_case_down[event.key])

        if event.type == pyg.KEYUP:
            pp.set_offset_speed(event_key_case_up[event.key])


def main():
    pyg.init()

    screen = uts.Screen()
    screen.set_area(uts.Area('./areas/01area.txt'))

    pp = ent.Player(0, (240, 150))
    pp.set_animation_type(ent.IDLE)
    screen.add_entity( pp)

    clock = pyg.time.Clock()
    FPS = 60
    loop = True

    vel = 0.4
    event_key_case_down = {
            pyg.K_DOWN: (0, vel),
            pyg.K_UP: (0, -vel),
            pyg.K_RIGHT: (vel, 0),
            pyg.K_LEFT: (-vel, 0),
            }
    event_key_case_up = {
            pyg.K_DOWN: (0, -vel),
            pyg.K_UP: (0, vel),
            pyg.K_RIGHT: (-vel, 0),
            pyg.K_LEFT: (vel, 0),
            }

    delta_t = 0
    while loop:
        # time in 'ms'
        delta_t = clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                loop = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    loop = False
                else:
                    pp.set_offset_speed(event_key_case_down[event.key])

            if event.type == pyg.KEYUP:
                pp.set_offset_speed(event_key_case_up[event.key])

        pp.update_sprite_frame(delta_t)
        pp.update_position(delta_t)

        screen.update_entities_to_draw()
        screen.update_display_position(pp.get_center_pos())
        screen.draw()

    pyg.quit()



if __name__=="__main__":
    main()

