import os
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "vector_frames")

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

def run():
   
    handler = partial(CORSHandler, directory=WEB_DIR)
    HTTPServer(("localhost", 8000), handler).serve_forever()

run()