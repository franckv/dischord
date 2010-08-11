from model import Song, Channel, Measure, Track, MeasureTrack, Beat, Note
from filereader import FileReader

class GP3Reader(FileReader):
    def parseSong(self):
        song = Song()

        self.parseProperties(song)
        self.parseChannels(song)

        nmeasures = self.readInt()
        ntracks = self.readInt()

        for i in range(nmeasures):
            measure = self.parseMeasure()
            measure.pos = i
            song.measures.append(measure)
        for j in range(ntracks):
            track = self.parseTrack()
            song.tracks.append(track)
        for i in range(nmeasures):
            measure = song.measures[i]
            for j in range(ntracks):
                track = song.tracks[j]
                measuretrack = self.parseMeasureTrack(measure, track)
                measure.tracks.append(measuretrack)
                track.measures.append(measuretrack)

        return song

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
        nlines = self.readInt()
        for i in range(nlines):
            song.comment += self.getPaddedString()

        song.tripletfeel = self.readBool()
        song.tempo = self.readInt()
        song.key = self.readInt()

    def parseChannels(self, song):
        for port in range(4):
            for channelno in range(16):
                instrument = self.readInt()
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
        nstrings = self.readInt()
        track = Track(trackname, nstrings)

        for j in range(7):
            tuning = self.readInt()
            track.tuning.append(tuning)
        track.port = self.readInt()
        track.channel = self.readInt() - 1
        track.effectChannel = self.readInt() - 1
        track.frets = self.readInt()
        track.capo = self.readInt()
        track.color = self.readColor()

        return track

    def parseMeasureTrack(self, measure, track):
        measuretrack = MeasureTrack(measure, track)
        nbeats = self.readInt()
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
            beat.nuplet = self.readInt()

        if flags & 2:
            self.parseChord()

        if flags & 4:
            self.text = self.getPaddedString()

        if flags & 8:
            self.parseBeatEffect(beat)

        if flags & 16:
            self.parseMixChange()
        
        stringmap = self.readByte()
        for string in range(7):
            if stringmap & (1 << string):
                note = self.parseNote()
                note.string = string
                beat.notes.append(note)

        return beat

    def parseBeatEffect(self, beat):
        flags = self.readByte()

        if flags & 1:
            beat.Vibrato = True
        if flags & 2:
            beat.Vibrato = True
        if flags & 16:
            beat.FadeIn = True
        if flags & 32:
            raise Exception('not implemented')
        if flags & 64:
            raise Exception('not implemented')

    def parseNote(self):
        note = Note()
        flags = self.readByte()
        
        if flags & 32:
            note.type = self.readByte()

        if flags & 1:
            note.duration = self.readByte()
            note.nuplet = self.readByte()
            raise Exception('not implemented')

        if flags & 16:
            note.dynamic = self.readByte()
        else:
            note.dynamic = 6

        if flags & 32:
            note.fret = self.readByte()
        
        if flags & 128:
            lfinger = self.readByte()
            rfinger = self.readByte()

        if flags & 8:
            self.parseNoteEffect(note)

        return note

    def parseNoteEffect(self, note):
        flags = self.readByte()

        if flags & 1:
            note.bend = self.readBend()
        if flags & 4:
            note.slide = True
        if flags & 2:
            note.hammer = True
        if flags & 16:
            note.grace = self.readGrace()

    def readBend(self):
        type = self.readByte()
        weight = self.readInt()
        npoints = self.readInt()

        for i in range(npoints):
            timepos = self.readInt()
            vertpos = self.readInt()
            vibrato = self.readByte()

    def readGrace(self):
        fret = self.readByte()
        dynamic = self.readByte()
        transition = self.readByte()
        duration = self.readByte()

if __name__ == '__main__':
    reader = GP3Reader('tests/test.gp3')

    reader.open()

    song = reader.parseSong()
    song.show()

    reader.close()
