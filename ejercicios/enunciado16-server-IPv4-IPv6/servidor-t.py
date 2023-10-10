#Con threadings

import socketserver

class manejar_cliente(socketserver.BaseRequestHandler):
    def manejar(self):
        while True:
            data = self.request.recv(1024)
            if data == b"exit":
                break
            self.request.sendall(data.upper())
        self.request.close()

if __name__ == "__main__":
    HOST = "::"  # Esto escuchará en todas las interfaces IPv6 disponibles y también admitirá IPv4

    PORT = 9999

    with socketserver.ThreadingTCPServer((HOST, PORT), manejar_cliente) as server:
        print(f"Servidor escuchando en [{HOST}]:{PORT} (IPv6/IPv4)")
        server.serve_forever()

