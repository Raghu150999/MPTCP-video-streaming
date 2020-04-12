import socket 
import time

CHUNK = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 8000))
sock.listen(2)
sc, addr = sock.accept()

f = open('public/test.mp4', 'rb')
i = 0
while True:
    data = f.read(CHUNK * 10)
    i += 1
    if not data:
        break
    # ffmpeg also handles slow and paused stream
    # if i % 100 == 99:
    #     print('Sleep')
    #     time.sleep(5)
    sc.sendall(data)
    print(f'chunk {i}', end='\r')

sc.close()
sock.close()







