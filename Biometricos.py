"""
Proyecto Wearable IoT con ESP32
- KY-039 (ritmo cardíaco) en lugar de MAX30100
- MLX90614 (temperatura) y OLED en bus I2C
- Comunicación MQTT para Node-RED
- Alertas por correo electrónico
"""

import time
import network
import machine
from machine import Pin, I2C, PWM, ADC
import ubinascii
from umqtt.simple import MQTTClient
import json
import gc
import urequests

# Importar las librerías de los sensores
from mlx90614 import MLX90614
from ssd1306 import SSD1306_I2C

# URL del servicio web para enviar correos (reemplaza con tu URL de Apps Script)
WEBAPP_URL = "https://script.google.com/macros/s/TU_ID_DE_SCRIPT/exec"

# Configuración de WiFi
WIFI_SSID = "ZONA PIPOLLA 2"
WIFI_PASSWORD = "pgvmKVN2vC"

# Configuración MQTT
MQTT_BROKER = "192.168.1.68"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_wearable"
MQTT_TOPIC = b"wearable/datos"

# Pines para los componentes
I2C_SDA_PIN = 16
I2C_SCL_PIN = 17
BUZZER_PIN = 5
KY039_PIN = 34  # Pin analógico para el sensor KY-039 (ADC1_CH0)
LED_ALERT_PIN = 4  # Usa el GPIO que tú decidas, por ejemplo el GPIO2
led_alert = Pin(LED_ALERT_PIN, Pin.OUT)


# Configuración de umbrales (valores normales para un adulto promedio)
TEMP_MIN = 30.0  # °C
TEMP_MAX = 37.8  # °C
HR_MIN = 60      # BPM
HR_MAX = 100     # BPM
SPO2_MIN = 95    # % (Valor simulado ya que KY-039 no mide SpO2)
SPO2_MAX = 100   # %

# Variables para control de alertas por correo
last_email_time = 0
EMAIL_INTERVAL = 60  # Enviar correo como máximo cada 60 segundos

# Variables para el sensor KY-039
pulse_readings = []
MAX_SAMPLES = 300  # Número de muestras para calcular BPM
last_beat = 0
beat_interval = 0

# Inicialización del bus I2C
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=100000)

# Función para enviar alerta por correo
def enviar_alerta_email(temp, heart_rate, spo2, alertas):
    try:
        data = {
            "temperatura": round(temp, 1),
            "ritmo_cardiaco": int(heart_rate),
            "spo2": int(spo2),
            "alertas": alertas,
            "timestamp": int(time.time())
        }
        
        print(f"Enviando alerta por correo: {data}")
        
        # Enviar solicitud al servicio web de Google Apps Script
        response = urequests.post(WEBAPP_URL, json=data)
        print(f"Respuesta del servidor: {response.text}")
        response.close()
        return True
    except Exception as e:
        print(f"Error al enviar alerta por correo: {e}")
        return False

# Buscar dispositivos I2C (para debugging)
def scan_i2c():
    print("Dispositivos I2C encontrados:", [hex(addr) for addr in i2c.scan()])

# Inicializar componentes
def init_components():
    # Inicializar pantalla OLED
    try:
        oled = SSD1306_I2C(128, 64, i2c)
        print("Pantalla OLED inicializada")
    except Exception as e:
        print("Error al inicializar OLED:", e)
        oled = None
        
    # Inicializar sensor KY-039
    try:
        ky039 = ADC(Pin(KY039_PIN))
        ky039.atten(ADC.ATTN_11DB)  # Configuración para rango completo 0-3.3V
        print("Sensor KY-039 inicializado")
    except Exception as e:
        print("Error al inicializar KY-039:", e)
        ky039 = None
        
    # Inicializar sensor de temperatura
    try:
        mlx = MLX90614(i2c)
        print("Sensor MLX90614 inicializado")
    except Exception as e:
        print("Error al inicializar MLX90614:", e)
        mlx = None
        
    # Inicializar buzzer
    try:
        buzzer = PWM(Pin(BUZZER_PIN), freq=2000, duty=0) # Inicialmente apagado
        print("Buzzer inicializado")
    except Exception as e:
        print("Error al inicializar Buzzer:", e) 
        buzzer = None
        
    return oled, ky039, mlx, buzzer

# Conectar a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Esperar por conexión con timeout
        max_wait = 20
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print("Esperando conexión...")
            time.sleep(1)
    
    if wlan.isconnected():
        print("Conectado a WiFi")
        print("Dirección IP:", wlan.ifconfig()[0])
        return True
    else:
        print("Error al conectar a WiFi")
        return False

