import cv2 as cv 
import numpy as np
import zlib


class VideoStream:
    '''
    Creates a video stream
    '''
    
    def __init__(self, videofile, resize=(640, 480)):
        # initialize capture
        self.cap = cv.VideoCapture(videofile)

        # output video dimensions
        self.out_dim = resize
    
    def read_frame(self):
        '''
        Read frame from the source and convert into bytes
        '''
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv.resize(frame, self.out_dim)
        # flatten the array
        frame = np.array(frame, dtype=np.uint8).reshape(1, -1)
        frame = bytearray(frame)
        databytes = zlib.compress(frame, 9)
        return databytes
    
    def extract_frame(self, databytes):
        '''
        Get frame from bytes
        '''
        frame = zlib.decompress(databytes)
        frame = np.array(list(frame), dtype=np.uint8).reshape((self.out_dim[1], self.out_dim[0], 3))
        return frame


