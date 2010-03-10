from mingus.containers import Note

from tuning import Tuning, Standard

class Guitar:
    def __init__(self, tuning = None, frets = 12):
        if tuning is None:
            self.tuning = Standard
        else:
            self.tuning = tuning

        self.frets = frets


    def show(self, scope=None):
        if scope is None:
            scope = range(0, self.frets + 1)

        self.show_ruler(scope)
        first = True
        for string in self.tuning:
            if not first:
                self.show_filler(scope)
            else:
                first = False

            self.show_string(scope, string)

    def show_notes(self, notes, scope=None):
        if scope is None:
            scope = range(0, self.frets + 1)

        self.show_ruler(scope)
        first = True
        for string in self.tuning:
            if not first:
                self.show_filler(scope)
            else:
                first = False

            self.show_string(scope, string, notes)

    def show_ruler(self, scope):
        ruler = ''
        for n in scope:
            ruler += ' '
            if n == 0:
                ruler += '0'
            else:
                if n < 10:
                    ruler += ' %i ' % n
                else:
                    ruler += ' %i' % n

        print ruler

    def show_string(self, scope, string, notes=None):
        filler = '|'
        for n in scope:
            d = notes and self.in_scale(notes, string, n)
            if d:
                c = self.format_note(d)
            else:
                c = '-'
            if n == 0:
                filler += c
            else:
                filler += '-%s-' % c
            filler += '|'

        print filler

    def format_note(self, d):
        red = '\033[01;31m'
        blue = '\033[34m'
        gray =  '\033[39m'
        yellow = '\033[33m'
        green = '\033[32m'
        endc = '\033[0m'

        if d == 1:
            color = red
        elif d == 3:
            color = gray
        elif d == 5:
            color = gray
        elif d == 7:
            color = gray
        else:
            color = gray
        return color + '%i' % d + endc

    def show_filler(self, scope):
        filler = '|'
        for n in scope:
            if n == 0:
                filler += ' '
            else:
                filler += '   '
            filler += '|'

        print filler

    def in_scale(self, notes, string, n):
        note = int(string) + n

        for i,val in enumerate(notes):
            if note % 12 == int(Note(val)) % 12:
                return i + 1
        return 0

