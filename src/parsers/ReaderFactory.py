from GP3Reader import GP3Reader
from GP4Reader import GP4Reader

def getReader(filename):
    if filename.endswith('.gp3'):
        return GP3Reader(filename)
    elif filename.endswith('.gp4'):
        return GP4Reader(filename)
    else:
        return None
