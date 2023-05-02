import os
import sys
import argparse

def invertir_linea(linea):
    return ''.join(reversed(linea))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="nombre del archivo")
    args = parser.parse_args()

    try:
        with open(args.file + '.txt', 'r') as archivo:
            lineas = archivo.readlines()
    except Exception:
        print('No se ha encontrado el archivo')
        sys.exit(1)

    try:
        with open("invertido_sin_multiprocessing.txt", "w") as arc_salida:
            for linea in lineas:
                linea = linea.strip()
                lectura, escritura = os.pipe()
                pid = os.fork()
                if pid == 0:# Proceso hijo
                    os.close(escritura)
                    linea_leida = os.read(lectura, 1024).decode().strip()
                    os.close(lectura)
                    linea_invertida = invertir_linea(linea_leida)
                    arc_salida.write(linea_invertida + '\n')
                    sys.exit(0)
                else: # Proceso padre
                    os.close(lectura)
                    os.write(escritura, linea.encode())
                    os.close(escritura)
                    os.waitpid(pid, 0)
    except KeyboardInterrupt:
        print('Finalizado por el usuario')
    except Exception as e:
        print('Ha ocurrido un error:', e.__class__.__name__)
