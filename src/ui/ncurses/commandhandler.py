import logging

from guitar import Guitar

class CommandHandler(object):
    def __init__(self, app):
        self.app = app
        self.buf = ''

    def run_command(self, event):
        cmd = self.app.read(event)
        if cmd == 'q' or cmd == 'quit':
            self.app.destroy()
        elif cmd.startswith('scale '):
            scale = cmd[5:]
            g = Guitar(frets = 12)

            self.app.main.show_tab('main')
            self.app.main.current.clear_lines()
            self.app.set_status('Scale: %s' % scale)
            self.app.update_title()
        elif cmd == 'clear':
            self.app.main.current.clear_lines()
            self.app.set_status('cleared')
        else:
            pass

    def run_search(self, event):
        search = self.app.read(event)

