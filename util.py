import struct
import socket

class Util:
    '''
    Helper functions for socket operations
    '''

    def __init__(self, sock):
        self.sock = sock

    def recvall(self, length):
        data = b''
        rem = length
        while rem > 0:
            try:
                new_data = self.sock.recv(rem)
                if not new_data:
                    raise Exception('peer closed')
                data += new_data
            except socket.timeout as e:
                # TODO: handle several timeouts (probably lost connection)
                pass
            rem = length - len(data)
        return data
    
    def recv(self):
        l = self.recvall(4)
        l, = struct.unpack('!I', l)
        data = self.recvall(l)
        return data
    
    def send(self, data):
        if type(data) == str:
            data = data.encode('ascii')
        l = len(data)
        l = struct.pack('!I', l)
        databytes = l
        databytes += data
        self.sock.sendall(databytes)