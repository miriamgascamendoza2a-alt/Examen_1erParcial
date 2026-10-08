import os  # Permite interactuar con el sistema operativo
import cv2  # OpenCV: Se encarga de abrir, leer y empaquetar el formato de video
import time  # Proporciona las funciones de cronómetro para medir el tiempo de ejecución
import numpy as np  # Funciona como puente/traductor entre las matrices de OpenCV y Pillow
from PIL import Image  # Pillow: Librería especializada en la edición y conversión de imágenes
from concurrent.futures import ThreadPoolExecutor  # Permite usar múltiples hilos de ejecución
def procesar_fotograma(frame):
    """Función que procesa un solo fotograma utilizando Pillow."""
    # OpenCV lee en BGR, lo convertimos a RGB para Pillow
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Crear la imagen de Pillow a partir de la matriz de OpenCV
    imagen_pil = Image.fromarray(frame_rgb)
    # Convertir a blanco y negro (escala de grises: 'L') usando Pillow
    imagen_bn_pil = imagen_pil.convert("L")
    # Volver a convertir la imagen de Pillow a matriz de Numpy para OpenCV
    return np.array(imagen_bn_pil)
def convertir_video_a_bn_todos_los_hilos(ruta_video_entrada, ruta_video_salida):
    # Abrir el video con OpenCV usando la ruta absoluta exacta
    cap = cv2.VideoCapture(ruta_video_entrada)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en {ruta_video_entrada}")
        print("Verifica que las carpetas y el nombre del archivo coincidan.")
        return
    # Obtener propiedades esenciales del video original
    fps = cap.get(cv2.CAP_PROP_FPS)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_fotogramas = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Detectar automáticamente el total de hilos lógicos del procesador
    total_hilos = os.cpu_count()
    print("Video abierto con éxito")
    print(f"Resolución: {ancho}x{alto} | FPS: {fps}")
    print(
        f"Procesando {total_fotogramas} fotogramas usando todos los hilos ({total_hilos})..."
    )
    # Configurar para guardar el archivo .mp4 resultante
    # Se usa isColor=False porque los fotogramas guardados serán en escala de grises
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        ruta_video_salida, fourcc, fps, (ancho, alto), isColor=False
    )
    tiempo_inicio = time.time()
    fotogramas_procesados = 0
    # Creamos un Pool de ejecución configurado con todos los hilos del sistema
    with ThreadPoolExecutor(max_workers=total_hilos) as executor:
        while True:
            lote_frames = []
            for _ in range(total_hilos):
                ret, frame = cap.read()
                if ret:
                    lote_frames.append(frame)
            if not lote_frames:
                break
            # 'map' asegura que los resultados mantengan el orden correcto del video
            resultados = executor.map(procesar_fotograma, lote_frames)
            # Escribir los fotogramas procesados en el archivo de salida
            for frame_bn in resultados:
                out.write(frame_bn)
                fotogramas_procesados += 1
            # Muestra el progreso cada 60 fotogramas junto con el porcentaje
            if fotogramas_procesados % 60 == 0 or fotogramas_procesados == total_fotogramas:
                porcentaje = (fotogramas_procesados / total_fotogramas) * 100
                print(
                    f"Progreso: {fotogramas_procesados}/{total_fotogramas} fotogramas ({porcentaje:.1f}%)"
                )
    tiempo_fin = time.time()
    tiempo_total_segundos = tiempo_fin - tiempo_inicio
    tiempo_total_minutos = tiempo_total_segundos / 60

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("\nProceso completado con éxito")
    # Mostrar el tiempo total de la tarea realizada en minutos
    print(
        f"Tiempo total de la tarea realizada: {tiempo_total_minutos:.2f} minutos."
    )
video_de_entrada = (
    r"C:\Users\miria\Documents\Visual studio code\python\Paralelo/Naturaleza.mp4"
)
video_de_salida = r"C:\Users\miria\Documents\Visual studio code\python\Paralelo/Naturaleza_blanco_y_negro.mp4"
# Ejecutar la función principal utilizando todos los hilos del procesador
convertir_video_a_bn_todos_los_hilos(video_de_entrada, video_de_salida)
