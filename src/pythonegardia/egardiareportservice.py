import http.server
import socketserver
import cgi
import urllib

port = 85

class Handler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>GET!</h1></body></html>")
        return
    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        content_length=int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("POST RECEIVED")
        print(post_data)
        self._set_headers()
        self.wfile.write("<html><body><h1><POST!</h1></body></html>")
        return
    def parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile,pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length),keep_blank_values=1)
        else:
            postvars = {}
        return postvars

print('Server listening on port 85...')
httpd = socketserver.TCPServer(('',port),Handler)
httpd.serve_forever()


