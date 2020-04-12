#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
 
 
class StaticServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
        root = './public'
        if self.path == '/':
            filename = root + '/index.html'
        else:
            filename = root + self.path
 
        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.mp4':
            self.send_header('Content-type', 'video/mp4')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        if not os.path.isfile(filename):
            self.wfile.write(b'File Not Found!')
        else:
            with open(filename, 'rb') as fh:
                data = fh.read()
                print(len(data))
                self.wfile.write(data)
 
def run(server_class=HTTPServer, handler_class=StaticServer, port=8000):
    server_address = ('192.168.0.108', port)
    httpd = server_class(server_address, handler_class)
    print('Starting http server on {}'.format(server_address))
    httpd.serve_forever()
 
run()