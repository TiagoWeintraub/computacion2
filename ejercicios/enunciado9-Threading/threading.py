"""
1 - Escribir un programa que genere dos hilos utilizando threading.
Uno de los hilos debera leer desde stdin el texto ingresado por el usuario y deberá escribirlo en una cola de mensajes (queue).
El segundo hilo deberá leer desde la queue el contenido y encriptará dicho texto utilizando el algoritmo ROT13 y lo almacenará en una cola de mensajes (queue).
El primer hilo deberá leer dicho mensaje de la cola y lo mostrará por pantalla.
ROT13
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
gato (claro)->(rot13) tngb"""

import threading
import queue
import codecs

queue1 = queue.Queue() #cola encriptada
queue2 = queue.Queue() #cola

def leer():

    texto = input("Ingrese un texto: ")
    queue1.put(texto)
    queue2.join()
    mensaje = queue2.get()
    print("El mensaje encriptado es:", mensaje)
    queue2.task_done()

def encriptar():
    texto = queue1.get()
    mensaje = codecs.encode(texto, "rot13")
    queue2.put(mensaje)
    queue1.task_done()

t1 = threading.Thread(target=leer)
t1.start()

t2 = threading.Thread(target=encriptar)
t2.start()

t1.join()
t2.join()
