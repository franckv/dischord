class Song(object):
    def __init__(self):
        self.channels = []
        self.measures = []
        self.tracks = []

class Channel(object):
    def __init__(self, instrument):
        self.instrument = instrument

class Measure(object):
    def __init__(self, signum, sigden):
        self.signature = (signum, sigden)
        self.repeatOpen = False
        self.repeatClose = self.repeatAlt = 0
        self.doubleBar = False
        self.marker = None
        self.markercolor = (0, 0, 0, 0)
        self.tracks = []

class Track(object):
    def __init__(self, name, nstrings):
        self.name = name
        self.nstrings = nstrings
        self.tuning = []
        self.measures = []

class MeasureTrack(object):
    def __init__(self, measure, track):
        self.measure = measure
        self.track = track
        self.beats = []

class Beat(object):
    def __init__(self):
        self.text = None
        self.dotted = False
        self.nuplet = None
        self.notes = []

class Note(object):
    def __init__(self):
        self.string = 0
        self.fret = 0
