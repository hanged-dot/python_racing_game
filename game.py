import pygame
import pygame as pg
from math import pi
from cars.car import Car
from cars.automatedcar import AutomatedCar
from map.road import Road
from map.background import Background
import config
from display import Display
import csv
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider


class Game:
    def __init__(self):

        pg.init()
        pg.mixer.init()
        pg.display.set_caption('Racing Game')
        self.clock = pg.time.Clock()
        self.begin = True
        self.crash = False
        self.pause = False
        self.display = Display(config.display_width, config.display_height, config.music_volume, config.sound_volume)
        self.background = Background(self.display)
        self.road = None
        self.player_car = None
        self.opponent_car = None
        '''opponent_car = Car(road,display)
        
        road.check_boundaries(opponent_car)
        road.check_for_checkpoints(opponent_car)
        opponent_moves = opponent_car.calc_route(road)'''

        file = open('statistics/stats.csv', mode='a', newline='')
        self.writer = csv.writer(file)

    def homescreen(self):
        new_surface = pg.surface.Surface((self.display.width, self.display.height), pg.SRCALPHA)
        start_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (1 / 3),
                              width=self.display.width * (3 / 10), height=self.display.height * (1 / 20),
                              text='Start Game', radius=20, colour=(255, 0, 0), onClick=self.race,
                              font=pg.font.Font('freesansbold.ttf', 20))
        quit_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (2 / 3),
                             width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                             text='Quit', radius=20, colour=(255, 0, 0), onClick=self.quit_game,
                             font=pg.font.Font('freesansbold.ttf', 20))

        while self.begin:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == pg.WINDOWSIZECHANGED:
                    self.window_changed(event.x, event.y)
                    new_surface = pg.surface.Surface((self.display.width, self.display.height), pg.SRCALPHA)
                    start_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (1 / 3),
                                          width=self.display.width * (3 / 10), height=self.display.height * (1 / 20),
                                          text='Start Game', radius=20, colour=(255, 0, 0), onClick=self.race,
                                          font=pg.font.Font('freesansbold.ttf', 20))
                    quit_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (2 / 3),
                                         width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                                         text='Quit', radius=20, colour=(255, 0, 0), onClick=self.quit_game,
                                         font=pg.font.Font('freesansbold.ttf', 20))

            self.background.draw()
            self.display.display.blit(new_surface, (0, 0))
            pygame_widgets.update(events)
            pg.display.update()
            self.clock.tick(15)

    def run(self):
        self.homescreen()

    def race(self):
        self.begin = False
        self.road = Road(config.road_length, config.road_width, config.max_speed, config.zoom, self.display)
        self.player_car = Car(self.road, self.display)
        self.opponent_car = AutomatedCar(self.road, self.display)
        i = 0
        while not self.crash:
            i += 1
            for event in pg.event.get():
                #if event.type != pg.MOUSEMOTION: print(event)  # writes in terminal everything that user does in the window
                if event.type == pg.QUIT:
                    self.crash = True
                    # we can choose if we want to close the window or send a message here before closing
                if event.type == pg.WINDOWSIZECHANGED:
                    self.window_changed(event.x, event.y)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pg.mixer.Sound("images/automobile-horn-153260.mp3").play()
                    if event.key == pg.K_UP or event.key == pg.K_DOWN:
                        self.player_car.engine_sound.play()
                    if event.key == pg.K_p:
                        self.window_changed(self.display.width, self.display.height)
                        self.paused()

            keys = pg.key.get_pressed()  # we need to move on this because we need both keys pressed to move
            self.player_car.update(keys)
            self.road.check_boundaries(self.player_car)
            self.road.check_for_checkpoints(self.player_car)

            if self.opponent_car._AutomatedCar__velocity < 2.0:
                self.opponent_car.update(True)
            else:
                self.opponent_car.update(False)
            self.road.check_boundaries(self.opponent_car)
            self.road.check_for_checkpoints(self.opponent_car)

            self.update_drawing()
            self.update_stats_display()
            self.writer.writerow([self.player_car.get_velocity(), self.player_car.get_dist_to_goal()])

            pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D

            if self.player_car.finish_line(): self.endscreen()
            # print(f'Nodes so far: {done}/{all}')
            self.clock.tick(60)  # the faster, the more you need here
        pg.quit()
        quit()


    def update_stats_display(self):
        circle_center=(0,0)
        radius=int(self.display.height * (1 / 7))
        statistics_surface = pg.Surface((self.display.width, self.display.height), pg.SRCALPHA)
        pg.draw.arc(statistics_surface, (128, 128, 128, 128), (circle_center[0] - radius, circle_center[1] - radius, 2 * radius, 2 * radius), 0, pi/2, 5)
        pygame.draw.line(statistics_surface, (128, 128, 128, 128), circle_center, (circle_center[0] + radius, circle_center[1]),5)
        pygame.draw.line(statistics_surface, (128, 128, 128, 128), circle_center, (circle_center[0], circle_center[1] + radius),5)
        font = pg.font.Font('freesansbold.ttf', self.display.height // 25)
        text1 = font.render('Velocity: %.0f' % (self.player_car.get_velocity() * 100), True, (255, 165, 0))
        text2 = font.render('Distance left: %.0f' % (self.player_car.get_dist_to_goal()), True, (255, 165, 0))
        text1_rect = text1.get_rect(center=(circle_center[0] + radius / 2, circle_center[1] + radius / 4))
        text2_rect = text2.get_rect(center=(circle_center[0] + radius / 2, circle_center[1] + 3 * radius / 4))
        statistics_surface.blit(text1, text1_rect)
        statistics_surface.blit(text2, text2_rect)

        self.display.display.blit(statistics_surface, (0,0))
        pg.display.update()

    def update_drawing(self):
        self.background.draw()
        self.road.draw(self.player_car.get_position())
        self.player_car.draw(self.player_car.get_position())
        self.opponent_car.draw(self.player_car.get_position())

    def window_changed(self, x, y):
        self.display.update_display(x, y)
        self.road.update_surface()
        self.update_drawing()

    def unpaused(self):
        self.pause = False

    def paused(self):
        self.pause = True
        p_but, q_but, r_but, n_but, vol, rect = self.pause_buttons()

        while self.pause:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == pg.WINDOWSIZECHANGED:
                    self.window_changed(event.x, event.y)
                    p_but, q_but, r_but, n_but, vol, rect = self.pause_buttons()
                if event.type == pg.KEYDOWN and (event.key == pg.K_p or event.key == pg.K_ESCAPE):
                    self.unpaused()
            self.update_drawing()
            self.display.display.blit(rect, (0, 0))
            pg.mixer.music.set_volume(vol.getValue())
            pygame_widgets.update(events)
            pg.display.update()
            self.clock.tick(15)

    def pause_buttons(self):
        self.update_drawing()
        rect = pg.Surface((self.display.width, self.display.height), pg.SRCALPHA)
        rect.fill((128, 128, 128, 128))
        self.display.display.blit(rect, (0, 0))
        volume_slider = Slider(self.display.display, int(self.display.width * (1 / 4)),
                               int(self.display.height * (1 / 3)), width=self.display.width // 2,
                               height=self.display.height // 20, min=0, max=1, step=0.1, curved=True,
                               initial=pg.mixer.music.get_volume())
        pause_button = Button(self.display.display, self.display.width * (2 / 3), self.display.height * (2 / 3),
                              width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                              text='Resume', radius=20, colour=(0, 0, 255), onClick=self.unpaused,
                              font=pg.font.Font('freesansbold.ttf', 20))
        quit_game_button = Button(self.display.display, self.display.width * (1 / 3), self.display.height * (2 / 3),
                                  width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                                  text='Quit', radius=20, colour=(255, 0, 0), onClick=self.homescreen,
                                  font=pg.font.Font('freesansbold.ttf', 20))
        restart_button = Button(self.display.display, self.display.width * (1 / 3), int(self.display.height * (4 / 5)),
                                width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                                text='Restart', radius=20, colour=(0, 255, 0), onClick=self.restart_game,
                                font=pg.font.Font('freesansbold.ttf', 20))
        new_game_button = Button(self.display.display, self.display.width * (2 / 3), int(self.display.height * (4 / 5)),
                                 width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                                 text='New Game', radius=20, colour=(0, 255, 0), onClick=self.race,
                                 font=pg.font.Font('freesansbold.ttf', 20))
        return pause_button, quit_game_button, restart_button, new_game_button, volume_slider, rect

    def quit_game(self):
        self.begin = False
        self.crash = True
        pg.quit()
        quit()

    def restart_game(self):
        self.player_car.restart()
        self.opponent_car.restart()

    def endscreen(self):
        self.pause = True
        self.begin = True
        font = pg.font.Font('freesansbold.ttf', self.display.height // 15)
        text = font.render('You WIN', True, (0, 255, 0), (0, 0, 0, 0))
        if self.opponent_car.finish_line():
            text = font.render('You LOSE', True, (255, 0, 0), (0, 0, 0, 0))
        new_surface = pg.surface.Surface((self.display.width, self.display.height), pg.SRCALPHA)
        start_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (1 / 3),
                                  width=self.display.width * (3 / 10), height=self.display.height * (1 / 20),
                                  text='Start Game', radius=20, colour=(255, 0, 0), onClick=self.race,
                                  font=pg.font.Font('freesansbold.ttf', 20))
        quit_game_button = Button(new_surface, self.display.width * (1 / 3), self.display.height * (2 / 3),
                                  width=self.display.width * (1.5 / 10), height=self.display.height * (1 / 20),
                                  text='Quit', radius=20, colour=(255, 0, 0), onClick=self.homescreen,
                                  font=pg.font.Font('freesansbold.ttf', 20))
        while self.pause:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == pg.WINDOWSIZECHANGED:
                    self.window_changed(event.x, event.y)
                    new_surface = pg.surface.Surface((self.display.width, self.display.height), pg.SRCALPHA)
                    start_button = Button(new_surface, self.display.width * (1 / 2), self.display.height * (1 / 3),
                                          width=self.display.width * (3 / 10), height=self.display.height * (1 / 20),
                                          text='Start Game', radius=20, colour=(255, 0, 0), onClick=self.race,
                                          font=pg.font.Font('freesansbold.ttf', 20))
                    quit_game_button = Button(self.display.display, self.display.width * (1 / 3),
                                              self.display.height * (2 / 3),
                                              width=self.display.width * (1.5 / 10),
                                              height=self.display.height * (1 / 20),
                                              text='Quit', radius=20, colour=(255, 0, 0), onClick=self.homescreen,
                                              font=pg.font.Font('freesansbold.ttf', 20))

            self.background.draw()
            new_surface.blit(text, (int(self.display.width / 4), int(self.display.height / 4)))
            pygame_widgets.update(events)
            pg.display.update()
            self.clock.tick(15)
