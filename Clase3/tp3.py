# PIPES

# 1- Escribir un programa en Python que comunique dos procesos. El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, contar la cantidad de palabras que contiene y mostrar ese número.

# 2- Verificar si es posible que dos procesos hijos (o nieto) lean el PIPE del padre.

"""" Si es posible que dos procesos hijos (o nieto) lean el PIPE del padre, ya que el PIPE es un objeto que se crea en el espacio de memoria del proceso padre, y los hijos heredan ese espacio de memoria, por lo tanto, los hijos pueden acceder al PIPE del padre """

# 3- Verificar si el PIPE sigue existiendo cuendo el padre muere (termina el proceso), cuando el hijo muere [o cuendo mueren ambos]
# $ ls -l /proc/[pid]/fd/

"""" El Pipe se cierra cuando el padre muere, y si el hijo muere antes que el padre también se cierra el Pipe,
si ambos mueren al mismo tiempo el Pipe no existirá más.
"""

import os
import argparse
import multiprocessing

class Programa():
    
    def __init__(self):
        parser = argparse.ArgumentParser(description='Creamos el objeto')

        parser.add_argument('-a', '--archivo', type=str, help='Archivo que se va a leer')

        self.args = parser.parse_args()

    def leer_archivo(self, conn):
        with open(self.args.archivo, 'r') as f:
            for linea in f:
                conn.send(linea)
            print(os.getpid())
            conn.send('Terminar')

    def contar_palabras(self, conn):

        n_linea = 0

        while True:
            linea = conn.recv()
            if linea == 'Terminar':
                break
            else: 
                n_linea += 1
            palabras = linea.split()
            palabras_no_vacias = []
            for palabra in palabras:
                if palabra != '':
                    palabras_no_vacias.append(palabra)
            print(f'La cantidad de palabras de la línea {n_linea} es {len(palabras_no_vacias)}')
        conn.close()

if __name__ == "__main__":
    con_padre, con_hijo = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target=Programa().leer_archivo, args=(con_hijo,)) #El proceso padre hace conexión con el hijo
    p2 = multiprocessing.Process(target=Programa().contar_palabras, args=(con_padre,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()


