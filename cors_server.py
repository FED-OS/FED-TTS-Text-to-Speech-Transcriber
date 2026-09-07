import http.server
import os
import socketserver


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    os.chdir("/workspace/tests_media")
    with socketserver.TCPServer(("0.0.0.0", 8000), CORSHandler) as httpd:
        print("CORS file server on :8000")
        httpd.serve_forever()
