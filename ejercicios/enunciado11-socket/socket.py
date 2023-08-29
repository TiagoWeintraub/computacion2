"""
Escribir un programa que implemente un socket pasivo que gestione de forma serializada distintas conecciones entrantes.

Debe atender nuevas conexiones de forma indefinida.

NOTA: cuando decimos serializado decimo que atiende una conexión y recibe una nueva conección una vez que esa conexión se cerró
"""

import socket

def manejar_conexion(socket):
    datos = socket.recv(1024)
    print(datos.decode())
    socket.close()

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)

    while True:
        cliente, _ = server_socket.accept()

        manejar_conexion(cliente) # No usamos threads

if __name__ == "__main__":
    main()

