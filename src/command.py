import os, os.path

from mingus.core import scales, chords

from guitar import Guitar
from tabreader import GP3Reader

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
        print line

def do_chord(options, chord):
    g = Guitar(frets=options.frets)
    scope = get_scope(options, g)

    lines = g.get_chord(chord, scope)
    for line in lines:
        print line

def do_tab(options, filename):
    reader = GP3Reader(filename)
    reader.open()
    song = reader.parseSong()
    track = song.tracks[options.track]
    scope = [int(n) for n in options.range.split(',')]
    show_tab(track, scope)
    reader.close()

def show_tab(track, measures=(0, 5)):
    strings = ['|' for i in range(track.nstrings)]
    for measure in track.measures[measures[0]:measures[1]]:
        #for beat in measure.beats:
        #    for note in beat.notes:
        #        print '%i/%i [%i]' % (note.string, note.fret, note.type)
        #    print

        for beat in measure.beats:
            for i in range(track.nstrings):
                note = None
                for n in beat.notes:
                    if n.string == i+1:
                        note = n
                if note is None or note.type == 2:
                    strings[i] += '--'
                else:
                    strings[i] += str(note.fret)
                    if note.fret < 10:
                        strings[i] += '-'

                strings[i] += '-'
        for i in range(track.nstrings):
            strings[i] += '|'

    for string in strings:
        print string

def get_scope(options, g):
    if options.range:
        try:
            (min,max) = [int(n) for n in options.range.split(',')]
            if min < 0: min = 0
            if max > g.frets: max = g.frets
            scope = range(min, max + 1)
        except:
            scope = range(0, g.frets + 1)
    else:
        scope = range(0, g.frets + 1)

    return scope

list = {
        'scale': {'args': 1, 'exec': do_scale},
        'chord': {'args': 1, 'exec': do_chord},
        'tab': {'args': 1, 'exec': do_tab},
        }

