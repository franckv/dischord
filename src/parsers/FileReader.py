import struct

class FileReader:
    def __init__(self, path):
        self.path = path
        # little endian
        self.endianess = 0

    def open(self):
        self.file = open(self.path, "rb")

    def close(self):
        self.file.close()

    def getPaddedString(self, pad = 0):
        if pad == 0: pad = self.readInt() - 1
        l = self.readByte()

        if l == 0:
            s = ''
        else:
            s = self.readString(pad)
            if pad > l: s = s[0:l]

        return s

    def readString(self, size = 0):
        if size == 0: size = self.readByte()
        s = self.file.read(size)

        return s

    def readByte(self):
        s = self.file.read(1)
        return struct.unpack('B', s)[0]
        #return ord(s[0])

    def readSignedByte(self):
        s = self.file.read(1)
        return struct.unpack('b', s)[0]

    def readChar(self):
        s = self.file.read(1)
        return s

    def readBool(self):
        s = self.file.read(1)
        return (ord(s) == 1)

    def readShort(self):
        if self.endianess == 0:
            format = '<H'
        else:
            format = '>H'
        s = self.file.read(2)
        return struct.unpack(format, s)[0]

    def readInt(self):
        if self.endianess == 0:
            format = '<I'
        else:
            format = '>I'
        s = self.file.read(4)
        i = struct.unpack(format, s)[0]
        if i > 1000:
            print(i)
            raise Exception('Integer Overflow')
        return i

    def readSignedInt(self):
        if self.endianess == 0:
            format = '<i'
        else:
            format = '>i'
        s = self.file.read(4)
        i = struct.unpack(format, s)[0]
        if abs(i) > 1000:
            print(i)
            raise Exception('Integer Overflow')
        return i


    def skip(self, c):
        self.file.read(c)

    def readColor(self):
        colR = self.readByte()
        colG = self.readByte()
        colB = self.readByte()
        colW = self.readByte()

        return (colR, colG, colB, colW)
