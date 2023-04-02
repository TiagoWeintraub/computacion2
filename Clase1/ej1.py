# Escribir un programa en Python que acepte un número de argumento entero positivo n y genere una lista de los n primeros números impares. El programa debe imprimir la lista resultante en la salida estandar.

import argparse    
import sys

def main():
    parser = argparse.ArgumentParser(description='Generar una lista de n números impares.')

    parser.add_argument('n', type=int, help='Número de elementos a generar')

    args = parser.parse_args()

    if args.n <= 0:
        print("El número de elementos debe ser un entero positivo.")
        sys.exit(1) # para indicar que ha habido un error

    impares = []
    n_impares = 0
    i = 1
    while n_impares < args.n:
        impares.append(i)
        n_impares += 1
        i += 2

    print(impares)

if __name__ == '__main__':
    main()