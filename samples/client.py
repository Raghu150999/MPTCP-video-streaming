import socket

MPTCP_ENABLED = 42

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_TCP, MPTCP_ENABLED, 1)

# Binding on localhost doesn't enable (?), use some other interface.
address = ('192.168.0.108', 0)
sock.bind(address)

# sock.connect(('127.0.0.1', 8000))
sock.connect(('192.168.0.108', 8000))
print('Connected')

# If 1, implies connection is MPTCP enabled
print('MPTCP enabled:', sock.getsockopt(socket.SOL_TCP, MPTCP_ENABLED))

msg = 'Hi'
block = ""
for i in range(1000):
    block += msg
sock.sendall(block.encode('ascii'))
sock.sendall(block.encode('ascii'))
sock.sendall(block.encode('ascii'))

# msg = sock.recv(65535).decode('ascii')
# print(msg)
sock.close()