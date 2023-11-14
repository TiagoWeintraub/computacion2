import http.server
import socketserver
import threading
import multiprocessing
import os
import argparse
from PIL import Image

# MODO DE USO:
# 1) INICIAR SERVIDOR HTTP:
#           python3 tp2.py -i 127.0.0.1 -p 8080 -e 0.5 --> Si no se coloca el factor de escalado -e la imagen es en escala de grises
# 2) INICIAR CLIENTE:
#           curl -X GET "http://127.0.0.1:8080/imagen.jpeg" --output imagen_procesada.jpeg
#           Otra opción es acceder a http://localhost:8080/imagen.jpeg

class ProcesadorDeImagenes(http.server.SimpleHTTPRequestHandler):
    factor_escala = 1.0
    imagen_procesada = None
    lock = threading.Lock()
    event = threading.Event()

    def do_GET(self):
        try:
            ruta_imagen = self.path[1:]

            if self.factor_escala == 1.0:
                ruta_procesada = self.convertir_a_escala_de_grises(ruta_imagen)
            else:
                ruta_procesada = self.escalar_imagen(ruta_imagen, self.factor_escala)

            if ruta_procesada:
                with open(ruta_procesada, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error en el servidor: no se pudo procesar la imagen")
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            print(f"Error en la solicitud GET: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error en el servidor: {e}".encode('utf-8'))

    def convertir_a_escala_de_grises(self, ruta_imagen):
        try:
            with Image.open(ruta_imagen) as img:
                img_gris = img.convert("L")
                ruta_procesada = "gris_" + os.path.basename(ruta_imagen)
                img_gris.save(ruta_procesada)
                return ruta_procesada
        except Exception as e:
            print(f"Error en la conversión a escala de grises: {e}")
            return None

    def escalar_imagen(self, ruta_imagen, factor_escala):
        try:
            with Image.open(ruta_imagen) as img:
                ancho, alto = img.size
                nuevo_ancho = int(ancho * factor_escala)
                nuevo_alto = int(alto * factor_escala)
                img_escalada = img.resize((nuevo_ancho, nuevo_alto))
                ruta_procesada = "escalada_" + os.path.basename(ruta_imagen)
                img_escalada.save(ruta_procesada)
                return ruta_procesada
        except Exception as e:
            print(f"Error en el escalado de la imagen: {e}")
            return None

def iniciar_servidor_http(ip, puerto, manejador, queue):
    with socketserver.ThreadingTCPServer((ip, puerto), manejador) as servidor_http:
        print(f"Servidor HTTP en {ip}:{puerto}")

        hilo_procesar_imagen = threading.Thread(target=procesar_imagen, args=(manejador,))
        hilo_procesar_imagen.start()

        while True:
            servidor_http.handle_request()

def procesar_imagen(manejador):
    try:
        while True:
            with manejador.lock:
                manejador.event.clear()
                while manejador.imagen_procesada is None:
                    manejador.lock.release()
                    manejador.event.wait()
                    manejador.lock.acquire()

                ruta_imagen_procesada = manejador.imagen_procesada
                manejador.imagen_procesada = None

            with open(ruta_imagen_procesada, 'rb') as f:
                manejador.request.sendall(f.read())
    except Exception as e:
        print(f"Error en el hilo de procesamiento de imágenes: {e}")

def iniciar_servidor_procesamiento_imagenes(queue):
    try:
        while True:
            factor_escala = queue.get()
            ProcesadorDeImagenes.factor_escala = factor_escala
            ruta_imagen_procesada = ProcesadorDeImagenes.convertir_a_escala_de_grises("imagen.jpg")

            with ProcesadorDeImagenes.lock:
                ProcesadorDeImagenes.imagen_procesada = ruta_imagen_procesada
                ProcesadorDeImagenes.event.set()

    except KeyboardInterrupt:
        print("\nDeteniendo servidor de procesamiento de imágenes...")
    except Exception as e:
        print(f"Error en el servidor de procesamiento de imágenes: {e}")

def main():
    parser = argparse.ArgumentParser(description='Tp2 - procesa imágenes')
    parser.add_argument('-i', '--ip', help='Dirección de escucha', required=True)
    parser.add_argument('-p', '--puerto', help='Puerto de escucha', type=int, required=True)
    parser.add_argument('-e', '--escala', help='Factor de escala para redimensionar la imagen', type=float, default=1.0)
    args = parser.parse_args()

    manejador = ProcesadorDeImagenes
    manejador.factor_escala = args.escala

    queue = multiprocessing.Queue()

    hilo_servidor_http = threading.Thread(target=iniciar_servidor_http, args=(args.ip, args.puerto, manejador, queue), daemon=True)
    hilo_servidor_http.start()

    proceso_procesamiento_imagenes = multiprocessing.Process(target=iniciar_servidor_procesamiento_imagenes, args=(queue,))
    proceso_procesamiento_imagenes.start()

    try:
        hilo_servidor_http.join()
        proceso_procesamiento_imagenes.join()
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")

if __name__ == "__main__":
    main()
