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
        return ord(s[0])

    def readSignedByte(self):
        b = self.readByte()
        if b > 127:
            b -= 256
        return b

    def readChar(self):
        s = self.file.read(1)
        return s

    def readBool(self):
        s = self.file.read(1)
        return (ord(s) == 1)

    def readShortBE(self):
        s = self.file.read(2)
        return (ord(s[0]) << 8) + ord(s[1])

    def readShortLE(self):
        s = self.file.read(2)
        return (ord(s[1]) << 8) + ord(s[0])

    def readShort(self):
        if self.endianess == 0:
            return self.readShortLE()
        else:
            return self.readShortBE()

    def readIntBE(self):
        s = self.file.read(4)
        return (ord(s[0]) << 24) + (ord(s[1]) << 16) + (ord(s[2]) << 8) + ord(s[3])

    def readIntLE(self):
        s = self.file.read(4)
        return (ord(s[3]) << 24) + (ord(s[2]) << 16) + (ord(s[1]) << 8) + ord(s[0])

    def readInt(self):
        if self.endianess == 0:
            return self.readIntLE()
        else:
            return self.readIntBE()

    def readColor(self):
        colR = self.readByte()
        colG = self.readByte()
        colB = self.readByte()
        colW = self.readByte()

        return (colR, colG, colB, colW)
