import socket
from util import Util
import cv2 as cv 
from constants import *
import threading
import zlib
import numpy as np 
import struct

class VideoClient:

    def __init__(self, saddr=("127.0.0.1", 8000), caddr=("127.0.0.1", 10000), filename="test2.mp4"):
        self.saddr = saddr
        self.caddr = caddr

        # control sock
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.csock.bind(caddr)
        self.csock.connect(saddr)
        self.csock.settimeout(0.1)
        self.running = True

        # data sock
        self.dsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dsock.bind((caddr[0], caddr[1]+1))
        self.dsock.connect(saddr)

        cutil = Util(self.csock)

        # send filename
        cutil.send(filename.encode('ascii'))

        # send SETUP request
        self.cutil = cutil
        cutil.send(SETUP.encode('ascii'))

        # TODO: get video details
        self.out_dim = (640, 480)

        # PLAY stream
        cutil.send(PP.encode('ascii'))
        self.playing = True
        self.player = threading.Thread(target=self.play, args=())
        self.player.start()
        while self.running:
            try:
                cutil.send(HEARTBEAT.encode('ascii'))
                l = self.csock.recv(4)
                l = struct.unpack('!I', l)
                msg = self.csock.recv(l).decode('ascii')
                if msg == EXIT:
                    self.running = False
                    self.playing = False
                    break
            except Exception as e:
                continue
        self.csock.close()
    
    def play(self):
        dutil = Util(self.dsock)
        # TODO: if connection lost keep max_timeout in util and raise exception if reached
        while self.playing:
            try:
                data = dutil.recv()
            except:
                print('Server closed...')
                self.running = False
                break
            frame = self.extract_frame(data)
            cv.imshow("video", frame)
            key = cv.waitKey(1)
            # QUIT
            if key == ord('q'):
                self.quit()
                break
            # PLAY/PAUSE
            elif key == ord('p'):
                self.pp()
                while True:
                    key = cv.waitKey(0)
                    if key == ord('q'):
                        self.quit()
                        break
                    elif key == ord('p'):
                        self.pp()
                        break
        self.dsock.close()
        cv.destroyAllWindows()
                    
    def pp(self):
        # perform play/pause action
        self.cutil.send(PP.encode('ascii'))

    def quit(self):
        self.cutil.send(EXIT.encode('ascii'))
        self.playing = False
        self.running = False

    def extract_frame(self, databytes):
        '''
        Get frame from bytes
        '''
        frame = zlib.decompress(databytes)
        frame = np.array(list(frame), dtype=np.uint8).reshape((self.out_dim[1], self.out_dim[0], 3))
        return frame

if __name__ == "__main__":
    print('Controls:')
    print('p: PAUSE/PLAY')
    print('q: QUIT')
    vc = VideoClient()
    # TODO: improve frame rate, use CHUNK encoding (?)