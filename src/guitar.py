from mingus.core import scales, chords
from mingus.containers import Note

from tuning import Tuning, Standard

class Guitar:
    def __init__(self, tuning = None, frets = 12):
        if tuning is None:
            self.tuning = Standard
        else:
            self.tuning = tuning

        self.frets = frets

    def get_notes(self, notes, scope=None):
        lines = []

        if scope is None:
            scope = range(0, self.frets + 1)

        lines.append(self.get_ruler(scope))
        first = True
        for string in self.tuning:
            if not first:
                lines.append(self.get_filler(scope))
            else:
                first = False

            lines.append(self.get_string(scope, string, notes))

        return lines

    def get_scale(self, scale, mode = 'major', scope=None):
        pass

    def get_chord(self, chord, scope):
        notes = chords.from_shorthand(chord)

        return self.get_notes(notes, scope)

    def get_ruler(self, scope):
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

        return ruler

    def get_string(self, scope, string, notes=None):
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

        return filler

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

    def get_filler(self, scope):
        filler = '|'
        for n in scope:
            if n == 0:
                filler += ' '
            else:
                filler += '   '
            filler += '|'

        return filler

    def in_scale(self, notes, string, n):
        note = int(string) + n

        for i,val in enumerate(notes):
            if note % 12 == int(Note(val)) % 12:
                return i + 1
        return 0

