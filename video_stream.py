import numpy as np
import zlib
from constants import CHUNK

class VideoStream:
    '''
    Creates a video stream
    '''
    
    def __init__(self, videofile):
        # initialize stream
        self.stream = open(videofile, 'rb')

    def read(self):
        '''
        Read CHUNK from the stream
        '''
        data = self.stream.read(CHUNK)
        if not data:
            return None
        # data = zlib.compress(data, 9)
        return data
    


