# 1 - Considerando el programa noblock.py, realizar un programa que lance 10 procesos hijos que intenten encontrar
# el nonce para un No-Bloque con una dificultad dada. El hijo que lo encuentre primero debe comunicarse con el padre.

# Realizar todo utilizando multiprocessing

import multiprocessing
import time
import hashlib

def noblock(diff):
    nonce = 0
    while not is_valid_hash(nonce, diff):
        nonce += 1
        return nonce

def is_valid_hash(nonce, diff):
    
    hash = hashlib.sha256(str(nonce).encode()).hexdigest()
    return hash.startswith("0" * diff)

def main():

    diff = 5
    procesos = []
    for i in range(10):
        proceso = multiprocessing.Process(target=noblock, args=(diff,))
        procesos.append(proceso)
        proceso.start()

    found = False
    nonce = None
    for proceso in procesos:
        proceso.join()
        if not found:
            if proceso.is_alive():
                continue
            found = True
            nonce = proceso.exitcode

    if found:
        print(f"El nonce encontrado es: {nonce}")
    else:
        print("No se ha encontrado el nonce")

if __name__ == "__main__":
    main()




