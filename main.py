import pygame as pyg
import utilities as uts


def main():
    pyg.init()

    screen = uts.Screen()
    screen.set_area(uts.Area('./areas/01area.txt'))

    loop = True
    while loop:
        screen.draw()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                loop = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    loop = False

    pyg.quit()



if __name__=="__main__":
    main()
