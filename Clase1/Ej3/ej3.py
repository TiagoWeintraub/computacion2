# Escribir un programa en Python que acepte argumentos de línea de comando para leer un archivo de texto. El programa debe contar el número de palabras y líneas del archivo e imprimirlas en la salida estándar. Además el programa debe aceptar una opción para imprimir la longitud promedio de las palabras del archivo. Esta última opción no debe ser obligatoria. Si hubiese errores deben guardarse el un archivo cuyo nombre será "errors.log" usando la redirección de la salida de error.

import argparse    
import sys

def main():

    parser = argparse.ArgumentParser(description='Repetición de una cadena de texto')

    # Argumentos
    parser.add_argument('-nombreArchivo', type=str, help='Cadena de texto')

    args = parser.parse_args()

    nombre_arch = args.nombreArchivo + '.txt'

    try:
        with open(nombre_arch, 'r') as archivo:
            lineas = archivo.readlines()
            unir = " ".join(lineas) 
            palabras = unir.strip().split(" ")
            cant_lineas = len(lineas)

            long = 0

            while "" in palabras:
                palabras.remove("")

            contador = 0
            for palabra in palabras:
                palabra_s = palabra.strip()
                longitud = len(palabra_s)
                # print(palabra_s)

                long += longitud
                contador += 1

            promedio = round(long)/len(palabras)
            # print(palabras)

        print(f'Cantidad de líneas: {cant_lineas}')
        print(f'Cantidad de palabras del archivo: {len(palabras)}')
        print(f'Promedio de la longitud de las palabras del archivo: {promedio}')
    except:
        print("\nHa ocurrido un error, revise el archivo 'errors.log' si quiere conocer acerca del error")
        with open("errors.log", "a") as errores: #"a" significa append, guarda un error por línea
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errores.write(f"Se produjo un error de tipo {exc_type.__name__}: {exc_value}\n")


if __name__ == '__main__':
    main()