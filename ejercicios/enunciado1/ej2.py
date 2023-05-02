# Escribir un programa en Python que acepte dos argumentos de línea de comando: una cadena de texto, un número entero. El programa debe imprimir una repetición de la cadena de texto tantas veces como el número entero.

import argparse    
import sys

def main():
    parser = argparse.ArgumentParser(description='Repetición de una cadena de texto')

    # Argumentos
    parser.add_argument('-c', type=str, help='Cadena de texto')
    parser.add_argument('-n', type=int, help='Número de repeticiones')

    args = parser.parse_args()
    
    if args.n <= 0:
        print("El número de repeticiones debe ser un entero positivo.")
        sys.exit(1)

    repe = args.c
    for i in range(args.n-1):
        repe += ' '
        repe += args.c
    
    print(repe)

if __name__ == '__main__':
    main()