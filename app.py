#!/usr/bin/python3

import curses

from bin.thehunt import TheHunt

if __name__ == '__main__':
    hunt = TheHunt()
    try:
        curses.wrapper(hunt.start)
    except KeyboardInterrupt:
        print("Terminated")
    finally:
        curses.endwin()
    exit()
