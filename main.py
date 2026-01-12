import http.server
import urllib.parse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def getAllValidLocationNames():
    locations = {"IST": [], "BARC": []}

    locations["IST"] = sorted(os.listdir(os.path.join(IMAGES_DIR, "IST")))
    locations["BARC"] = sorted(os.listdir(os.path.join(IMAGES_DIR, "BARC")))

    return locations

# Create Dictionary of valid locations and their rooms
validLocationNames = getAllValidLocationNames()

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        room = query_params.get('room', [None])[0]
        moveDirection = query_params.get('direction', [None])[0]

        if parsed_path.path == '/get-image' and room:
            building = room.split('-')[0]
            file_path = os.path.join(IMAGES_DIR, building, f"{room}.JPG")


            # direction is valid and given
            if moveDirection is not None:
                try:
                    currentPhotoIndex = validLocationNames[building].index(room+".JPG")
                except ValueError:
                    # Respond with 400 for invalid requests
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                    self.end_headers()
                    self.wfile.write(b"Bad Request")
                    return

                # Set to current index until new index is found
                targetPhotoIndex = currentPhotoIndex
                if moveDirection == "next":
                    targetPhotoIndex = currentPhotoIndex + 1
                    if len(validLocationNames[building]) == targetPhotoIndex:
                        targetPhotoIndex = 0
                elif moveDirection == "previous":
                    targetPhotoIndex = currentPhotoIndex - 1
                    if -1 == targetPhotoIndex:
                        targetPhotoIndex = len(validLocationNames[building]) - 1
                else:
                    # Respond with 400 for invalid requests
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                    self.end_headers()
                    self.wfile.write(b"Bad Request")
                    return
                targetPhotoFileName = validLocationNames[building][targetPhotoIndex]
                file_path = os.path.join(IMAGES_DIR, building, targetPhotoFileName)

            if os.path.exists(file_path):
                filename = os.path.basename(file_path)  # Extract filename (e.g., "IST-1002.JPG")

                # Respond with the image
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                self.send_header("Access-Control-Expose-Headers","X-Image-Filename")  # Allow browser to read this header
                self.send_header("X-Image-Filename", filename)  # Send filename in response header
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
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    print("Server running on http://0.0.0.0:8080")
    httpd.serve_forever()
