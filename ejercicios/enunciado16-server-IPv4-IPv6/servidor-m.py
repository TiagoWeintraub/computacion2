#Con multiprocessing

import socket
import multiprocessing

HOST = "::"  # Esto escuchará en todas las interfaces IPv6 disponibles
PORT = 9999

def manejar_cliente(cliente):
    while True:
        datos = cliente.recv(1024)
        if datos == b"exit":
            break
        cliente.sendall(datos.upper())
    cliente.close()

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escuchando en [{HOST}]:{PORT} (IPv6/IPv4)")
    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión establecida con {direccion}")
        proceso = multiprocessing.Process(target=manejar_cliente, args=(cliente,))
        proceso.start()

