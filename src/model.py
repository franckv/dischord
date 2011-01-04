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


# note durations (W=Whole, ...)
(W, H, Q, E, S, T, X) = [64, 32, 16, 8, 4, 2, 1]

class Beat(object):
    def __init__(self):
        self.text = None
        self.duration = 0
        self.dotted = False
        self.nuplet = None
        self.notes = []
        self.vibrato = False
        self.tapping = False
        self.slapping = False
        self.popping = False
        self.fadeIn = False

class Note(object):
    def __init__(self):
        self.string = 0
        self.fret = 0
        self.tied = False
        self.dead = False
        self.hammer = False
        self.slide = False
        self.bend = 0
