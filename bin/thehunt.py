#!/bin/python3

import curses
import json
import math
import random
from .gameboard import Board
from time import sleep

random.seed()
LEVELSFILE = 'data/levels.json'

WELCOME_SCRIPT = [ \
    "__________________Welcome to the Hunt!_____________________",
    "Your objective is to hunt and kill the pesky rabbit!       ",
    "Track the rabbit down and try to catch it. If you think you",
    "have a shot, take it! However, be careful has you have     ",
    "limited ammo to use against the rabbit. Like any good      ",
    "hunter, you'll need to sit, wait, and listen for the rabit.",
    "Good Luck!                                                 ",
    "CONTROLS:  w, a, s, d: to move around the woods            ",
    "           f: to fire your gun (if enabled)                ",
    "           <space>: to listen to the rabbit's footsteps    ",
    "                                                           ",
    "What difficulty would you like to play?                    ",
    "Levels 1-3:                                                ",
    ]

class TheHunt:
    def __init__(self):
        self.axis = [0, 0]
        self.board = None
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

    def appendHistory(self, player, move):
        self.hist[player].append({'move':move, 'loc':self.pos[player]})
        return

    def calculate(self, player, decision):
        return [self.pos[player][0] +  self.translate[decision][0], \
                self.pos[player][1] +  self.translate[decision][1]]

    def checkBoundry(self, player, decision):
        new_pos = self.calculate(player, decision)
        if 0 <= new_pos[0] and self.axis[0] > new_pos[0]:
            if 0 <= new_pos[1] and self.axis[1] > new_pos[1]:
                return new_pos
        return None

    def decisionAi(self):
        new_pos = None
        choices = {'w':0, 'a':0, 's':0, 'd':0}
        old_dist = self.distance()
        new_dist = self.distance()
        if self.distance() < self.axis[0] / 4:
            for decision in choices:
                new_pos = self.checkBoundry('ai', decision)
                if new_pos:
                    choices[decision] = self.distance(ai_pos=new_pos)
            new_pos = self.checkBoundry('ai', max(choices, key=choices.get))
        else:
            while not new_pos:
                new_pos = self.checkBoundry('ai', random.choice(list(choices)))
        self.pos['ai'] = new_pos
        self.appendHistory('ai', new_pos)
        return

    def decisionUsr(self, window):
        valid_moves = ['w', 'a', 's', 'd', ' ']
        window.addstr(1, 1, "Which direction (w, a, s, d): ")
        while True:
            decision = window.getkey(1,32)
            if decision in valid_moves:
                new_pos = self.checkBoundry('usr', decision)
                if new_pos:
                    self.pos['usr'] = new_pos
                    self.appendHistory('usr', decision)
                    break
            elif 'q' == decision:
                self.quit = True
                return
            elif 'f' == decision and self.gun_enable:
                self.fire()
                break
        return

    def distance(self, ai_pos=None, usr_pos=None):
        if None == ai_pos: ai_pos = self.pos['ai']
        if None == usr_pos: usr_pos = self.pos['usr']
        a = math.pow(ai_pos[0] - usr_pos[0], 2)
        b = math.pow(ai_pos[1] - usr_pos[1], 2)
        return math.sqrt(a + b)

    def fire(self):
        return

    def placePlayers(self):
        while self.distance() < (self.axis[0] / 3):
            self.pos['ai'] = [random.randint(0, self.axis[0] - 1),
                              random.randint(0, self.axis[1] - 1)]
            self.pos['usr'] = [random.randint(0, self.axis[0] - 1),
                               random.randint(0, self.axis[1] - 1)]
        self.appendHistory('ai', ' ')
        self.appendHistory('usr', ' ')
        return

    def run(self):
        win_usr = self.window.subwin(8, 40, 1, 1)
        win_board = self.window.subwin(self.axis[0] + 2, (self.axis[1] + 2) * 2, 1, 60)
        win_usr.border()
        victory = False

        while not self.quit:
            if self.board_print:
                self.board.printGrid(self.pos, win_board)
            self.decisionAi()
            self.window.addstr(20, 1, "{}".format(self.pos))
            self.window.refresh()
            self.decisionUsr(win_usr)
            if self.pos['ai'] == self.pos['usr']:
                self.quit = True
                victory = True
        if victory:
            win_vic = self.window.subwin(10, 40, 2, 4)
            win_vic.erase()
            win_vic.border()
            self.victory(win_vic)
        return

    def start(self, winscr):
        curses.curs_set(2)
        self.window = winscr
        start_win = self.window.subwin(15, 63, 1, 1)

        index = 1
        for line in WELCOME_SCRIPT:
            start_win.addstr(index, 2, line)
            index += 1
        start_win.border()

        valid = ['1', '2', '3', 'q']
        while True:
            level = start_win.getkey(13, 14)
            if level in valid:
                if level == 'q':
                    return
                break
            else:
                start_win.addstr(13, 18, "Invalid option {:2}".format(level))
                start_win.move(13, 14)
                start_win.refresh()

        with open(LEVELSFILE) as lvls:
            settings = json.load(lvls)
            settings = settings['levels'][int(level) - 1]

        self.axis = settings['axis']
        self.board_print = settings['board_print']
        self.gun_enable = settings['gun_enable']
        self.gun_ammo = settings['gun_ammo']
        self.gun_prob = settings['gun_prob']
        self.gun_range = settings['gun_range']

        start_win.addstr(13, 14, "{} Let the Hunt begin!".format(level))
        start_win.refresh()
        sleep(1)
        start_win.erase()
        start_win.refresh()
        self.board = Board(self.axis)
        self.placePlayers()
        self.run()

    def victory(self, window):
        curses.curs_set(0)
        window.addstr(4,10, "You caught the Rabbit!")
        window.refresh()
        sleep(1)
        window.addstr(5,10, "Press any key to exit.")
        window.getkey(4,2)
        return
