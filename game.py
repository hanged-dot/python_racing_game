import pygame
import pygame as pg
import numpy as np
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
from button_manager import ButtonManager
from enum import Enum


class GameState(Enum):
    HOMESCREEN = 0,
    RACE = 1,
    PAUSE = 2,
    ENDGAME = 3,


class Game:
    def __init__(self):

        pg.init()
        pg.mixer.init()
        pg.display.set_caption('Racing Game')
        self.clock = pg.time.Clock()
        self.game_state = GameState.HOMESCREEN
        self.display = Display(config.display_width, config.display_height, config.music_volume, config.sound_volume)
        self.background = Background(self.display)
        self.road = None
        self.player_car = None
        self.opponent_car = None

        self.button_manager = ButtonManager(self)

    def run(self):
        while True:
            match self.game_state:
                case GameState.HOMESCREEN:
                    self.homescreen()

                case GameState.RACE:
                    self.race()

                case GameState.PAUSE:
                    self.paused()

                case GameState.ENDGAME:
                    self.endscreen()

            self.clock.tick(60)  # the faster, the more you need here

    def init_homescreen(self):
        self.game_state = GameState.HOMESCREEN
        self.background.draw()
        self.button_manager.show_homescreen()

    def homescreen(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.WINDOWSIZECHANGED:
                self.display.update_display(event.x, event.y)
                self.button_manager.spawn_buttons()
                self.button_manager.show_homescreen()

        self.background.draw()
        self.display.display.blit(self.button_manager.begin_text,
                                  (int(self.display.width / 13), int(self.display.height / 4)))
        pygame_widgets.update(events)
        pg.display.update()

    def init_race(self):
        self.games_won()
        self.game_state = GameState.RACE
        self.button_manager.hide_all()

        self.road = Road(config.road_length, config.road_width, config.max_speed, config.zoom, self.display)
        self.player_car = Car(self.road, self.display)
        self.opponent_car = AutomatedCar(self.road, self.display)
        self.opponent_car.set_base_velocity(self.avg_vel / self.total_games)

    def race(self):
        for event in pg.event.get():
            #if event.type != pg.MOUSEMOTION: print(event)  # writes in terminal everything that user does in the window
            if event.type == pg.QUIT:
                self.quit_game()
                return
            if event.type == pg.WINDOWSIZECHANGED:
                self.window_changed(event.x, event.y)
                self.button_manager.spawn_buttons()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pg.mixer.Sound("images/automobile-horn-153260.mp3").play()
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    self.player_car.engine_sound.play()
                if event.key == pg.K_p:
                    self.window_changed(self.display.width, self.display.height)
                    self.init_pause()

        keys = pg.key.get_pressed()  # we need to move on this because we need both keys pressed to move
        self.player_car.update(keys)
        self.road.check_boundaries(self.player_car)
        self.road.check_for_checkpoints(self.player_car)

        self.opponent_car.update()
        self.road.check_boundaries(self.opponent_car)
        self.road.check_for_checkpoints(self.opponent_car)

        self.update_drawing()
        self.update_stats_display()

        pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D

        if self.player_car.finish_line():
            self.init_endscreen()

    def games_won(self):
        self.total_games = 0
        self.games_won_ = 0
        self.avg_vel = 0

        with open('statistics/stats.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            for row in csv_reader:
                self.total_games += 1
                self.games_won_ += int(row[0])
                self.avg_vel += float(row[1])

    def update_stats_display(self):
        statistics_surface = pg.Surface((self.display.width // 2.8, self.display.height // 4), pg.SRCALPHA)
        statistics_surface.fill((128, 128, 128, 128))

        font = pg.font.Font('freesansbold.ttf', self.display.height // 30)
        text1 = font.render('Velocity: %.0f' % (self.player_car.get_velocity() * 100), True, (255, 165, 0))
        text2 = font.render('Distance left: %.0f' % (self.player_car.get_dist_to_goal()), True, (255, 165, 0))
        text3 = font.render('Avg. velocity: %.0f' % (self.player_car.get_avg_velocity() * 100), True, (255, 165, 0))
        text4 = font.render('Games won: %d/%d' % (self.games_won_, self.total_games), True, (255, 165, 0))
        text5 = font.render('Typical velocity: %.0f' % (self.avg_vel * 100 / self.total_games), True, (255, 165, 0))
        text1_rect = text1.get_rect(left=0, top=0)
        text2_rect = text2.get_rect(left=0, top=self.display.height // 10)
        text3_rect = text3.get_rect(left=0, top=self.display.height // 20)
        text4_rect = text2.get_rect(left=0, top=self.display.height // 6.5)
        text5_rect = text3.get_rect(left=0, top=self.display.height // 5)
        statistics_surface.blit(text1, text1_rect)
        statistics_surface.blit(text2, text2_rect)
        statistics_surface.blit(text3, text3_rect)
        statistics_surface.blit(text4, text4_rect)
        statistics_surface.blit(text5, text5_rect)

        self.display.display.blit(statistics_surface, (0, 0))
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

    def init_pause(self):
        self.game_state = GameState.PAUSE
        self.button_manager.set_pause_statistics_text(
            "Distance left: %.0f  Avg. velocity: %.0f  Games won: %d/%d  Typical velocity: %.0f"
            % (self.player_car.get_dist_to_goal(), self.player_car.get_avg_velocity() * 100,
               self.games_won_, self.total_games, self.avg_vel * 100 / self.total_games))
        self.button_manager.show_pause()

    def paused(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.WINDOWSIZECHANGED:
                self.window_changed(event.x, event.y)
                self.button_manager.spawn_buttons()
                self.init_pause()
            if event.type == pg.KEYDOWN and (event.key == pg.K_p or event.key == pg.K_ESCAPE):
                self.unpaused()
        self.update_drawing()
        self.display.display.blit(self.button_manager.rect, (0, 0))
        self.display.display.blit(self.button_manager.pause_statistics_text,
                                  (int(self.display.width // 40), int(self.display.height / 5)))
        pg.mixer.music.set_volume(self.button_manager.getVolumeValue())
        pygame_widgets.update(events)
        pg.display.flip()

    def restart_race(self):
        self.player_car.restart()
        self.opponent_car.restart()

    def unpaused(self):
        self.game_state = GameState.RACE

    def init_endscreen(self):
        self.game_state = GameState.ENDGAME
        self.button_manager.show_endgame()

    def endscreen(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.WINDOWSIZECHANGED:
                self.window_changed(event.x, event.y)
                self.button_manager.spawn_buttons()
                self.button_manager.show_endgame()

        self.background.draw()
        self.display.display.blit(self.button_manager.endgame_text,
                                  (int(self.display.width / 3), int(self.display.height / 4)))
        pygame_widgets.update(events)
        pg.display.update()

    def quit_game(self):
        pg.quit()
        quit()
