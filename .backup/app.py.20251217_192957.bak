from http.server import HTTPServer, BaseHTTPRequestHandler
import handlers

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            handlers.handle_root(self)
        else:
            self.send_error(404, 'File not found')

if __name__ == '__main__':
    from config import HOST, PORT
    httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print(f'Serving on {HOST}:{PORT}...')
    httpd.serve_forever()
