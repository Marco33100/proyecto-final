from machine import Pin, SPI
from ili9341 import Display, color565
from time import sleep, ticks_ms
from xpt2046 import Touch
import urandom

# Configuración SPI
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=320, height=240, rotation=0)
touch = Touch(SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19)), cs=Pin(33))

# Paleta de colores mejorada para fondo blanco
COLORES = {
    'fondo': color565(255, 255, 255),  # blanco
    'panel': color565(230, 230, 230),  # gris claro
    'texto': color565(0, 0, 0),        # negro
    'primario': color565(0, 120, 215), # azul Windows
    'secundario': color565(0, 180, 100),
    'alerta': color565(255, 70, 70)
}

# Datos simulados para gráficos
datos_sensor = [50 + urandom.getrandbits(5) for _ in range(30)]

# Clase XglcdFont (copiada de tu librería)
class XglcdFont(object):
    """Font data in X-GLCD format."""
    BIT_POS = {1: 0, 2: 2, 4: 4, 8: 6, 16: 8, 32: 10, 64: 12, 128: 14, 256: 16}

    def __init__(self, path, width, height, start_letter=32, letter_count=96):
        self.width = width
        self.height = max(height, 8)
        self.start_letter = start_letter
        self.letter_count = letter_count
        self.bytes_per_letter = (floor((self.height - 1) / 8) + 1) * self.width + 1
        self.__load_xglcd_font(path)

    def __load_xglcd_font(self, path):
        bytes_per_letter = self.bytes_per_letter
        self.letters = bytearray(bytes_per_letter * self.letter_count)
        mv = memoryview(self.letters)
        offset = 0
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0 or line[0:2] != '0x':
                    continue
                comment = line.find('//')
                if comment != -1:
                    line = line[0:comment].strip()
                if line.endswith(','):
                    line = line[0:len(line) - 1]
                mv[offset: offset + bytes_per_letter] = bytearray(
                    int(b, 16) for b in line.split(','))
                offset += bytes_per_letter

    def lit_bits(self, n):
        while n:
            b = n & (~n+1)
            yield self.BIT_POS[b]
            n ^= b

    def get_letter(self, letter, color, background=0, landscape=False):
        letter_ord = ord(letter) - self.start_letter
        if letter_ord >= self.letter_count:
            print('Font does not contain character: ' + letter)
            return b'', 0, 0
        bytes_per_letter = self.bytes_per_letter
        offset = letter_ord * bytes_per_letter
        mv = memoryview(self.letters[offset:offset + bytes_per_letter])

        letter_width = mv[0]
        letter_height = self.height
        letter_size = letter_height * letter_width
        if background:
            buf = bytearray(background.to_bytes(2, 'big') * letter_size)
        else:
            buf = bytearray(letter_size * 2)

        msb, lsb = color.to_bytes(2, 'big')

        if landscape:
            pos = (letter_size * 2) - (letter_height * 2)
            lh = letter_height
            for b in mv[1:]:
                for bit in self.lit_bits(b):
                    buf[bit + pos] = msb
                    buf[bit + pos + 1] = lsb
                if lh > 8:
                    pos += 16
                    lh -= 8
                else:
                    pos -= (letter_height * 4) - (lh * 2)
                    lh = letter_height
        else:
            col = 0
            bytes_per_letter = ceil(letter_height / 8)
            letter_byte = 0
            for b in mv[1:]:
                segment_size = letter_byte * letter_width * 16
                for bit in self.lit_bits(b):
                    pos = (bit * letter_width) + (col * 2) + segment_size
                    buf[pos] = msb
                    pos = (bit * letter_width) + (col * 2) + 1 + segment_size
                    buf[pos] = lsb
                letter_byte += 1
                if letter_byte + 1 > bytes_per_letter:
                    col += 1
                    letter_byte = 0

        return buf, letter_width, letter_height

    def measure_text(self, text, spacing=1):
        length = 0
        for letter in text:
            letter_ord = ord(letter) - self.start_letter
            offset = letter_ord * self.bytes_per_letter
            length += self.letters[offset] + spacing
        return length

# Cargar fuente (necesitarás tener el archivo de fuente en tu sistema)
# font = XglcdFont('font_file.txt', width=8, height=16)  # Descomenta y ajusta cuando tengas el archivo

