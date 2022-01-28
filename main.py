#!/bin/python3
#!/bin/python3

import time
import threading as th
import pygame as pyg
import utilities as uts



def main():
    pyg.init()

    screen = uts.Screen()
    screen.set_area(uts.Area('./areas/01area.txt'))

    clock = pyg.time.Clock()
    FPS = 10
    loop = True

    while loop:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                loop = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    loop = False

        screen.draw()

    pyg.quit()



if __name__=="__main__":
    main()
