"""
Memoria Compartida

Etapa 1

Escribir un programa que reciba por argumento la opción -f acompañada de un path_file

El programa deberá crear un segmento de memoria compartida y generar dos hijos H1 y H2.

H1 deberá leer desde sdtin lo que ingrese el usuario, línea por línea, enviando una señal USR1 al padre en cada línea leida.

Una vez ingresada una línea, el proceso padre leerá la memoria compartida y mostrará la línea leida por pantalla y enviará una señal USR1 a H2.

Al recibir la señal USR1, H2 leerá la línea desde la memoria compartida y la escribirá en mayúsculas en el archivo recibido como argumento.

Etapa 2
Cuando el usuario introduzca "bye" en la terminal, H1 enviará al padre la señal USR2 y terminará.

Al recibir la señal USR2, el padre, la enviará a H2 que también terminará.

El padre esperará a ambos hijos y terminará también.
"""
import os
import sys
import mmap
import signal
import multiprocessing as mp

def h1_handler(signum, frame):
    if signum == signal.SIGUSR1:
        line = sys.stdin.readline().rstrip('\n')
        os.kill(os.getppid(), signal.SIGUSR1)
        if line == "bye":
            os.kill(os.getpid(), signal.SIGUSR2)

def h2_handler(signum, frame):
    if signum == signal.SIGUSR1:
        with mmap.mmap(fd, 0) as mm:
            line = mm.readline().decode().rstrip('\n')
            mm.seek(0)
            mm.write(line.upper().encode())
        os.kill(os.getppid(), signal.SIGUSR2)

def parent_handler(signum, frame):
    if signum == signal.SIGUSR1:
        with mmap.mmap(fd, 0) as mm:
            line = mm.readline().decode().rstrip('\n')
            print(f"Line received: {line}")
        os.kill(h2_pid, signal.SIGUSR1)
    elif signum == signal.SIGUSR2:
        os.kill(h2_pid, signal.SIGUSR2)
        os.waitpid(h1_pid, 0)
        os.waitpid(h2_pid, 0)
        os.close(fd)
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != '-f':
        print("Usage: python programa.py -f <path_file>")
        sys.exit(1)

    path_file = sys.argv[2]
    fd = os.open(path_file, os.O_RDWR | os.O_CREAT)
    os.write(fd, b'\0')

    h1_pid = os.fork()
    if h1_pid == 0:
        signal.signal(signal.SIGUSR1, h1_handler)
        signal.pause()
        sys.exit(0)

    h2_pid = os.fork()
    if h2_pid == 0:
        signal.signal(signal.SIGUSR1, h2_handler)
        signal.pause()
        sys.exit(0)

    signal.signal(signal.SIGUSR1, parent_handler)
    signal.signal(signal.SIGUSR2, parent_handler)

    os.waitpid(h1_pid, 0)
    os.waitpid(h2_pid, 0)
    os.close(fd)
    sys.exit(0)
