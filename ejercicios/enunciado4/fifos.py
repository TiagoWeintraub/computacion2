# FIFOS - COLA - QUEUE
# 1- Escribir un programa que realice la multiplicación de dos matrices de 2x2. Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.

import os
import sys

# Calcular el producto de matrices 2x2
def producto_matrices(matriz1, matriz2):
    resultado = []
    for i in range(2):
        fila = []
        for j in range(2):
            fila.append(matriz1[i][0] * matriz2[0][j] + matriz1[i][1] * matriz2[1][j])
        resultado.append(fila)
    return resultado

# Escribir un elemento en la FIFO
def escribir_en_fifo(fifo, i, j, valor):
    fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
    os.write(fd, f"({i},{j}):{valor}\n".encode())
    os.close(fd)
    print(f"Escribiendo en la FIFO ({i},{j}):{valor}")

# Función para leer los elementos de la FIFO y mostrar el resultado final
def leer_fifo(fifo):
    resultado = []
    with open(fifo, "r") as f:
        for linea in f:
            print(linea.strip())
            i, j = [int(x) for x in linea.split(":")[0][1:-1].split(",")]
            valor = int(linea.split(":")[1])
            resultado.append((i, j, valor))
    resultado_final = [[0, 0], [0, 0]]
    for i, j, valor in resultado:
        resultado_final[i][j] = valor
    print("El resultado final es:")
    for fila in resultado_final:
        print(fila)

if __name__ == "__main__":
    # Definir las matrices
    matriz1 = [[1, 2], [3, 4]]
    matriz2 = [[5, 6], [7, 8]]
# Crear la FIFO
fifo = "resultado.fifo"
if os.path.exists(fifo):
    os.remove(fifo)
os.mkfifo(fifo)

# Crear los procesos para calcular cada elemento de la matriz resultante
procesos = []
for i in range(2):
    for j in range(2):
        pid = os.fork()
        if pid == 0:
            # Proceso hijo
            valor = matriz1[i][0] * matriz2[0][j] + matriz1[i][1] * matriz2[1][j]
            escribir_en_fifo(fifo, i, j, valor)
            sys.exit(0)
        else:
            # Proceso padre
            procesos.append(pid)

# Leer los elementos de la FIFO mientras los procesos hijos están escribiendo en ella
resultado = []
with open(fifo, "r") as f:
    while any(os.waitpid(pid, os.WNOHANG) == (0, 0) for pid in procesos):
        for linea in f:
            print(linea.strip())
            i, j = [int(x) for x in linea.split(":")[0][1:-1].split(",")]
            valor = int(linea.split(":")[1])
            resultado.append((i, j, valor))

# Mostrar el resultado final
resultado_final = [[0, 0], [0, 0]]
for i, j, valor in resultado:
    resultado_final[i][j] = valor
print("El resultado final es:")
for fila in resultado_final:
    print(fila)