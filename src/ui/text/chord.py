EMPTY='.'
FULL='*'

def show_chord(frets):
    nstrings = len(frets)
    start = min(frets)

    if start > 1:
        print('  -' + (nstrings-1) * ' -')
    elif start == 1:
        print('  ' + (nstrings*2-1) * '=')
    else:
        line = '  '
        first = True
        for f in frets:
            if not first:
                line += '='
            else:
                first = False
            if f == 0:
                line += 'O'
            elif f == -1:
                line += 'X'
            else:
                line += '='

        print(line)

    start = max(1, start)
    for i in range(5):
        if i == 0:
            line = str(start)
            if start < 10:
                line += ' '
        else:
            line = '  '

        first = True
        for f in frets:
            if not first:
                line += ' '
            else:
                first = False
            if f == start + i:
                line += FULL
            else:
                line += EMPTY

        print(line)


if __name__ == '__main__':
    show_chord([0, 2, 2, 1, 0, 0])
    show_chord([-1, 3, 2, 0, 1, 0])
    show_chord([5, 7, 7, 6, 5, 5])
