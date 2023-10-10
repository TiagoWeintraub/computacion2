"""## EJERCICIOS ##
1 - Implementar un servidor http con el módulo http.server que sirva diferentes páginas utilizando como base el código analizado en clase.
2- Utilizar links para navegar entre las distintas páginas."""

import http.server
import socketserver


PORT = 1111


class handler_manual (http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.server_version = "Simple HTTP Server (Python)"

    def do_GET(self):
        print("REQUEST: ", self.requestline)
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open('ejercicio17/index.html', 'rb') as file:
                self.wfile.write(file.read())
            self.wfile.write(b'<p>Bienvenido al servidor HTTP simple.</p>')
        elif self.path == '/page1.html':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open('ejercicio17/page1.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/page2.html':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open('ejercicio17/page2.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1>')



socketserver.TCPServer.allow_reuse_address = True

myhttphandler = handler_manual

httpd = http.server.HTTPServer(("", PORT), myhttphandler)

print(f"Opening httpd server at port {PORT}")

httpd.serve_forever()

httpd.shutdown()
