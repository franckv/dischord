import log
import re
import curses

from guitar import Guitar

from ui.ncurses.widget import TextPanel

class CommandHandler(object):
    def __init__(self, screen):
        self.screen = screen
        self.buf = ''

    def handle(self):
        curses.curs_set(0)
        while True:
            c = self.screen.get_char()
            log.debug(c)

            if c is None:
                continue


            (y, x) = self.screen.get_pos()
            self.screen.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))

            events = ['<KEY_LEFT>', '<KEY_RIGHT>', '<KEY_DOWN>', '<KEY_UP>', '<KEY_RESIZE>', '<KEY_ENTER>', '<KEY_BACKSPACE>', '<KEY_TAB>', '<KEY_BTAB>']

            if c in events:
                self.screen.send_event(c)
            elif c == ':':
                cmd = self.screen.read_command()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, cmd.strip()))
                self.run_command(cmd)
            elif c == '/':
                search = self.screen.read_search()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, search.strip()))
                self.run_search(search)
            else:
                log.debug('unknown command %s' % c)

    def run_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            self.screen.destroy()
        elif cmd.startswith('scale '):
            scale = cmd[5:]
            g = Guitar(frets = 12)

            self.screen.main.show_tab('main')
            self.screen.main.current.clear_lines()
            self.screen.set_status('Scale: %s' % scale)
            self.screen.update_title()
        elif cmd == 'clear':
            self.screen.main.current.clear_lines()
            self.screen.set_status('cleared')
        else:
            pass

    def run_search(self, search):
        pass

