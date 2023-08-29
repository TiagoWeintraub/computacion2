"""
2 - Realizar dos versiones de un servidor de mayúsculas que atienda múltiples clientes de forma concurrente utilizando multiprocessing y threading utilizando sockets TCP.

El hilo/proceso hijo debe responder con mayúsculas hasta que el cliente envíe la palabra exit. 

En caso de exit el cliente debe administrar correctamente el cierre de la conexión y del proceso/hilo.
"""

import socket
import threading

HOST = "localhost"
PORT = 9999

def manejar_cliente(cliente):
    while True:
        datos = cliente.recv(1024)
        if datos == b"exit":
            break
        cliente.sendall(datos.upper())
    cliente.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión establecida con {direccion}")
        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()
