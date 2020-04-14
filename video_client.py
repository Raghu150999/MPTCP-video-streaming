import socket
from util import Util
from constants import *
import threading
import zlib
import numpy as np 
import struct
import subprocess as sp
import os
import argparse
import time

# Helper functions
def get_fileformat(filename):
    for i, ch in enumerate(filename[::-1]):
        if ch == '.':
            return filename[i+1:]

class VideoClient:

    def __init__(self, saddr, caddr, filename):
        # server address
        self.saddr = saddr
        # client address
        self.caddr = caddr

        # control sock
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.csock.bind(caddr)
        self.csock.connect(saddr)
        self.csock.settimeout(1)
        self.running = True

        # data sock
        self.dsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dsock.bind((caddr[0], caddr[1]+1))
        self.dsock.connect(saddr)

        cutil = Util(self.csock)

        # send filename (requested)
        self.filename = filename
        cutil.send(filename)

        # send SETUP request
        self.cutil = cutil
        cutil.send(SETUP)

        # PLAY stream
        cutil.send(PLAY)
        self.playing = True
        self.player = threading.Thread(target=self.play, args=())
        self.player.start()

        while self.running:
            time.sleep(5)
            try:
                # send HEARTBEAT to server to maintain connection
                cutil.send(HEARTBEAT)
                l = self.csock.recv(4)
                l, = struct.unpack('!I', l)
                msg = self.csock.recv(l).decode('ascii')
                if msg == EXIT:
                    self.running = False
                    self.playing = False
                    break
            except socket.timeout as e:
                # No commands received (if timeout)
                continue
            
        self.quit()
        self.csock.close()
    
    def play(self):
        # TODO: handle differnt file formats
        # start ffmpeg decoder
        cmd = ['ffplay', '-i', 'pipe:', '-f', 'mp4']
        # remove output of ffmpeg for clean interface
        devnull = open(os.devnull, 'w')
        proc = sp.Popen(cmd, stdin=sp.PIPE, stderr=devnull)

        # TODO: if connection lost keep max_timeout in util and raise exception if reached
        while self.playing:
            try:
                data = self.dsock.recv(CHUNK)
            except:
                print('Server closed...')
                self.running = False
                break
            if not data:
                print('Stream finished...Press Q to quit')
                self.running = False
                break
            # data = zlib.decompress(data)
            try:
                proc.stdin.write(data)
            except:
                # client closed stream
                self.running = False
                self.playing = False
                print('Exited...')
                break
        self.dsock.close()
        try:
            proc.stdin.close()
            proc.wait()
        except:
            pass

    def quit(self):
        self.cutil.send(EXIT)
        self.playing = False
        self.running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Video streaming client')
    parser.add_argument('--filename', type=str, default='test.mp4', help='video filename to stream')
    parser.add_argument('--ip', type=str, default="", help='IP address of server')
    parser.add_argument('--port', type=int, default=8000, help='port number of server')
    args = parser.parse_args()
    print('Controls:')
    print('p: PAUSE/PLAY')
    print('q: QUIT')
    # TODO: handle invalid filename
    vc = VideoClient(saddr=(args.ip, args.port), caddr=("", 10000), filename=f'public/{args.filename}')
    