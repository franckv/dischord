import logging
import curses

import common
from pycurses_widgets import Screen, StatusBar, CommandBar, TitleBar, TextPanel, TabPanel
from ui.ncurses.commandhandler import CommandHandler

class Window(Screen):
    def __init__(self, win):
        super(Window, self).__init__(win)

        self.title = TitleBar(self)

        self.main = TabPanel(self)
        self.main.create_tab(TextPanel, 'main')
        self.main.create_tab(TextPanel, 'help')
        self.main.tabs['help'].add_line('Help !')

        self.status = StatusBar(self)
        self.command = CommandBar(self)

        self.main.register_event('<KEY_TAB>', self.show_next_tab)
        self.main.register_event('<KEY_BTAB>', self.show_prev_tab)

        self.handler = CommandHandler(self)

        self.command.register_event(':', self.handler.run_command)
        self.command.register_event('/', self.handler.run_search)

        self.redraw()

    def send_event(self, event):
        logging.debug('received event %s' % event)
        return super(Window, self).send_event(event) or \
            self.main.send_event(event) or \
            self.command.send_event(event)

    def set_status(self, text):
        self.status.set_text(text)

    def set_title(self, text):
        self.title.set_text(text)

    def get_char(self):
        return self.command.get_char()

    def show_next_tab(self, event=None):
        self.main.show_next_tab()
        self.update_title()

    def show_prev_tab(self, event=None):
        self.main.show_prev_tab()
        self.update_title()

    def update_title(self):
        title = ''
        for tab in self.main.childs:
            if title != '':
                title += ' '
            if tab.name == self.main.current.name:
                title += '[%s]' % tab.name
            else:
                title += tab.name

        self.set_title('%s v%s %s' % (common.PROGNAME, common.PROGVERSION, title))

    def read(self, c):
        return self.command.read(c, self.validate_command_input)

    def validate_command_input(self, c):
        (y, x) = self.command.get_pos()
        self.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))
    
        return True

    def run(self):
        curses.curs_set(0)
        self.handle_events()

