import os, sys
from optparse import OptionParser
import logging

import ui.text, ui.ncurses

if __name__ == '__main__':
    logging.basicConfig(
        level = logging.WARN,
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename = '/tmp/dischord.log',
        filemode = 'w'
    )

    logging.debug('Start')
   
    usage = 'Usage: %prog COMMAND [ARGS]'
    parser = OptionParser(usage)
    parser.add_option('-m', '--mode', dest='mode', default='major', help='mode of the scale: major (default), harmonic_minor, ionian, ...')
    parser.add_option('-r', '--range', dest='range', default='0,5', help='range of the frets to display')
    parser.add_option('-f', '--frets', dest='frets', type='int', default=12, help='number of frets on the neck')

    parser.add_option('-t', '--track', dest='track', type='int', default=0, help='track to display')

    parser.add_option('--ui', dest='ui', default='console', help='interface: curses or console (default)')
   
    (options, args) = parser.parse_args()
   
    if options.ui == 'curses':
        ui.ncurses.run()
    else:
        ui.text.run(options, args)

    logging.debug('Stop')

