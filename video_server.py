import socket
import numpy as np 
import struct
import time
import threading
from util import Util
from video_stream import VideoStream
from constants import *
import argparse

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
        # try to send EXIT cmd
        try:
            self.cutil.send(EXIT)
        except:
            # error if client closed
            pass
        self.sock.close()
        # if stream is live, quit stream
        if self.streaming:
            self.streaming = False
            self.streamer.join()
        if self.data_sock:
            self.data_sock.close()
    
    # control socket
    def handle(self):
        util = Util(self.sock)
        self.cutil = util

        # get video filename
        # TODO: handle unknow filename
        filename = util.recv().decode('ascii')

        cmd = util.recv().decode('ascii')
        if cmd != SETUP:
            self.terminate()
            return

        util.send(OK)

        # Start video capture
        self.vs = VideoStream(filename)
        
        while True:
            cmd = util.recv().decode('ascii')
            if cmd == EXIT:
                self.terminate()
                return
            elif cmd == PLAY:
                self.streamer = threading.Thread(target=self.start_streaming, args=())
                self.streamer.start()
            elif cmd == HEARTBEAT:
                # TODO: handle if no HEARTBEAT received for long
                pass
            if self.completed:
                self.terminate()
                return
    
    # data socket
    def start_streaming(self):
        self.streaming = True
        print('Started streaming...', self.addr)
        while self.streaming:
            data = self.vs.read()
            if data == None:
                print("Finished streaming...", self.addr)
                self.streaming = False
                break
            try:
                self.data_sock.sendall(data)
            except Exception as e:
                print('Client closed...')
                self.streaming = False
                self.completed = True
                break
            self.fnbr += 1
            print(f'Sent frame {self.fnbr}', end='\r')
        self.data_sock.close()

    def attach_data_sock(self, sock):
        self.data_sock = sock

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Video streaming client')
    parser.add_argument('--ip', type=str, default="", help='IP address of server')
    parser.add_argument('--port', type=int, default=8000, help='port number of server')
    args = parser.parse_args()
    vs = VideoServer(addr=(args.ip, args.port))