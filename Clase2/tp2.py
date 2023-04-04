# Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar relizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.

import os
import argparse
import math

def fork():
    
    parser = argparse.ArgumentParser(description='Creamos el objeto')

    # Argumentos     # -n es para consola y --numero para código: ej python3 tp2.py -n 16 -f
    parser.add_argument('-n', '--numero',type=float, help='Número a sacar la raíz')
    parser.add_argument('-f', '--fork', action='store_true', help='Hace el fork') #El valor del fork es true

    args = parser.parse_args()
    
    if args.fork: #Se cumple porque el action = true 
        pid = os.fork()

        if args.numero == 0:
            return 0

        elif pid == 0:
            if args.numero < 0:
                resultado = str(round(-math.sqrt(-1*args.numero),2)) + 'i'
            else: 
                resultado = round(-math.sqrt(args.numero),2)
            return resultado

        else:
            if args.numero < 0:
                resultado = str(round(math.sqrt(-1*args.numero),2)) + 'i'
            else: 
                resultado = round(math.sqrt(args.numero),2)
            return resultado

if __name__ == '__main__':
    print(fork())