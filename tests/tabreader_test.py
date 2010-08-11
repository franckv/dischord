import unittest

from tabreader import GP3Reader

class TestGP3Reader(unittest.TestCase):
    def setUp(self):
        self.reader = GP3Reader('tests/test.gp3')
        self.reader.open()

    def tearDown(self):
        self.reader.close()

    def test_parseSong(self):
        song = self.reader.parseSong()

        self.assertNotEqual(song, None)

        self.assertNotEqual(song.version, None)
        self.assertNotEqual(song.title, None)
        self.assertNotEqual(song.subtitle, None)
        self.assertNotEqual(song.artist, None)
        self.assertNotEqual(song.album, None)
        self.assertNotEqual(song.author, None)
        self.assertNotEqual(song.copyright, None)
        self.assertNotEqual(song.creator, None)
        self.assertNotEqual(song.instructions, None)
        self.assertNotEqual(song.comment, None)
        self.assertNotEqual(song.tripletfeel , None)
        self.assertNotEqual(song.tempo, None)
        self.assertNotEqual(song.key, None)

        self.assertNotEqual(len(song.channels), 0)
        self.assertNotEqual(len(song.measures), 0)
        self.assertNotEqual(len(song.tracks), 0)

        for chan in song.channels:
            self.assertNotEqual(chan.instrument, None)

        for measure in song.measures:
            self.assertNotEqual(measure.signature, None)
            self.assertNotEqual(measure.repeatOpen, None)
            self.assertNotEqual(measure.repeatClose, None)
            self.assertNotEqual(measure.repeatAlt, None)
            self.assertNotEqual(measure.doubleBar, None)
            self.assertNotEqual(measure.markercolor, None)
            self.assertNotEqual(len(measure.tracks), 0)

        for track in song.tracks:
            self.assertNotEqual(track.name, None)
            self.assertNotEqual(track.nstrings, None)
            self.assertNotEqual(track.tuning, None)
            self.assertNotEqual(track.frets, None)
            self.assertNotEqual(track.capo, None)
            self.assertNotEqual(track.color, None)
            self.assertNotEqual(len(track.measures), 0)
            for measure in track.measures:
                self.assertTrue(self.checkBeats(measure))

    def checkBeats(self, measure):
        sum = 0 
        nuplets = 0
        for beat in measure.beats:
            duration = beat.duration
        
            if beat.dotted:
                duration += duration / 2
            
            if beat.nuplet:
                nuplets += 1
                if beat.nuplet == 3:
                    if nuplets == 3:
                        duration = 0
                else:
                    raise Exception('Not implemented')
            else:
                nuplets = 0
        
            sum += duration
            
        (signum, sigden) = measure.measure.signature
        check = signum * (64/sigden)

        return sum == check

if __name__ == '__main__':
    unittest.main()

