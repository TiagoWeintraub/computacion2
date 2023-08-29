"""
1 - Escribir un programa que reciba un mensaje desde otro proceso usando fifo (pipes con nombre). 
El proceso receptor deberá lanzar tantos hilos como líneas tenga el mensaje y deberá enviar cada línea a los hilos secundarios. 
Cada hilo secundario deberá calcular la cantidad de caracteres de su línea y COMPROBAR la cuenta de la línea anterior."""

import multiprocessing as mp
import os
import sys

def contar_caracteres(línea, conteo_anterior):
    conteo = len(línea)

    if conteo_anterior is not None and conteo != conteo_anterior + 1:
        print("La longitud de la línea {} no es correcta: {} (esperado: {})".format(
            línea, conteo, conteo_anterior + 1))
        sys.exit(1)

    return conteo

def main():
    fifo = os.open("fifo", os.O_RDONLY)

    pool = mp.Pool()

    conteo_anterior = None

    while True:
        línea = os.read(fifo, 1024)
        if línea == b"":
            break

        conteo = pool.apply_async(contar_caracteres, args=(línea, conteo_anterior))

        conteo_anterior = conteo.get()

    os.close(fifo)

if __name__ == "__main__":
    main()