# Configurar cliente MQTT
def setup_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print("Conectado a broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar a MQTT:", e)
        return None

# Función para activar la alarma
def sound_alarm(buzzer, duration=0.5):
    if buzzer:
        try:
            buzzer.duty(512)  # 50% duty cycle (volumen medio)
            time.sleep(duration)
            buzzer.duty(0)    # Apagar
        except Exception as e:
            print("Error en buzzer:", e)

# Verificar si los valores están fuera de rango
def check_values(temp, heart_rate, spo2):
    global last_email_time
    current_time = time.time()
    
    alerts = []
    
    if temp < TEMP_MIN:
        alerts.append(f"¡ALERTA! Temperatura baja: {temp:.1f}°C")
        led_alert.on()
    elif temp > TEMP_MAX:
        alerts.append(f"¡ALERTA! Temperatura alta: {temp:.1f}°C")
        led_alert.onn()
    else:
        led_alert.off()
        
    if heart_rate < HR_MIN:
        alerts.append(f"¡ALERTA! Ritmo cardíaco bajo: {heart_rate} BPM")
    elif heart_rate > HR_MAX:
        alerts.append(f"¡ALERTA! Ritmo cardíaco alto: {heart_rate} BPM")
        
    if spo2 < SPO2_MIN:
        alerts.append(f"¡ALERTA! SpO2 bajo: {spo2}%")
    
    # Si hay alertas y ha pasado suficiente tiempo desde el último correo
    if alerts and (current_time - last_email_time >= EMAIL_INTERVAL):
        print(f"Se detectaron alertas, enviando correo: {alerts}")
        if enviar_alerta_email(temp, heart_rate, spo2, alerts):
            last_email_time = current_time
            print(f"Correo enviado. Próximo correo disponible en {EMAIL_INTERVAL} segundos")
        
    return alerts

# Función para mostrar datos en la pantalla OLED
def update_display(oled, temp, heart_rate, spo2, alerts=None):
    if oled:
        try:
            oled.fill(0)  # Limpiar pantalla
            
            # Mostrar valores
            oled.text("Temp: {:.1f} C".format(temp), 0, 0)
            oled.text("HR: {} BPM".format(heart_rate), 0, 16)
            oled.text("SpO2: {}%*".format(spo2), 0, 32)  # Asterisco para indicar valor simulado
            
            # Mostrar alerta (si hay)
            if alerts and len(alerts) > 0:
                oled.text("ALERTA!", 0, 48)
            else:
                oled.text("*valor simulado", 0, 48)  # Indicar que SpO2 es simulado
                
            oled.show()
        except Exception as e:
            print("Error al actualizar display:", e)

# Función mejorada para procesar datos del sensor KY-039
def process_ky039(ky039_sensor):
    global pulse_readings, last_beat, beat_interval
    
    try:
        # Leer el valor analógico del sensor
        value = ky039_sensor.read()
        print(f"KY-039 raw: {value}")
        
        # Añadir a las lecturas
        pulse_readings.append(value)
        
        # Limitar el número de lecturas almacenadas
        if len(pulse_readings) > MAX_SAMPLES:
            pulse_readings.pop(0)
            
        if len(pulse_readings) < 20:
            return 75
        
        # Trabajar con las últimas 20 muestras
        recent_readings = pulse_readings[-20:]
        min_value = min(recent_readings)
        max_value = max(recent_readings)
        
        # Calcular la derivada (tasa de cambio)
        derivatives = []
        for i in range(1, len(recent_readings)):
            derivatives.append(recent_readings[i] - recent_readings[i-1])
        
        # Buscar picos en la derivada (cambios rápidos)
        current_time = time.time() * 1000
        
        # Detectar un pico cuando hay un cambio grande
        if len(derivatives) > 2 and abs(derivatives[-1]) > 50:
            # Asegurarse de que no detectamos el mismo latido dos veces
            if last_beat == 0 or (current_time - last_beat) > 300:  # Al menos 300ms entre latidos
                print(f"¡Cambio detectado! Derivada: {derivatives[-1]}")
                
                if last_beat == 0:
                    last_beat = current_time
                    return 75
                
                beat_interval = current_time - last_beat
                last_beat = current_time
                
                if 300 < beat_interval < 1500:
                    bpm = int(60000 / beat_interval)
                    print(f"Pulso calculado: {bpm} BPM (intervalo: {beat_interval}ms)")
                    return bpm
        
        # Reset si no hay latidos en 3 segundos
        if last_beat > 0 and (current_time - last_beat) > 3000:
            print("Sin latidos detectados en 3s, reiniciando")
            last_beat = 0
            return 75
            
        # Usar último cálculo válido
        if beat_interval > 300 and beat_interval < 1500:
            return int(60000 / beat_interval)
            
        return 75
            
    except Exception as e:
        print(f"Error procesando KY-039: {e}")
        return 75

