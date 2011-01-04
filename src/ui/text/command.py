import os, os.path

from mingus.core import scales, chords

from guitar import Guitar
from parsers import ReaderFactory

from . import tab, chord

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
    scope = [min(int(n), len(song.measures)) for n in options.range.split(',')]

    tab.show_tab(song, options.track, scope)

    reader.close()

def do_diagram(options, notes):
    notes = notes.lower().replace('x','-1')
    frets = [int(f) for f in notes.split(',')]

    chord.show_chord(frets)

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