def dibujar_texto(x, y, texto, color, fondo=None, font_size=16):
    """Dibuja texto usando la mejor fuente disponible"""
    if font_size <= 8:
        display.draw_text8x8(x, y, texto, color, fondo if fondo else COLORES['fondo'])
    else:
        # Usar XglcdFont si está disponible
        if 'font' in globals():
            for letra in texto:
                buf, w, h = font.get_letter(letra, color, fondo)
                if w > 0 and h > 0:
                    display.draw_sprite(buf, x, y, w, h)
                    x += w + 1  # Espaciado entre letras
        else:
            # Fallback a draw_text8x8 si no hay fuente cargada
            display.draw_text8x8(x, y, texto, color, fondo if fondo else COLORES['fondo'])

def dibujar_panel(x, y, ancho, alto, titulo=""):
    """Dibuja un panel más limpio sobre fondo blanco"""
    # Sombra clara
    display.fill_rectangle(x+2, y+2, ancho, alto, color565(200, 200, 200))
    # Panel principal
    display.fill_rectangle(x, y, ancho, alto, COLORES['panel'])
    # Borde
    display.draw_rectangle(x, y, ancho, alto, COLORES['primario'])
    # Título
    if titulo:
        dibujar_texto(x+10, y+5, titulo, COLORES['primario'], COLORES['panel'])

def dibujar_grafico(x, y, ancho, alto, datos, color):
    """Dibuja un gráfico de líneas"""
    max_val = max(datos) if max(datos) > 0 else 1
    puntos = []
    
    for i, valor in enumerate(datos):
        px = x + int(i * (ancho / len(datos)))
        py = y + alto - int((valor / max_val) * alto)
        puntos.append((px, py))
    
    for i in range(len(puntos)-1):
        display.draw_line(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1], color)

def dibujar_medidor(x, y, tamaño, valor, maximo=100, titulo=""):
    """Dibuja un medidor circular moderno"""
    radio = tamaño // 2
    centro_x = x + radio
    centro_y = y + radio
    
    # Borde
    display.draw_circle(centro_x, centro_y, radio, COLORES['primario'])

    # Relleno dinámico
    for r in range(radio-4, 0, -2):
        display.fill_circle(centro_x, centro_y, r, color565(
            int(255 * (valor/maximo)),
            int(150 * (1 - valor/maximo)),
            150))

    # Valor numérico
    dibujar_texto(centro_x - 10, centro_y - 5, f"{valor}%", COLORES['texto'], 0)

    # Título
    if titulo:
        dibujar_texto(centro_x - len(titulo)*4, y + tamaño + 5, titulo, COLORES['texto'], 0)

def actualizar_datos():
    """Actualiza datos simulados"""
    global datos_sensor
    datos_sensor = datos_sensor[1:] + [50 + urandom.getrandbits(5)]
    return datos_sensor[-1]

def dibujar_interfaz():
    """Dibuja toda la interfaz"""
    display.clear(COLORES['fondo'])
    
    # Panel gráfico
    dibujar_panel(10, 10, 300, 100, "Datos del Sensor")
    dibujar_grafico(20, 30, 280, 70, datos_sensor, COLORES['primario'])
    
    # Medidores
    valor_actual = actualizar_datos()
    dibujar_medidor(50, 130, 80, valor_actual, 100, "Nivel")
    dibujar_medidor(180, 130, 80, 100-valor_actual, 100, "Comp.")
    
    # Barra de estado inferior
    display.fill_rectangle(0, 220, 320, 20, COLORES['panel'])
    dibujar_texto(10, 222, f"Lectura: {valor_actual}%", COLORES['texto'], COLORES['panel'])
    dibujar_texto(220, 222, "CORE v1.0", COLORES['primario'], COLORES['panel'])

# Bucle principal
ultima_actualizacion = ticks_ms()
while True:
    if ticks_ms() - ultima_actualizacion > 1000:  # Actualizar cada segundo
        dibujar_interfaz()
        ultima_actualizacion = ticks_ms()
    
    # Detección de toques
    coords = touch.get_touch()
    if coords:
        x, y = coords
        print(f"Toque en: {x}, {y}")  # Para depuración
    
    sleep(0.1)
