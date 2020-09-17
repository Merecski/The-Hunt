#!/bin/python3

from time import sleep

import curses

class TheHunt:
    def __init__(self):
        self.hist = {'ai':[], 'usr':[]}
        self.pos = {'ai':[0, 0], 'usr':[0, 0]}
        self.win = None

    def action(self, player, direction):
        return {'move':direction, 'loc':self.pos[player]}

    def start(self):
        self.win = curses.initscr()
        start_win = self.win.subwin(15, 63, 1, 1)
        start_win.addstr(1, 2,  "__________________Welcome to the Hunt!_____________________")
        start_win.addstr(2, 2,  "Your objective is to hunt and kill the pesky rabbit!       ")
        start_win.addstr(3, 2,  "Track the rabbit down and try to catch it. If you think you")
        start_win.addstr(4, 2,  "have a shot, take it! However, be careful has you have     ")
        start_win.addstr(5, 2,  "limited ammo to use against the rabbit. Like any good      ")
        start_win.addstr(6, 2,  "hunter, you'll need to sit, wait, and listen for the rabit.")
        start_win.addstr(7, 2,  "Good Luck!                                                 ")
        start_win.addstr(8, 2,  "CONTROLS:  w, a, s, d: to move around the woods            ")
        start_win.addstr(9, 2,  "           f: to fire your gun (limited ammo!)             ")
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
                sleep(0.2)
                start_win.addstr(13, 18, "Invalid option")
                start_win.refresh()
                sleep(1)
                start_win.addstr(13, 14, "                    ")
        sleep(0.5)


if __name__ == '__main__':
    hunt = TheHunt()
    try:
        hunt.start()
        print("Hello World!")
    except KeyboardInterrupt:
        print("Terminated")
    finally:
        curses.endwin()

