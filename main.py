import os, sys
from optparse import OptionParser
import logging

import log
import command
import ui.ncurses

if __name__ == '__main__':
    log.init(logging.WARN, '/tmp/dischord.log')
    log.debug('Start')
   
    usage = 'Usage: %prog COMMAND [ARGS]'
    parser = OptionParser(usage)
    parser.add_option('-m', '--mode', dest='mode', default='major', help='mode of the scale: major (default), harmonic_minor, ionian, ...')
    parser.add_option('-r', '--range', dest='range', help='range of the frets to display')
    parser.add_option('-f', '--frets', dest='frets', type='int', default=12, help='number of frets on the neck')

    parser.add_option('--ui', dest='ui', default='console', help='interface: curses or console (default)')
   
    (options, args) = parser.parse_args()
   
    if options.ui == 'curses':
        ui.ncurses.run()
    else:
        if len(args) == 0:
            parser.error('missing command')

        cmd = args[0]

        if not cmd in command.list:
            parser.error('invalid command')
        else:
            nargs = int(command.list[cmd]['args'])
           
            if nargs != len(args) - 1:
                parser.error('wrong number of arguments (expected %i)' % nargs)
            else:
                command.list[cmd]['exec'](options, *args[1:])

    log.debug('Stop')

