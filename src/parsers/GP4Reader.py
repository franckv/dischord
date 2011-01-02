from model import Song, Channel, Measure, Track, MeasureTrack, Beat, Note
from .GPReader import GPReader

class GP4Reader(GPReader):
    def parseProperties(self, song):
        song.version = self.getPaddedString(30)
        song.title = self.getPaddedString()
        song.subtitle = self.getPaddedString()
        song.artist = self.getPaddedString()
        song.album = self.getPaddedString()
        song.author = self.getPaddedString()
        song.copyright = self.getPaddedString()
        song.creator = self.getPaddedString()
        song.instructions = self.getPaddedString()

        song.comment = ''
        nlines = self.readSignedInt()
        for i in range(nlines):
            song.comment += self.getPaddedString()

        song.tripletfeel = self.readBool()

        song.lyricTrack = self.readInt()
        self.parseLyrics()

        song.tempo = self.readSignedInt()
        song.key = self.readSignedInt()
        song.octave = self.readByte()

    def parseLyrics(self):
        for i in range(5):
            self.skip(4)
            l = self.readInt()
            if l > 0:
                s = self.readString(l)

    def parseChannels(self, song):
        for port in range(4):
            for channelno in range(16):
                instrument = self.readSignedInt()
                channel = Channel(instrument)
                channel.port = port
                channel.number = channelno
                channel.volume = self.readByte()
                channel.balance = self.readByte()
                channel.chorus = self.readByte()
                channel.reverb = self.readByte()
                channel.phaser = self.readByte()
                channel.tremolo = self.readByte()
                blank1 = self.readByte()
                blank2 = self.readByte()
                song.channels.append(channel)

    def parseMeasure(self):
        signum = sigden = 4
        flags = self.readByte()
        # numerator
        if flags & 1:
            signum = self.readByte()
        # denominator
        if flags & 2:
            sigden = self.readByte()

        measure = Measure(signum, sigden)

        # begin repeat
        if flags & 4:
            measure.repeatOpen = True
        # end repeat
        if flags & 8:
            measure.repeatClose = self.readByte()
        #no of alt ending
        if flags & 16:
            measure.repeatAlt = self.readByte()
        # marker
        if flags & 32:
            measure.marker = self.getPaddedString()
            measure.markercolor = self.readColor()
        # tonality
        if flags & 64:
            self.readByte()
            self.readByte()
        # double bar
        if flags & 128:
            measure.doubleBar = True

        return measure

    def parseTrack(self):
        flags = self.readByte()
        trackname = self.getPaddedString(40)
        nstrings = self.readSignedInt()
        track = Track(trackname, nstrings)

        for j in range(7):
            tuning = self.readSignedInt()
            track.tuning.append(tuning)
        track.port = self.readSignedInt()
        track.channel = self.readSignedInt() - 1
        track.effectChannel = self.readSignedInt() - 1
        track.frets = self.readSignedInt()
        track.capo = self.readSignedInt()
        track.color = self.readColor()

        return track

    def parseMeasureTrack(self, measure, track):
        measuretrack = MeasureTrack(measure, track)
        nbeats = self.readSignedInt()
        for i in range(nbeats):
            beat = self.parseBeat()
            measuretrack.beats.append(beat)

        return measuretrack

    def parseBeat(self):
        beat = Beat()
        flags = self.readByte()

        if flags & 64:
            beat.status = self.readByte()

        duration = self.readSignedByte()
        duration = pow(2, 4 - duration)
        beat.duration = duration

        if flags & 1:
            beat.dotted = True

        if flags & 32:
            beat.nuplet = self.readSignedInt()

        if flags & 2:
            header = self.readByte()
            if header & 1:
                raise Exception('Not implemented')
            else:
                chordname = self.getPaddedString()
                firstfret = self.readInt()
                if (firstfret != 0):
                    for i in range(6):
                        fret = self.readInt()

        if flags & 4:
            self.text = self.getPaddedString()

        if flags & 8:
            self.parseBeatEffect(beat)

        if flags & 16:
            self.parseMixChange()
        
        stringmap = self.readByte()
        for string in reversed(list(range(7))):
            if stringmap & (1 << string):
                note = self.parseNote()
                note.string = 7 - string
                note.map = stringmap
                beat.notes.append(note)

        return beat

    def parseBeatEffect(self, beat):
        flags = self.readByte()
        flags2 = self.readByte()

        if flags & 2:
            beat.vibrato = True

        if flags & 16:
            beat.fadeIn = True

        if flags & 32:
            type = self.readByte()
            if type == 1:
                beat.tapping = True
            elif type == 2:
                beat.slapping = True
            elif type == 3:
                beat.popping = True

        if flags2 & 4:
            beat.tremolo = self.parseBend()

        if flags & 64:
            raise Exception('Not implemented')

        if flags2 & 2:
            self.readByte()

    def parseMixChange(self):
        instrument = self.readSignedByte()
        volume = self.readSignedByte()
        pan = self.readSignedByte()
        chorus = self.readSignedByte()
        reverb = self.readSignedByte()
        phaser = self.readSignedByte()
        tremolo = self.readSignedByte()
        tempo = self.readSignedInt()
        
        if volume >= 0:
            volumeduration = self.readByte()
        if pan >= 0:
            panduration = self.readByte()
        if chorus >= 0:
            chorusduration = self.readByte()
        if reverb >= 0:
            reverbduration = self.readByte()
        if phaser >= 0:
            phaserduration = self.readByte()
        if tremolo >= 0:
            tremoloduration = self.readByte()
        if tempo >= 0:
            tempoduration = self.readByte()
        self.readByte()

    def parseNote(self):
        note = Note()
        flags = self.readByte()
        
        if flags & 64:
            note.accentuated = True

        if flags & 4:
            note.ghost = True

        if flags & 32:
            note.type = self.readByte()
            if note.type == 2:
                note.tied = True
            elif note.type == 3:
                note.dead = True

        if flags & 1:
            note.duration = self.readByte()
            note.nuplet = self.readByte()

        if flags & 16:
            note.dynamic = self.readByte()
        else:
            note.dynamic = 6

        if flags & 32:
            note.fret = self.readByte()
        
        if flags & 128:
            note.lfinger = self.readByte()
            note.rfinger = self.readByte()

        if flags & 8:
            self.parseNoteEffect(note)

        return note

    def parseNoteEffect(self, note):
        flags = self.readByte()
        flags2 = self.readByte()

        if flags & 2:
            note.hammer = True

        if flags2 & 64:
            note.vibrato = True

        if flags2 & 2:
            note.palmMute = True

        if flags2 & 1:
            note.staccato = True

        if flags & 1:
            note.bend = self.parseBend()

        if flags & 16:
            note.grace = self.parseGrace()

        if flags2 & 4:
            note.tremoloPicking = self.readByte()

        if flags2 & 8:
            note.slide = True
            self.readByte()

        if flags2 & 16:
            note.harmonics = self.readByte()

        if flags2 & 32:
            note.trill = True
            fret = self.readByte()
            period = self.readByte()

    def parseBend(self):
        type = self.readByte()
        weight = self.readSignedInt()
        npoints = self.readSignedInt()

        for i in range(npoints):
            timepos = self.readSignedInt()
            vertpos = self.readSignedInt()
            vibrato = self.readByte()

        return type

    def parseGrace(self):
        fret = self.readByte()
        dynamic = self.readByte()
        transition = self.readByte()
        duration = self.readByte()

if __name__ == '__main__':
    reader = GP4Reader('tests/test.gp4')

    reader.open()

    song = reader.parseSong()
    song.show()

    reader.close()
