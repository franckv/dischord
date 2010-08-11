from mingus.containers import Note

class Tuning:
    def __init__(self, notes = None):
        self.notes = notes

    def __iter__(self):
        for note in self.notes:
            yield note

Standard = Tuning((Note('E', 4), Note('B', 3), Note('G', 3), Note('D', 3), Note('A', 2), Note('E', 2)))
