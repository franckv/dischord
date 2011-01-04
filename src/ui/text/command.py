import os, os.path

from mingus.core import scales, chords

from guitar import Guitar
from parsers import ReaderFactory

def do_scale(options, scale):
    g = Guitar(frets=options.frets)
    scope = get_scope(options, g)

    if options.mode == 'major':
        notes = scales.diatonic(scale)
    elif options.mode == 'minor':
        notes = scales.harmonic_minor(scale)
    elif options.mode == 'natural_minor':
        notes = scales.natural_minor(scale)
    elif options.mode == 'harmonic_minor':
        notes = scales.harmonic_minor(scale)
    elif options.mode == 'melodic_minor':
        notes = scales.melodic_minor(scale)
    elif options.mode == 'ionian':
        notes = scales.ionian(scale)
    elif options.mode == 'dorian':
        notes = scales.dorian(scale)
    elif options.mode == 'phrygian':
        notes = scales.phrygian(scale)
    elif options.mode == 'lydian':
        notes = scales.lydian(scale)
    elif options.mode == 'mixolydian':
        notes = scales.mixolydian(scale)
    elif options.mode == 'aeolian':
        notes = scales.aeolian(scale)
    elif options.mode == 'locrian':
        notes = scales.locrian(scale)

    lines = g.get_notes(notes, scope)
    for line in lines:
        print(line)

def do_chord(options, chord):
    g = Guitar(frets=options.frets)
    scope = get_scope(options, g)

    lines = g.get_chord(chord, scope)
    for line in lines:
        print(line)

def do_tab(options, filename):
    reader = ReaderFactory.getReader(filename)
    reader.open()
    song = reader.parseSong()
    track = song.tracks[options.track]
    scope = [min(int(n), len(song.measures)) for n in options.range.split(',')]

    for subscope in split_scope(scope, 5):
        show_tab(track, subscope)
    reader.close()

def do_diagram(options, notes):
    pass

def split_scope(scope, r):
    inf = scope[0]
    sup = scope[1]
    result = []
    
    i = inf
    while i<sup:
        m = min(sup, i+r)
        result.append((i, m))
        i += r

    return result

def show_tab(track, measures=(0, 5)):
    strings = ['|' for i in range(track.nstrings)]
    for measure in track.measures[measures[0]:measures[1]]:
        for beat in measure.beats:
            for i in range(track.nstrings):
                note = None
                for n in beat.notes:
                    if n.string == i+1:
                        note = n
                if note is None or note.tied:
                    strings[i] += '--'
                elif note.dead:
                    strings[i] += 'x-'
                else:
                    strings[i] += str(note.fret)
                    if note.fret < 10:
                        strings[i] += '-'

                if note and note.hammer:
                    strings[i] += 'h'
                elif note and note.slide:
                    strings[i] += '/'
                elif note and note.bend > 0:
                    strings[i] += '^'
                else:
                    strings[i] += '-'
        for i in range(track.nstrings):
            strings[i] += '|'

    for string in strings:
        print(string)
    print()

def get_scope(options, g):
    if options.range:
        try:
            (min,max) = [int(n) for n in options.range.split(',')]
            if min < 0: min = 0
            if max > g.frets: max = g.frets
            scope = list(range(min, max + 1))
        except:
            scope = list(range(0, g.frets + 1))
    else:
        scope = list(range(0, g.frets + 1))

    return scope

cmd = {
    'scale': {'args': 1, 'exec': do_scale},
    'chord': {'args': 1, 'exec': do_chord},
    'tab': {'args': 1, 'exec': do_tab},
    'diagram': {'args': 1, 'exec': do_diagram},
}

