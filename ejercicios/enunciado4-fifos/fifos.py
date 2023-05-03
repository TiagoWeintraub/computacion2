# FIFOS - COLA - QUEUE
# 1- Escribir un programa que realice la multiplicación de dos matrices de 2x2. Cada producto deberá calcularse en un proceso distinto devolviendo el resultado en una fifo indicando el indice del producto. El padre deberá leer en la fifo y mostrar el resultado final.

import os
import multiprocessing
import sys
import time
import argparse

# Calcular el producto de matrices 2x2

def multiplicacion(matriz1, matriz2, num_proceso, lock, fifo):
    if num_proceso == 1:
        producto = matriz1[0][0] * matriz2[0][0] + matriz1[0][1] * matriz2[1][0]
        fila = 0
        columna = 0
            
    elif num_proceso == 2:
        producto = matriz1[0][0] * matriz2[0][1] + matriz1[0][1] * matriz2[1][1]
        fila = 0
        columna = 1

    elif num_proceso == 3:
        producto = matriz1[1][0] * matriz2[0][0] + matriz1[1][1] * matriz2[1][0]
        fila = 1
        columna = 0
    
    elif num_proceso == 4:
        producto = matriz1[1][0] * matriz2[0][1] + matriz1[1][1] * matriz2[1][1]
        fila = 1
        columna = 1

    with lock:
        fifo.write(f'{fila},{columna},{producto}\n')
        fifo.flush()

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    fifo_path = path + "/fifo1"
    if os.path.exists(fifo_path):
        os.remove(fifo_path)
    os.mkfifo(fifo_path)

    lock = multiprocessing.Lock()
    fifo = open("fifo1", "w")

    matrizA = [[1,2],[3,4]]
    matrizB = [[5,6],[7,8]]
    
    procesos = []
    for i in range(4):
        proceso = multiprocessing.Process(target=multiplicacion, args=(matrizA,matrizB,i+1,lock,fifo))
        proceso.start()
        procesos.append(proceso)

    for proceso in procesos:
        proceso.join()
    
    fifo = open("fifo1", "r")
    resultado = []
    for linea in fifo:
        lista = linea.split(',')
        fila = int(lista[0])
        producto = float(lista[2])
        if len(resultado) <= fila:
            resultado.append([])
        resultado[fila].append(producto)
    print(resultado)
    
    fifo.close()
    os.remove(path + "/fifo1")

    # os.unlink(fifo_path)


































