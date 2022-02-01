#!/bin/python3

import time
import threading as th
import pygame as pyg
import utilities as uts
import entities as ent



def main():
    pyg.init()

    screen = uts.Screen()
    screen.set_area(uts.Area('./areas/01area.txt'))

    pp = ent.Player(0, (150, 150))
    pp.set_animation_type(ent.IDLE)
    screen.add_entity( pp)

    clock = pyg.time.Clock()
    FPS = 60
    loop = True

    event_key_case_down = {
            pyg.K_DOWN: (0, 1),
            pyg.K_UP: (0, -1),
            pyg.K_RIGHT: (1, 0),
            pyg.K_LEFT: (-1, 0),
            }
    event_key_case_up = {
            pyg.K_DOWN: (0, -1),
            pyg.K_UP: (0, 1),
            pyg.K_RIGHT: (-1, 0),
            pyg.K_LEFT: (1, 0),
            }

    while loop:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                loop = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    loop = False
                else:
                    screen.display_offset_speed( event_key_case_down[event.key])

            if event.type == pyg.KEYUP:
                screen.display_offset_speed(event_key_case_up[event.key])

        pp.update_sprite()
        screen.draw()

    pyg.quit()



if __name__=="__main__":
    main()
