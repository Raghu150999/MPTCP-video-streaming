import socket
import cv2 as cv 
import numpy as np 
import struct
import time
import threading
from util import Util
from video_stream import VideoStream
from constants import *

class VideoServer:

    def __init__(self, addr=("127.0.0.1", 8000)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(5)
        self.connections = {}
        while True:
            # control socket must be even port
            # data socket port = control socket port + 1
            sc, addr = self.sock.accept()
            port = addr[1]
            # data socket
            if port % 2 == 1:
                control_port = port - 1
                caddr = (addr[0], control_port)
                # control socket exists
                if self.connections.get(caddr) != None:
                    self.connections[caddr].attach_data_sock(sc)
                    self.connections[caddr].start()
                continue
            self.connections[addr] = ClientHandler(sc, addr)

class ClientHandler(threading.Thread):

    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.data_sock = None
        self.streaming = False
        self.completed = False
        self.fnbr = 0

    def run(self):
        self.handle()

    def terminate(self):
        self.sock.close()
        # if stream is live, quit stream
        if self.streaming:
            self.streaming = False
            self.streamer.join()
        if self.data_sock:
            self.data_sock.close()
    
    # control socket
    def handle(self):
        sock = self.sock
        util = Util(sock)
        self.util = util

        # get video filename
        filename = util.recv().decode('ascii')

        cmd = util.recv().decode('ascii')
        if cmd != SETUP:
            util.send(EXIT.encode('ascii'))
            self.terminate()
            return

        # Start video capture
        self.vs = VideoStream(filename)
        
        while True:
            cmd = util.recv().decode('ascii')
            if cmd == EXIT:
                self.terminate()
                return
            elif cmd == PP and not self.streaming:
                self.streamer = threading.Thread(target=self.start_streaming, args=())
                self.streamer.start()
            elif cmd == PP and self.streaming:
                self.streaming = False
                self.streamer.join()
            elif cmd == HEARTBEAT:
                pass
            if self.completed:
                util.send(EXIT.encode('ascii'))
                self.terminate()
                return
    
    # data socket
    def start_streaming(self):
        self.streaming = True
        util = Util(self.data_sock)
        while self.streaming:
            frame = self.vs.read_frame()
            if frame == None:
                print("Finished streaming...")
                self.streaming = False
                self.completed = True
                break
            data = self.vs.read_frame()
            try:
                util.send(data)
            except Exception as e:
                print('Client closed...')
                self.streaming = False
                break
            self.fnbr += 1
            print(f'Sent frame {self.fnbr}', end='\r')
        self.data_sock.close()

    def attach_data_sock(self, sock):
        self.data_sock = sock

if __name__ == "__main__":
    vs = VideoServer()