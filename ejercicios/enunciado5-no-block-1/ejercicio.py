# 1 - Considerando el programa noblock.py, realizar un programa que lance dos procesos hijos que intenten encontrar 
# el nonce para un No-Bloque con una dificultad dada. El hijo que lo encuentre primero debe comunicarse con el padre
# mediante una señal guardando el nonce (number used once) en una fifo para que el padre pueda leerla. 

# Hacer otra versión pero utilizando pipes.

import os
import signal
from noblock import NoBlock, proof_of_work

path = os.path.dirname(os.path.abspath(__file__))
fifo_path = path + "/fifo1"
if os.path.exists(fifo_path):
    os.remove(fifo_path)
os.mkfifo(fifo_path)

def hijo(seed):
    block = NoBlock(seed=seed, nonce=0)
    new_hash = proof_of_work(block)

    with open(fifo_path, 'w') as fifo:
        fifo.write(str(block.nonce))

    os.kill(os.getppid(), signal.SIGUSR1)


def manejo_de_señal(signum, frame):

    with open(fifo_path, 'r') as fifo:
        nonce = fifo.read()

    print("Nonce encontrado:", nonce)

    os.remove(fifo_path)
    exit(0)

signal.signal(signal.SIGUSR1, manejo_de_señal)

for i in range(2):
    pid = os.fork()
    if pid == 0:
        seed = f'Semilla {i+1}'
        hijo(seed)
        exit(0)

signal.pause()
os.remove(fifo_path)