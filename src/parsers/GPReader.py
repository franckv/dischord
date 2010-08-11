from model import Song
from FileReader import FileReader

class GPReader(FileReader):
    def parseSong(self):
        song = Song()

        self.parseProperties(song)
        self.parseChannels(song)

        nmeasures = self.readSignedInt()
        ntracks = self.readSignedInt()

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
