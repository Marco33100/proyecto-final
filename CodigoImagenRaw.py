from machine import Pin, SPI
from ili9341 import Display, color565
from time import sleep
import os

# Configuración SPI con tus pines exactos
spi = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(15),
                 width=320, height=240, rotation=90)  # Rotación 90°

# Backlight (usando tu pin 21)
backlight = Pin(21, Pin.OUT)
backlight.on()

def mostrar_imagen_raw(archivo, x, y, ancho, alto):
    """Muestra una imagen .raw en la pantalla"""
    try:
        # Verificar si el archivo existe
        if archivo not in os.listdir():
            print(f"Error: Archivo {archivo} no encontrado")
            return False
        
        # Calcular tamaño esperado del archivo (2 bytes por píxel)
        tamaño_esperado = ancho * alto * 2
        tamaño_real = os.stat(archivo)[6]  # Tamaño real del archivo
        
        if tamaño_real != tamaño_esperado:
            print(f"Error: Tamaño de imagen incorrecto. Esperado: {tamaño_esperado}, Actual: {tamaño_real}")
            return False
        
        # Leer y mostrar la imagen
        with open(archivo, 'rb') as f:
            display.block(x, y, x + ancho - 1, y + alto - 1, f.read())
        return True
        
    except Exception as e:
        print(f"Error al mostrar imagen: {e}")
        return False

# Limpiar pantalla
display.clear(color565(0, 0, 0))

# Mostrar imagen (ajusta los parámetros según tu imagen)
print("Mostrando imagen...")
if mostrar_imagen_raw('MicroPython128x128.raw',  # Nombre de archivo
                     50, 50,                    # Posición X,Y (esquina superior izquierda)
                     128, 128):                 # Ancho y alto de la imagen
    print("Imagen mostrada correctamente")
else:
    print("No se pudo mostrar la imagen")

# Texto adicional para referencia
display.draw_text8x8(10, 10, "CYD ESP32 - Mostrando Imagen", 
                    color565(255, 255, 255), color565(0, 0, 0))