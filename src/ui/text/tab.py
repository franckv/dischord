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

def show_tab(song, ntrack, scope):
    track = song.tracks[ntrack]

    for subscope in split_scope(scope, 5):
        show_scope(track, subscope)
 
def show_scope(track, measures=(0, 5)):
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


