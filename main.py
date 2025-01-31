import http.server
import urllib.parse
import os

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        room = query_params.get('room', [None])[0]

        if parsed_path.path == '/get-image' and room:
            file_path = f"images/{room}.jpg"

            if os.path.exists(file_path):
                # Respond with the image
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                self.end_headers()
                with open(file_path, "rb") as image_file:
                    self.wfile.write(image_file.read())
            else:
                # Respond with 404 if the image is not found
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                self.end_headers()
                self.wfile.write(b"Image not found")
        else:
            # Respond with 400 for invalid requests
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
            self.end_headers()
            self.wfile.write(b"Bad Request")

if __name__ == "__main__":
    server_address = ('', 48497)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    print("Server running on http://0.0.0.0:48497")
    httpd.serve_forever()
