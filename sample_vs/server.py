import socket
import cv2 as cv 
import numpy as np 
import struct
import time

class VideoServer:

    def __init__(self, addr=("", 8000)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(2)
        self.source = "test2.mp4"
        while True:
            sc, addr = self.sock.accept()
            self.handle(sc)
    
    def handle(self, sock):
        # Start video capture
        cap = cv.VideoCapture(self.source)
        print()
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("finished stream")
                length = struct.pack('!I', 0)
                sock.sendall(length)
                return
            frame = cv.resize(frame, (640, 480))
            frame = np.array(frame, dtype=np.uint8).reshape(1, -1)
            databytes = bytearray(frame)
            length = struct.pack('!I', len(databytes))
            try:
                sock.sendall(length)
                sock.sendall(databytes)
            except Exception as e:
                print(e)
                return
            i += 1
            print(f'Sent frame {i}', end='\r')

if __name__ == "__main__":
    vs = VideoServer()