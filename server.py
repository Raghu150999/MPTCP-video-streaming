import socket

MPTCP_ENABLED = 42

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# when net.mptcp.mptcp_enabled = 2, both client and server should enable MPTCP socket option for using MPTCP

# Enable MPTCP
sock.setsockopt(socket.SOL_TCP, MPTCP_ENABLED, 1)

# MPTCP not working on localhost for some reason?
sock.bind(('192.168.0.108', 8000))
sock.listen(1)

while True:
    sc, address = sock.accept()
    print('Client', address)
    # if 1, implies connection is MPTCP
    print(sc.getsockopt(socket.SOL_TCP, MPTCP_ENABLED))
    print(sc.recv(65535).decode('ascii'))
    print(sc.recv(65535).decode('ascii'))
    print(sc.recv(65535).decode('ascii'))
    sc.close()
