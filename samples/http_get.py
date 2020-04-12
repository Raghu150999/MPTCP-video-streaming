import socket

MPTCP_ENABLED = 42

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Need to enable manually if net.mptcp.mptcp_enabled = 2
# sock.setsockopt(socket.SOL_TCP, MPTCP_ENABLED, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(sock.getsockopt(socket.SOL_TCP, MPTCP_ENABLED))
url = 'amiusingmptcp.de'
# url = 'multipath-tcp.org'
address = (socket.gethostbyname(url), 80)
sock.connect(address)
# Used to check if MPTCP is working for the given website
print(sock.getsockopt(socket.SOL_TCP, MPTCP_ENABLED))
exit(0)

req = \
    "GET / HTTP/1.1\r\n" + \
    "host: {}\r\n".format(url) + \
    "connection: close\r\n" + \
    "accept: text/html\r\n" + \
    "\r\n"

req = req.encode('utf-8')
sock.sendall(req)

data = b''
sz = 0
while True:
    reply = sock.recv(65535)
    if not reply:
        break
    data = data + reply
    reply = reply.decode('utf-8', 'ignore')
    # sz += len(reply)
    # print('\rReceived {} bytes'.format(sz), end='')

print(data.decode('utf-8', 'ignore'))

