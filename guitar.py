from mingus.containers import Note
from mingus.core import scales, chords

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

    def show_scale(self, scale, scope=None):
        if scope is None:
            scope = range(0, self.frets + 1)

        self.show_ruler(scope)
        first = True
        for string in self.tuning:
            if not first:
                self.show_filler(scope)
            else:
                first = False

            self.show_string(scope, string, scale)

    def show_chord(self, chord, scope=None):
        if scope is None:
            scope = range(0, self.frets + 1)

        self.show_ruler(scope)
        first = True
        for string in self.tuning:
            if not first:
                self.show_filler(scope)
            else:
                first = False

            self.show_string(scope, string, chord)



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

    def show_string(self, scope, string, scale=None):
        filler = '|'
        for n in scope:
            d = scale and self.in_scale(scale, string, n)
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

    def in_scale(self, scale, string, n):
        inote = int(string) + n
        note = Note().from_int(inote)

        if note.name in scale:
            return scale.index(note.name) + 1
        else:
            return 0

if __name__ == '__main__':
    g = Guitar()
    scope = range(0, 13)
    #g.show(scope)
    g.show_scale(scales.diatonic('C'), scope)

    print
    scope = range(0, 13)
    g.show_chord(chords.from_shorthand('Am'), scope)
