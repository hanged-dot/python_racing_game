from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
import pygame as pg
import csv


class ButtonManager:
    def __init__(self, parent):
        self.parent = parent
        self.spawn_buttons()
        self.show_homescreen()

    def spawn_buttons(self):
        self.font = pg.font.Font('freesansbold.ttf', self.get_display_height() // 15)

        self.begin_text = self.font.render("Radiator Springs Adventure", True, (0, 0, 0, 255))

        self.begin_start_button = Button(self.get_display(), self.get_display_width() * (1 / 3),
                                         self.get_display_height() * (1 / 2),
                                         width=self.get_display_width() * (3 / 10),
                                         height=self.get_display_height() * (1 / 20),
                                         text='Start Game', radius=20, colour=(255, 0, 0),
                                         onClick=self.parent.init_race,
                                         font=pg.font.Font('freesansbold.ttf', 20))
        self.begin_end_button = Button(self.get_display(), self.get_display_width() * (1 / 3),
                                       self.get_display_height() * (3 / 4),
                                       width=self.get_display_width() * (1.5 / 10),
                                       height=self.get_display_height() * (1 / 20),
                                       text='Quit', radius=20, colour=(255, 0, 0), onClick=self.parent.quit_game,
                                       font=pg.font.Font('freesansbold.ttf', 20))

        self.rect = pg.Surface((self.get_display_width(), self.get_display_height()), pg.SRCALPHA)
        self.rect.fill((128, 128, 128, 128))

        self.pause_volume_slider = Slider(self.get_display(), int(self.get_display_width() * (1 / 4)),
                                          int(self.get_display_height() * (2 / 5)), width=self.get_display_width() // 2,
                                          height=self.get_display_height() // 20, min=0, max=1, step=0.1, curved=True,
                                          initial=pg.mixer.music.get_volume())
        self.pause_unpause_button = Button(self.get_display(), int(self.get_display_width() * (2 / 3)),
                                           int(self.get_display_height() * (3 / 5)),
                                           width=self.get_display_width() * (1.5 / 10),
                                           height=self.get_display_height() * (1 / 20),
                                           text='Resume', radius=20, colour=(0, 0, 255), onClick=self.parent.unpaused,
                                           font=pg.font.Font('freesansbold.ttf', 20))
        self.pause_quit_game_button = Button(self.get_display(), int(self.get_display_width() * (1 / 4)),
                                             self.get_display_height() * (3 / 5),
                                             width=self.get_display_width() * (1.5 / 10),
                                             height=self.get_display_height() * (1 / 20),
                                             text='Quit', radius=20, colour=(255, 0, 0),
                                             onClick=self.parent.init_homescreen,
                                             font=pg.font.Font('freesansbold.ttf', 20))
        self.pause_restart_button = Button(self.get_display(), self.get_display_width() * (1 / 4),
                                           int(self.get_display_height() * (4 / 5)),
                                           width=self.get_display_width() * (1.5 / 10),
                                           height=self.get_display_height() * (1 / 20),
                                           text='Restart', radius=20, colour=(0, 255, 0),
                                           onClick=self.parent.restart_race,
                                           font=pg.font.Font('freesansbold.ttf', 20))
        self.pause_new_game_button = Button(self.get_display(), self.get_display_width() * (2 / 3),
                                            int(self.get_display_height() * (4 / 5)),
                                            width=int(self.get_display_width() * (2 / 10)),
                                            height=self.get_display_height() * (1 / 20),
                                            text='New Game', radius=20, colour=(0, 255, 0),
                                            onClick=self.parent.init_race,
                                            font=pg.font.Font('freesansbold.ttf', 20))

        self.pause_statistics_text_value = ""

        self.endgame_start_button = Button(self.get_display(), self.get_display_width() * (1 / 3),
                                           self.get_display_height() * (1 / 2),
                                           width=self.get_display_width() * (3 / 10),
                                           height=self.get_display_height() * (1 / 20),
                                           text='Start Game', radius=20, colour=(255, 0, 0),
                                           onClick=self.parent.init_race,
                                           font=pg.font.Font('freesansbold.ttf', 20))
        self.endgame_quit_game_button = Button(self.get_display(), self.get_display_width() * (1 / 3),
                                               self.get_display_height() * (3 / 4),
                                               width=self.get_display_width() * (1.5 / 10),
                                               height=self.get_display_height() * (1 / 20),
                                               text='Quit', radius=20, colour=(255, 0, 0),
                                               onClick=self.parent.init_homescreen,
                                               font=pg.font.Font('freesansbold.ttf', 20))

        self.hide_all()

    def show_homescreen(self):
        self.hide_all()
        self.begin_text = self.font.render("Radiator Springs Adventure", True, (0, 0, 0, 255))
        self.begin_start_button.show()
        self.begin_end_button.show()

    def show_pause(self):
        self.hide_all()

        self.rect.fill((128, 128, 128, 128))
        self.pause_volume_slider.show()
        self.pause_unpause_button.show()
        self.pause_quit_game_button.show()
        self.pause_restart_button.show()
        self.pause_new_game_button.show()

        self.pause_statistics_text = self.font.render(self.pause_statistics_text_value, True, (255, 0, 0, 255),
                                                      (128, 128, 128, 128))

    def show_endgame(self):
        self.hide_all()

        file = open('statistics/stats.csv', mode='a', newline='')
        writer = csv.writer(file)

        self.endgame_start_button.show()
        self.endgame_quit_game_button.show()

        if self.parent.opponent_car.finish_line():
            self.endgame_text = self.font.render('You LOSE', True, (255, 0, 0, 255), (128, 128, 128, 128))
            writer.writerow([0, self.parent.player_car.get_avg_velocity()])
        else:
            self.endgame_text = self.font.render('You WIN', True, (0, 255, 0, 255), (128, 128, 128, 128))
            writer.writerow([1, self.parent.player_car.get_avg_velocity()])

    def hide_all(self):
        self.begin_start_button.hide()
        self.begin_end_button.hide()
        self.rect.fill((128, 128, 128, 0))
        self.pause_volume_slider.hide()
        self.pause_unpause_button.hide()
        self.pause_quit_game_button.hide()
        self.pause_restart_button.hide()
        self.pause_new_game_button.hide()
        self.endgame_start_button.hide()
        self.endgame_quit_game_button.hide()

        self.endgame_text = self.font.render('', True, (255, 0, 0, 0))
        self.pause_statistics_text = self.font.render('', True, (255, 0, 0, 0))
        self.begin_text = self.font.render('', True, (255, 0, 0, 0))

    def get_display_width(self):
        return self.parent.display.width

    def get_display_height(self):
        return self.parent.display.height

    def get_display(self):
        return self.parent.display.display

    def getVolumeValue(self):
        return self.pause_volume_slider.getValue()

    def setPauseStatisticsText(self, text):
        self.pause_statistics_text_value = text
        self.pause_statistics_text = self.font.render(self.pause_statistics_text_value, True, (255, 165, 0),
                                                      (128, 128, 128, 128))
