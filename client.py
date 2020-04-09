import socket
import cv2 as cv 
import numpy as np 
import struct
import time

class VideoClient:

    def __init__(self, addr=("", 8000)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        i = 0
        while True:
            length = self.sock.recv(4)
            length, = struct.unpack('!I', length)
            if length == 0:
                print('Finished streaming...')
                exit()
            databytes = self.recvall(length)
            assert(len(databytes) == length)
            img = np.array(list(databytes))
            img = np.array(img, dtype=np.uint8).reshape(480, 640, 3)
            cv.imshow("Stream", img)
            i += 1
            print(f'Received frame {i}', end='\r')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                self.sock.close()
                return

    def recvall(self, length):
        data = b''
        rem = length
        while rem > 0:
            data += self.sock.recv(rem)
            rem = length - len(data)
        return data

if __name__ == "__main__":
    vc = VideoClient()