import os  # Permite interactuar con el sistema operativo
import cv2  # OpenCV: Se encarga de abrir, leer y empaquetar el formato de video
import time  # Proporciona las funciones de cronómetro para medir el tiempo de ejecución
from concurrent.futures import ThreadPoolExecutor  # Permite usar múltiples hilos de ejecución
def procesar_fotograma(frame):
    """Función que procesa un solo fotograma utilizando OpenCV de forma nativa."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
def convertir_video_a_bn_sobre_saturado(ruta_video_entrada, ruta_video_salida):
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
    # 16 hilos (el doble de la capacidad lógica de hardware)
    num_hilos_virtuales = 16
    print("Video abierto con éxito")
    print(f"Resolución: {ancho}x{alto} | FPS: {fps}")
    print(
        f"Procesando {total_fotogramas} fotogramas simulando {num_hilos_virtuales} hilos..."
    )
    # Configurar el codec para guardar el archivo .mp4 resultante
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        ruta_video_salida, fourcc, fps, (ancho, alto), isColor=False
    )
    tiempo_inicio = time.time()
    fotogramas_procesados = 0
    # Creamos un Pool de ejecución configurado exactamente para 16 hilos
    with ThreadPoolExecutor(max_workers=num_hilos_virtuales) as executor:
        while True:
            lote_frames = []
            for _ in range(num_hilos_virtuales):
                ret, frame = cap.read()
                if ret:
                    lote_frames.append(frame)
            if not lote_frames:
                break
            # 'map' asegura que los resultados mantengan el orden original del video
            resultados = executor.map(procesar_fotograma, lote_frames)
            # Escribir los fotogramas procesados en el archivo de salida
            for frame_bn in resultados:
                out.write(frame_bn)
                fotogramas_procesados += 1
            if (
                fotogramas_procesados % 240 == 0
                or fotogramas_procesados == total_fotogramas
            ):
                print(
                    f"Progreso: {fotogramas_procesados}/{total_fotogramas} fotogramas procesados."
                )
    tiempo_fin = time.time()
    tiempo_total_segundos = tiempo_fin - tiempo_inicio
    tiempo_total_minutos = tiempo_total_segundos / 60
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("\nProceso completado con éxito")
    # Mostrar el tiempo total de la tarea realizada convertido a minutos
    print(
        f"Tiempo total de la tarea realizada: {tiempo_total_minutos:.2f} minutos."
    )
video_de_entrada = (
     r"C:\Users\miria\Documents\Visual studio code\python\Paralelo\Naturaleza.mp4"
)
video_de_salida = r"C:\Users\miria\Documents\Visual studio code\python\Paralelo\Naturaleza_blanco_y_negro.mp4"
# Ejecutar la función principal utilizando 16 hilos (coincide con el nombre de arriba)
convertir_video_a_bn_sobre_saturado(video_de_entrada, video_de_salida)
