# Computación II: Concurrency and IPC in Python

Exercises and assignments on processes, IPC, signals, threads and network servers using Python's standard library.  
Ejercicios y trabajos prácticos sobre procesos, IPC, señales, hilos y servidores de red con la biblioteca estándar de Python.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![POSIX](https://img.shields.io/badge/OS-POSIX-555555?style=flat-square)
![Pillow](https://img.shields.io/badge/Pillow-TP2-555555?style=flat-square)

[English](#english) · [Español](#español)

## English

### About

Coursework for the university course *Computación II* (2023): sixteen exercise sets in `ejercicios/` plus two graded assignments (`tp1/`, `tp2/`). Everything runs on the standard library except TP2, which uses Pillow. `os.fork`, `os.mkfifo` and `SIGUSR1/2` need a POSIX system (Linux or macOS).

### Exercise index

| Folder | Topic | What it does |
|---|---|---|
| [enunciado1](ejercicios/enunciado1) | CLI args (`argparse`) | First *n* odd numbers; repeat a string *n* times; count lines, words and average word length of a file, logging errors to `errors.log` |
| [enunciado2-fork](ejercicios/enunciado2-fork) | `os.fork` | With `-f` it forks: the parent computes the positive square root of `-n`, the child the negative one |
| [enunciado3-pipes](ejercicios/enunciado3-pipes) | Pipes | One process sends each line of `-a <file>` through a `multiprocessing.Pipe`, the other counts its words |
| [enunciado4-fifos](ejercicios/enunciado4-fifos) | FIFOs (`os.mkfifo`) | 2×2 matrix product with one process per cell; results go through a FIFO (guarded by a `Lock`) and the parent assembles the matrix |
| [enunciado5-no-block-1](ejercicios/enunciado5-no-block-1) | Signals + FIFO / pipes | Two forked children search a SHA-256 proof-of-work nonce (`noblock.py`); the first writes it to a FIFO and sends `SIGUSR1` to the parent. `ej_pipes.py` adds `os.pipe` |
| [enunciado6-memoria-compartida](ejercicios/enunciado6-memoria-compartida) | Shared memory (`mmap`) + signals | Parent and two children share an `mmap` over the `-f` file, coordinated with `SIGUSR1`/`SIGUSR2`: stdin line, parent prints it, a child writes it uppercased; `bye` ends |
| [enunciado7-no-block-2](ejercicios/enunciado7-no-block-2) | `multiprocessing.Process` | 10 processes search a SHA-256 nonce with difficulty 5 and the parent reports the result |
| [enunciado8-Pool](ejercicios/enunciado8-Pool) | `multiprocessing.Pool` | Primality of 2–100 with `Pool.map`, default pool vs. `cpu_count()` workers |
| [enunciado9-Threading](ejercicios/enunciado9-Threading) | `threading` + `queue` | One thread reads stdin, another ROT13-encodes it; data moves through two queues |
| [enunciado10-pipes-con-nombre](ejercicios/enunciado10-pipes-con-nombre) | Named pipe + `Pool` | Reads from a FIFO named `fifo` and checks each line's length against the previous one with `apply_async` |
| [enunciado11-socket](ejercicios/enunciado11-socket) | Passive TCP socket | Serial server on `localhost:8080`: one connection at a time, prints what it receives |
| [enunciado12-servidor](ejercicios/enunciado12-servidor) | Concurrent TCP servers | Uppercase server on `localhost:9999` in a `multiprocessing` and a `threading` version; `exit` closes the connection |
| [enunciado13-TCP-UDP-socketserver](ejercicios/enunciado13-TCP-UDP-socketserver) | `socketserver` | Threaded TCP uppercase server (`ThreadingMixIn`) on `0.0.0.0:30051`, stopped with Enter |
| [enunciado14-server-http](ejercicios/enunciado14-server-http) | `http.server` | Custom `BaseHTTPRequestHandler` on port 1111 serving an index and two linked pages, 404 otherwise |
| [enunciado15-concurrent.futures](ejercicios/enunciado15-concurrent.futures) | `ProcessPoolExecutor` | Tests every number up to the input in parallel and prints the largest prime ≤ the input |
| [enunciado16-server-IPv4-IPv6](ejercicios/enunciado16-server-IPv4-IPv6) | IPv4/IPv6 | Exercise 12 server bound to `::` (`AF_INET6`) with `multiprocessing`, plus a `socketserver.ThreadingTCPServer` version |

### Assignments

- **[TP1](tp1/CONSIGNA.md): line reverser.** Reads the text file given with `-f` and creates one child process per line. Each line goes to its child through a pipe and the child reverses it. `tp1_sin_multip.py` uses `os.fork` + `os.pipe` and writes the result to `invertido_sin_multiprocessing.txt`; `tp1_multip.py` (bonus) uses `multiprocessing.Process` + `Pipe`, sends the reversed line back to the parent and writes `info_invertida.txt`. A sample `texto.txt` and both outputs are included.
- **[TP2](tp2/enunciado_TP2.md): image processing over HTTP.** A `ThreadingTCPServer` with a `SimpleHTTPRequestHandler` subclass. `GET /<image>` returns the image in grayscale (`-e` not given) or resized by the `-e` factor, saved as `gris_<name>` or `escalada_<name>`. Pillow does the processing inside the request handler. The script also starts a `multiprocessing.Process` fed by a `multiprocessing.Queue` and a thread synchronized with a `Lock` and an `Event`, aimed at the assignment's IPC and synchronization requirements. A sample `imagen.jpeg` is included.

### Running

```bash
# from the repo root
python3 ejercicios/enunciado1/ej1.py 5
python3 ejercicios/enunciado1/ej2.py -c hola -n 3
python3 ejercicios/enunciado3-pipes/tp3.py -a ejercicios/enunciado3-pipes/archivo.txt
(cd tp1 && python3 tp1_sin_multip.py -f texto)   # file name without .txt

pip install pillow
cd tp2 && python3 tp2.py -i 127.0.0.1 -p 8080 -e 0.5   # omit -e for grayscale
# from another terminal
curl -X GET "http://127.0.0.1:8080/imagen.jpeg" --output imagen_procesada.jpeg
```

The servers listen on the host and port hard-coded in each file (see the table). Some files are named after standard-library modules (`socket.py`, `threading.py`, `multiprocessing.py`). Run from their own folder, they shadow the real module, so rename them first.

### Author

Tiago Weintraub · [github.com/TiagoWeintraub](https://github.com/TiagoWeintraub)

## Español

### Sobre el proyecto

Trabajos de la materia universitaria *Computación II* (2023): dieciséis enunciados en `ejercicios/` y dos trabajos prácticos (`tp1/`, `tp2/`). Todo usa la biblioteca estándar salvo el TP2, que usa Pillow. `os.fork`, `os.mkfifo` y `SIGUSR1/2` requieren un sistema POSIX (Linux o macOS).

### Índice de ejercicios

| Carpeta | Tema | Qué hace |
|---|---|---|
| [enunciado1](ejercicios/enunciado1) | Argumentos CLI (`argparse`) | Primeros *n* impares; repetir un texto *n* veces; contar líneas, palabras y longitud promedio de palabra de un archivo, con errores en `errors.log` |
| [enunciado2-fork](ejercicios/enunciado2-fork) | `os.fork` | Con `-f` hace fork: el padre calcula la raíz cuadrada positiva de `-n` y el hijo la negativa |
| [enunciado3-pipes](ejercicios/enunciado3-pipes) | Pipes | Un proceso envía cada línea de `-a <archivo>` por un `multiprocessing.Pipe` y el otro cuenta sus palabras |
| [enunciado4-fifos](ejercicios/enunciado4-fifos) | FIFOs (`os.mkfifo`) | Producto de matrices 2×2 con un proceso por celda; los resultados pasan por una FIFO (protegida con un `Lock`) y el padre arma la matriz |
| [enunciado5-no-block-1](ejercicios/enunciado5-no-block-1) | Señales + FIFO / pipes | Dos hijos buscan un nonce de prueba de trabajo SHA-256 (`noblock.py`); el primero lo escribe en una FIFO y envía `SIGUSR1` al padre. `ej_pipes.py` suma `os.pipe` |
| [enunciado6-memoria-compartida](ejercicios/enunciado6-memoria-compartida) | Memoria compartida (`mmap`) + señales | Padre y dos hijos comparten un `mmap` sobre el archivo de `-f`, coordinados con `SIGUSR1`/`SIGUSR2`: línea de stdin, el padre la muestra, un hijo la escribe en mayúsculas; `bye` termina |
| [enunciado7-no-block-2](ejercicios/enunciado7-no-block-2) | `multiprocessing.Process` | 10 procesos buscan un nonce SHA-256 con dificultad 5 y el padre informa el resultado |
| [enunciado8-Pool](ejercicios/enunciado8-Pool) | `multiprocessing.Pool` | Primalidad de 2 a 100 con `Pool.map`, pool por defecto vs. `cpu_count()` workers |
| [enunciado9-Threading](ejercicios/enunciado9-Threading) | `threading` + `queue` | Un hilo lee stdin y otro lo codifica en ROT13; los datos pasan por dos colas |
| [enunciado10-pipes-con-nombre](ejercicios/enunciado10-pipes-con-nombre) | Pipe con nombre + `Pool` | Lee de una FIFO llamada `fifo` y compara la longitud de cada línea con la anterior usando `apply_async` |
| [enunciado11-socket](ejercicios/enunciado11-socket) | Socket TCP pasivo | Servidor serializado en `localhost:8080`: una conexión a la vez, imprime lo que recibe |
| [enunciado12-servidor](ejercicios/enunciado12-servidor) | Servidores TCP concurrentes | Servidor de mayúsculas en `localhost:9999`, versión `multiprocessing` y versión `threading`; `exit` cierra la conexión |
| [enunciado13-TCP-UDP-socketserver](ejercicios/enunciado13-TCP-UDP-socketserver) | `socketserver` | Servidor TCP de mayúsculas con hilos (`ThreadingMixIn`) en `0.0.0.0:30051`, se detiene con Enter |
| [enunciado14-server-http](ejercicios/enunciado14-server-http) | `http.server` | `BaseHTTPRequestHandler` propio en el puerto 1111 que sirve un index y dos páginas enlazadas, 404 en otro caso |
| [enunciado15-concurrent.futures](ejercicios/enunciado15-concurrent.futures) | `ProcessPoolExecutor` | Prueba en paralelo todos los números hasta el ingresado e imprime el mayor primo ≤ ese valor |
| [enunciado16-server-IPv4-IPv6](ejercicios/enunciado16-server-IPv4-IPv6) | IPv4/IPv6 | Servidor del ejercicio 12 escuchando en `::` (`AF_INET6`) con `multiprocessing`, más una versión con `socketserver.ThreadingTCPServer` |

### Trabajos prácticos

- **[TP1](tp1/CONSIGNA.md): inversor de líneas.** Lee el archivo de texto indicado con `-f` y crea un proceso hijo por línea. Cada línea viaja a su hijo por un pipe y el hijo la invierte. `tp1_sin_multip.py` usa `os.fork` + `os.pipe` y escribe el resultado en `invertido_sin_multiprocessing.txt`; `tp1_multip.py` (bonus) usa `multiprocessing.Process` + `Pipe`, devuelve la línea invertida al padre y escribe `info_invertida.txt`. Incluye un `texto.txt` de ejemplo y ambas salidas.
- **[TP2](tp2/enunciado_TP2.md): procesamiento de imágenes por HTTP.** Un `ThreadingTCPServer` con una subclase de `SimpleHTTPRequestHandler`. `GET /<imagen>` devuelve la imagen en escala de grises (sin `-e`) o redimensionada por el factor `-e`, guardada como `gris_<nombre>` o `escalada_<nombre>`. Pillow hace el procesamiento dentro del handler. El script además lanza un `multiprocessing.Process` alimentado por una `multiprocessing.Queue` y un hilo sincronizado con un `Lock` y un `Event`, orientados a los requisitos de IPC y sincronización de la consigna. Incluye una `imagen.jpeg` de ejemplo.

### Cómo usarlo

```bash
# from the repo root
python3 ejercicios/enunciado1/ej1.py 5
python3 ejercicios/enunciado1/ej2.py -c hola -n 3
python3 ejercicios/enunciado3-pipes/tp3.py -a ejercicios/enunciado3-pipes/archivo.txt
(cd tp1 && python3 tp1_sin_multip.py -f texto)   # file name without .txt

pip install pillow
cd tp2 && python3 tp2.py -i 127.0.0.1 -p 8080 -e 0.5   # omit -e for grayscale
# from another terminal
curl -X GET "http://127.0.0.1:8080/imagen.jpeg" --output imagen_procesada.jpeg
```

Los servidores escuchan en el host y puerto fijados en cada archivo (ver la tabla). Algunos archivos llevan el nombre de módulos de la biblioteca estándar (`socket.py`, `threading.py`, `multiprocessing.py`). Si se ejecutan desde su propia carpeta, tapan al módulo real, así que conviene renombrarlos antes.

### Autor

Tiago Weintraub · [github.com/TiagoWeintraub](https://github.com/TiagoWeintraub)
