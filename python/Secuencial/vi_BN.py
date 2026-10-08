import os # Permite interactuar con el sistema operativo 
import cv2 # OpenCV: Se encarga de abrir, leer y empaquetar el formato de video
import time # Proporciona las funciones de cronómetro para medir el tiempo de ejecución
import numpy as np # Funciona como puente/traductor entre las matrices de OpenCV y Pillow
from PIL import Image # Pillow: Librería especializada en la edición y conversión de imágenes
from moviepy.video.io.VideoFileClip import VideoFileClip # Herramienta para extraer e inyectar audio
def convertir_video_a_bn_con_audio(ruta_video_entrada, ruta_video_salida):
    # 1. Abrir el video con OpenCV
    cap = cv2.VideoCapture(ruta_video_entrada)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en {ruta_video_entrada}")
        print("Verifica que las carpetas y el nombre del archivo coincidan exactamente.")
        return
    # Obtener propiedades del video original
    fps = cap.get(cv2.CAP_PROP_FPS)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_fotogramas = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("¡Video abierto con éxito!")
    print(f"Resolución: {ancho}x{alto} | FPS: {fps}")
    print(f"Procesando {total_fotogramas} fotogramas...")
    # Ruta temporal para el video mudo
    ruta_temporal = ruta_video_salida.replace(".mp4", "_temp_mudo.mp4")
    # Configurar el codec para guardar el archivo de video mudo temporal
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(ruta_temporal, fourcc, fps, (ancho, alto), isColor=False)
    # INICIO DE LA MEDICIÓN DE TIEMPO 
    tiempo_inicio = time.time()
    fotogramas_procesados = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # PROCESAMIENTO DE FOTOGRAMAS CON PILLOW
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(frame_rgb)
        imagen_bn_pil = imagen_pil.convert('L')
        frame_bn = np.array(imagen_bn_pil)
        out.write(frame_bn)
        fotogramas_procesados += 1
        # OPTIMIZACIÓN: Se imprime cada 300 fotogramas para no frenar el procesador
        if fotogramas_procesados % 60 == 0:  
            print(f"Progreso: {fotogramas_procesados}/{total_fotogramas} fotogramas procesados.")
    # Liberar recursos de OpenCV inmediatamente
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("\nFotogramas procesados. Transfiriendo el audio original...")
    try:
        video_original = VideoFileClip(ruta_video_entrada)
        video_bn_mudo = VideoFileClip(ruta_temporal)
        if video_original.audio is not None:
            video_final = video_bn_mudo.with_audio(video_original.audio)
            # preset="ultrafast" acelera drásticamente la velocidad de MoviePy
            video_final.write_videofile(
                ruta_video_salida, 
                codec="libx264", 
                audio_codec="aac", 
                preset="ultrafast",
                logger=None
            )
        else:
            print("El video original no contiene audio. Guardando archivo final...")
            video_bn_mudo.write_videofile(ruta_video_salida, codec="libx264", preset="ultrafast", logger=None)
        video_original.close()
        video_bn_mudo.close()
    except Exception as e:
        print(f"Ocurrió un aviso/error con el audio: {e}")
    finally:
        # Limpieza: Borrar el archivo temporal mudo
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    print("\n¡Proceso completado con éxito!")
    print(f"Tiempo total de la tarea realizada: {tiempo_total:.2f} segundos.")
# Configuración de rutas finales 
video_de_entrada = r"C:\Users\miria\Documents\Visual studio code\python\Secuencial\Sistema_solar.mp4" 
video_de_salida = r"C:\Users\miria\Documents\Visual studio code\python\Secuencial\Sistema_solar_blanco_y_negro.mp4"
convertir_video_a_bn_con_audio(video_de_entrada, video_de_salida)