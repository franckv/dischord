from optparse import OptionParser

from mingus.core import scales, chords

from guitar import Guitar


if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage)
    parser.add_option('-s', '--scale', dest='scale', help='display scale starting at given root note')
    parser.add_option('-m', '--mode', dest='mode', default='major', help='mode of the scale: major (default), harmonic_minor, ionian, ...')
    parser.add_option('-c', '--chord', dest='chord', help='name of the chord to play')
    parser.add_option('-r', '--range', dest='range', help='range of the frets to display')


    (options, args) = parser.parse_args()

    g = Guitar()

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


    if options.scale:
        if options.mode == 'major':
            notes = scales.diatonic(options.scale)
        elif options.mode == 'minor':
            notes = scales.harmonic_minor(options.scale)
        elif options.mode == 'natural_minor':
            notes = scales.natural_minor(options.scale)
        elif options.mode == 'harmonic_minor':
            notes = scales.harmonic_minor(options.scale)
        elif options.mode == 'melodic_minor':
            notes = scales.melodic_minor(options.scale)
        elif options.mode == 'ionian':
            notes = scales.ionian(options.scale)
        elif options.mode == 'dorian':
            notes = scales.dorian(options.scale)
        elif options.mode == 'phrygian':
            notes = scales.phrygian(options.scale)
        elif options.mode == 'lydian':
            notes = scales.lydian(options.scale)
        elif options.mode == 'mixolydian':
            notes = scales.mixolydian(options.scale)
        elif options.mode == 'aeolian':
            notes = scales.aeolian(options.scale)
        elif options.mode == 'locrian':
            notes = scales.locrian(options.scale)
        else:
            notes = []
    elif options.chord:
        try:
            notes = chords.from_shorthand(options.chord)
        except:
            notes = []
    else:
        notes = []

    g.show_notes(notes, scope)