# Simular SpO2 basado en ritmo cardíaco y temperatura
def simulate_spo2(heart_rate, temp):
    # Esta es una simulación simplificada y NO refleja una relación médica real
    # Solo para propósitos de demostración
    
    # Base SpO2 - normalmente entre 95-100%
    base_spo2 = 98
    
    # Ajustar según HR (simplificado para demostración)
    if heart_rate < 60:  # Bradycardia
        base_spo2 -= 2
    elif heart_rate > 100:  # Tachycardia
        base_spo2 -= 1
        
    # Ajustar según temperatura (simplificado para demostración)
    if temp < 35.0:  # Hypothermia
        base_spo2 -= 3
    elif temp > 38.0:  # Fever
        base_spo2 -= 2
        
    # Asegurar que el valor esté dentro de límites razonables
    return max(min(base_spo2, 100), 85)

# Función principal
def main():
    # Iniciar con limpieza de memoria
    gc.collect()
    
    # Escanear dispositivos I2C
    scan_i2c()
    
    # Inicializar componentes
    oled, ky039, mlx, buzzer = init_components()
    
    # Conectar a WiFi
    wifi_connected = connect_wifi()
    
    # Configurar MQTT si WiFi está conectado
    mqtt_client = None
    if wifi_connected:
        mqtt_client = setup_mqtt()
    
    # Inicializar variables para lecturas
    temp = 0.0
    heart_rate = 75  # Valor inicial
    spo2 = 97        # Valor inicial (simulado)
    last_mqtt_time = 0
    
    print("Iniciando monitoreo...")
    
    # Bucle principal
    while True:
        try:
            # Recolectar basura para evitar problemas de memoria
            gc.collect()
            
            # Obtener tiempo actual
            current_time = time.time()
            
            # Leer temperatura
            if mlx:
                try:
                    temp = mlx.read_object_temp()
                    print(f"Temperatura: {temp:.1f}°C")
                except Exception as e:
                    print("Error al leer temperatura:", e)
            
            # Leer pulso del sensor KY-039
            if ky039:
                try:
                    heart_rate = process_ky039(ky039)
                    print(f"Ritmo cardíaco: {heart_rate} BPM")
                    
                    # Simular SpO2 basado en ritmo cardíaco y temperatura
                    spo2 = simulate_spo2(heart_rate, temp)
                    print(f"SpO2 (simulado): {spo2}%")
                except Exception as e:
                    print("Error al obtener datos KY-039:", e)
            
            # Verificar valores y enviar alerta si es necesario
            alerts = check_values(temp, heart_rate, spo2)
            
            # Activar alarma si hay alertas
            if alerts:
                print("ALERTAS DETECTADAS:")
                for alert in alerts:
                    print(alert)
                sound_alarm(buzzer, 1)  # Duración más corta para reducir bloqueos
            
            # Actualizar pantalla
            update_display(oled, temp, heart_rate, spo2, alerts)
            
            # Enviar datos a MQTT cada 5 segundos
            if mqtt_client and (current_time - last_mqtt_time >= 5):
                try:
                    # Datos simplificados para evitar problemas de serialización
                    data = {
                        "temperatura": round(temp, 1),
                        "ritmo_cardiaco": int(heart_rate),
                        "spo2": int(spo2),  # Valor simulado
                        "alertas": ", ".join(alerts) if alerts else "",
                        "timestamp": int(current_time)
                    }
                    # Convertir a JSON con manejo de errores
                    json_data = json.dumps(data)
                    mqtt_client.publish(MQTT_TOPIC, json_data.encode())  # Codificar como bytes
                    print(f"Datos enviados a MQTT: {json_data}")
                    last_mqtt_time = current_time
                except Exception as e:
                    print(f"Error al publicar en MQTT: {e}")
            
            # Esperar - tiempo más corto para muestreo frecuente del sensor KY-039
            time.sleep(0.1)  # Muestreo más frecuente para detectar mejor los pulsos
            
        except KeyboardInterrupt:
            print("Programa terminado por el usuario")
            break
        except Exception as e:
            print("Error en bucle principal:", e)
            time.sleep(3)  # Esperar más tiempo antes de reintentar

# Punto de entrada principal con protección global
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error fatal:", e)