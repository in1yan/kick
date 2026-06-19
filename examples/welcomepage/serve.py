import http.server
import socketserver
import os

PORT = 8000

# Change directory to the folder containing the site files (assumes this script is in the project root)
web_dir = os.path.abspath('.')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
