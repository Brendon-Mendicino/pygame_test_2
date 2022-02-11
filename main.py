#!/bin/python3

import time
import threading as th
import pygame as pyg
import utilities as uts
import entities as ent



class Game:

    loop = True

    # TODO: temp
    k_set = { pyg.K_DOWN, pyg.K_UP, pyg.K_RIGHT, pyg.K_LEFT, }

    def __init__(self):
        pyg.init()

        self.screen = uts.Screen()
        self.area = uts.Area('./areas/01area.txt')
        # TODO: for testing
        self.area.set_scale(self.screen.find_scale_factor())
        #####################
        self.screen.set_area(self.area)
        
        self.player = ent.Player(0, (240, 150))
        self.player.set_animation_type(ent.IDLE)
        self.screen.add_entity(self.player)

        self.clock = pyg.time.Clock()
        self.FPS = 60


    def run(self):
        delta_t = 0
        while self.loop:
            delta_t = self.clock.tick(self.FPS)

            for event in pyg.event.get():
                self.game_events(event)

            self.player.update_sprite_frame(delta_t)
            self.player.update_position(delta_t)
            # TODO: for testing
            print(self.area.check_collision(self.player))
            #####################

            self.screen.update_entities_to_draw()
            self.screen.update_display_position(self.player.get_center_pos())
            self.screen.draw()

        pyg.quit()


    def game_events(self, event: pyg.event.Event):
        if event.type == pyg.QUIT:
            self.loop = False
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                self.loop = False
            elif event.key == pyg.K_0:
                self.screen.set_window_resolution(0)
            elif event.key == pyg.K_1:
                self.screen.set_window_resolution(1)
            elif event.key == pyg.K_2:
                self.screen.set_window_resolution(2)

            elif self.k_set.issuperset([event.key]):
                self.player.set_input_direction(event.key)

        if event.type == pyg.KEYUP:
            if self.k_set.issuperset([event.key]):
                self.player.set_input_direction(event.key)


if __name__=="__main__":
    game = Game()
    game.run()

