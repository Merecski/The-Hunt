#!/usr/bin/python3.6
from bin.thehunt import TheHunt
import curses

if __name__ == '__main__':
    hunt = TheHunt()
    try:
        curses.wrapper(hunt.start)
    except KeyboardInterrupt:
        print("Terminated")
    finally:
        curses.endwin()
    exit()
