#!/bin/python3

import curses
import json
import math
import random
from time import sleep

random.seed()
LEVELSFILE = 'data/levels.json'


class TheHunt:
    def __init__(self):
        self.axis = [0, 0]
        self.grid = False
        self.gun_enable = False
        self.gun_ammo = None
        self.gun_prob = None
        self.hist = {'ai':[], 'usr':[]}
        self.pos = {'ai':[0, 0], 'usr':[0, 0]}
        self.quit = False
        self.window = None

        self.translate = {
            'w':[-1,  0],
            'a':[ 0, -1],
            's':[ 1,  0],
            'd':[ 0,  1],
            ' ':[ 0,  0]
        }

    def action(self, player, direction):
        return {'move':direction, 'loc':self.pos[player]}

    def appendHistory(self, player, move):
        self.hist[player].append({'move':move, 'loc':self.pos[player]})
        return

    def calculate(self, player, decision):
        return [self.pos[player][0] +  self.translate[decision][0], \
                self.pos[player][1] +  self.translate[decision][1]]

    def checkBoundry(self, player, decision):
        new_pos = self.calculate(player, decision)
        if 0 < new_pos[0] and self.axis[0] > new_pos[0]:
            if 0 < new_pos[1] and self.axis[1] > new_pos[1]:
                return new_pos
        return False

    def decisionAi(self):
        new_pos = None
        choices = {'w':0, 'a':0, 's':0, 'd':0}
        old_dist = self.distance()
        new_dist = self.distance()
        for decision in choices:
            new_pos = self.checkBoundry('ai', decision)
            if new_pos:
                choices[decision] = self.distance(ai_pos=new_pos)
        new_pos = self.checkBoundry('ai', max(choices, key=choices.get))
        self.pos['ai'] = new_pos
        self.appendHistory('ai', new_pos)
        return

    def decisionUsr(self, window):
        window.addstr(1, 1, "Which direction (w, a, s, d): ")
        decision = window.getkey(1,32)
        return

    def distance(self, ai_pos=None, usr_pos=None):
        if None == ai_pos: ai_pos = self.pos['ai']
        if None == usr_pos: usr_pos = self.pos['usr']
        a = math.pow(ai_pos[0] - usr_pos[0], 2)
        b = math.pow(ai_pos[1] - usr_pos[1], 2)
        return math.sqrt(a + b)

    def placePlayers(self):
        while self.distance() < (self.axis[0] / 3):
            self.pos['ai'] = [random.randint(0, self.axis[0]), random.randint(0, self.axis[1])]
            self.pos['usr'] = [random.randint(0, self.axis[0]), random.randint(0, self.axis[1])]
        self.appendHistory('ai', ' ')
        self.appendHistory('usr', ' ')
        return

    def run(self):
        usr_win = self.window.subwin(8, 50, 1, 1)
        while not self.quit:
            self.decisionAi()
            self.decisionUsr(usr_win)
            self.window.addstr(20, 1, "{}".format(self.pos))
            self.window.refresh()
        return

    def start(self, winscr):
        curses.curs_set(2)
        self.window = winscr
        start_win = self.window.subwin(15, 63, 1, 1)
        start_win.addstr(1, 2,  "__________________Welcome to the Hunt!_____________________")
        start_win.addstr(2, 2,  "Your objective is to hunt and kill the pesky rabbit!       ")
        start_win.addstr(3, 2,  "Track the rabbit down and try to catch it. If you think you")
        start_win.addstr(4, 2,  "have a shot, take it! However, be careful has you have     ")
        start_win.addstr(5, 2,  "limited ammo to use against the rabbit. Like any good      ")
        start_win.addstr(6, 2,  "hunter, you'll need to sit, wait, and listen for the rabit.")
        start_win.addstr(7, 2,  "Good Luck!                                                 ")
        start_win.addstr(8, 2,  "CONTROLS:  w, a, s, d: to move around the woods            ")
        start_win.addstr(9, 2,  "           f: to fire your gun (if enabled)                ")
        start_win.addstr(10, 2, "           <space>: to listen to the rabbit's footsteps    ")

        start_win.addstr(12, 2, "What difficulty would you like to play?                    ")
        start_win.addstr(13, 2, "Levels 1-3:                                                ")
        start_win.border()

        valid = ['1', '2', '3', 'q']
        while True:
            level = start_win.getkey(13, 14)
            if level in valid:
                break
            else:
                start_win.addstr(13, 18, "Invalid option {:2}".format(level))
                start_win.move(13, 14)
                start_win.refresh()

        if level == 'q':
            return

        with open(LEVELSFILE) as lvls:
            settings = json.load(lvls)
            settings = settings['levels'][int(level) - 1]
        
        self.axis = settings['axis']
        self.grid = settings['grid']
        self.gun_enable = settings['gun_enable']
        self.gun_ammo = settings['gun_ammo']
        self.gun_prob = settings['gun_prob']
        self.gun_range = settings['gun_range']

        start_win.addstr(13, 14, "{} Let the Hunt begin!".format(level))
        start_win.refresh()
        sleep(1)
        start_win.erase()
        start_win.refresh()
        self.placePlayers()
        self.run()
