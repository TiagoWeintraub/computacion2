import os
import signal
from noblock import NoBlock, proof_of_work

path = os.path.dirname(os.path.abspath(__file__))
fifo_path = path + "/fifo1"
if os.path.exists(fifo_path):
    os.remove(fifo_path)
os.mkfifo(fifo_path)

def hijo(seed, fifo_path):
    block = NoBlock(seed=seed, nonce=0)
    new_hash = proof_of_work(block)

    with open(fifo_path, 'w') as fifo:
        fifo.write(str(block.nonce))

    os.kill(os.getppid(), signal.SIGUSR1)


def manejo_de_señal(signum, frame, fifo_path):
    with open(fifo_path, 'r') as fifo:
        nonce = fifo.read()

    print("Nonce encontrado:", nonce)

    os.remove(fifo_path)
    exit(0)

signal.signal(signal.SIGUSR1, lambda signum, frame: manejo_de_señal(signum, frame, fifo_path))

for i in range(2):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        fifo_path_child = path + "/fifo_child_" + str(i)
        os.mkfifo(fifo_path_child)
        w = os.fdopen(w, 'w')
        w.write(fifo_path_child)
        w.close()
        fifo_child = os.open(fifo_path_child, os.O_RDONLY)
        fifo_path = os.read(fifo_child, 1024).decode().strip()
        os.close(fifo_child)
        seed = f'Semilla {i+1}'
        hijo(seed, fifo_path)
        exit(0)
    else:
        os.close(w)
        r = os.fdopen(r, 'r')
        fifo_path_child = r.read().strip()
        r.close()
        fifo_child = os.open(fifo_path_child, os.O_WRONLY)
        os.write(fifo_child, fifo_path.encode())
        os.close(fifo_child)

signal.pause()
os.remove(fifo_path)
