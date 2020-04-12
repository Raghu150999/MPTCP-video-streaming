import os
import socket
import subprocess as sp

CHUNK = 1024
cmd = ['ffplay', '-i', 'pipe:', '-f', 'mp4']
# remove output of ffmpeg for clean interface
devnull = open(os.devnull, 'w')
proc = sp.Popen(cmd, stdin=sp.PIPE, stderr=devnull)

sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("", 8000))
while True:
    data = sock.recv(CHUNK * 10)
    if not data:
        print('Finished...')
        break
    proc.stdin.write(data)

sock.close()
proc.stdin.close()
proc.wait()