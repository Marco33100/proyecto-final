# Proyecto-Final

##  Pulsera de medición de datos biometricos
Es una pulsera que detecta ya las pulsaciones

##  Descripción General
Este proyecto integra múltiples sensores y actuadores conectados a través de una red de ESP32, coordinados mediante Node-RED. Incluye visualización gráfica del sistema, control manual desde un dashboard web y almacenamiento de datos históricos en PostgreSQL.

##  Características principales
--Detección de ritmo cardíaco usando el sensor KY-039.
--Medición de temperatura corporal con el sensor MLX90614.
--Visualización de datos en una pantalla OLED 1.8” SPI.
--Activación de alertas sonoras mediante un buzzer pasivo en caso de anomalías.
--Botón físico para interacción manual o reinicio de mediciones.
--Almacenamiento de datos biométricos en una base de datos PostgreSQL.
--Gráficas en tiempo real en Node-RED Dashboard.
--Comunicación entre módulos a través de MQTT con Mosquitto

##  Objetivos del Proyecto
--Desarrollar un sistema portátil de monitoreo de signos vitales.
--Visualizar los datos de salud en tiempo real desde una interfaz gráfica web.
--Generar alertas automáticas cuando se detecten valores fuera de rangos normales.
--Guardar registros históricos de las mediciones en una base de datos.
--Permitir la interacción del usuario mediante un botón físico y visualización OLED.


## 🧠 Tecnologías Utilizadas
|Tecnología	|Descripción|
|ESP32|	Microcontroladores para lectura y actuación|
|Node-RED	|Plataforma de automatización y dashboard web|
|PostgreSQL|	Base de datos para almacenamiento de datos|
|Python|	Scripts de backend y análisis de datos|
|MQTT| con Mosquitto	Protocolo de mensajería entre nodos ESP32 y Node Red|
|Impresión 3D|	Estructuras físicas y mecanismos personalizados|

## 🧠 Arquitectura del Sistema

                         ┌───────────────────────────────┐
                         │        ESP32 Principal        │
                         │  • Lectura de sensores        │
                         │    - KY-039 (Ritmo cardíaco)  │
                         │    - MLX90614 (Temperatura)   │
                         │  • Pantalla OLED (1.8”)       │
                         │  • Botón de interacción       │
                         │  • Alerta sonora (Buzzer)     │
                         └──────────────┬────────────────┘
                                        │
                                        ▼
                                    [ MQTT ]
                                        │
                                        ▼
                         ┌──────────────────────────────────┐
                         │         🌐 Node-RED              │
                         │  • Visualización en tiempo real  │
                         │  • Control automático y manual   │
                         │  • Detección de alertas          │
                         └──────────────┬───────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │  🗄️ Base de Datos PostgreSQL|
                         │                              |
                         │  • Registro de mediciones    │
                         │  • Trazabilidad de alertas   │
                         └──────────────────────────────┘

## Tabla de Actuadores
Sensor | Descripción|Foto
KY-039 | Sensor óptico para medir el ritmo cardíaco|
MLX90614 | Sensor de temperatura sin contacto infrarrojo|
	
## Tabla de Sensores
Actuador | Función| Foto
Pantalla OLED | Muestra los valores en tiempo real al usuario|
Buzzer Pasivo | Emite sonido en caso de alerta|
Botón | Permite interacción manual del usuario|

## Funcionalidad del Sistema
El sistema está basado en una pulsera que lee parámetros como el ritmo cardíaco y la temperatura corporal. Estos datos se transmiten mediante MQTT hacia un servidor donde Node-RED:

-Procesa los datos entrantes.

-Los visualiza en gráficos en tiempo real.

-Los guarda en PostgreSQL.

-Evalúa si deben emitirse alertas.

-Permite que los datos también se muestren localmente en la OLED.

## Interfaz Gráfica DashBoard
La interfaz fue desarrollada en Node-RED y permite:

1.- Visualizar gráficas de temperatura, ritmo cardíaco y SpO2.
2.- Revisar valores individuales en tiempo real.
3.- Observar notificaciones o alertas de salud.
4.- Controlar el estado del sistema de forma manual.

## Ejemplo de interfaz:
La estructura fue diseñada para ser ligera y cómoda como una pulsera, con espacio para los sensores y pantalla OLED.
![image](https://github.com/user-attachments/assets/99e2e0aa-f90b-4f84-9ba7-156acf12d8fa)

## Diagramas de las Placas
Proyecto en Cirkit Designer
![image](https://github.com/user-attachments/assets/45100d5d-c5d6-4f01-ab9c-61ca21137902)

## Almacenamiento de Datos
Los datos se almacenan en una tabla PostgreSQL estructurada así:

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperatura FLOAT,
    ritmo_cardiaco INTEGER,
    spo2 INTEGER,
    alertas TEXT[]
);

Esto permite:

-- Consultar mediciones por fecha y hora.

-- Analizar tendencias en los signos vitales.

-- Integrar los datos con otras herramientas externas.


## Material Multimedia

### Evidencia de desarrollo en clase
#### Actividad, datos de envio
https://drive.google.com/drive/folders/1vL-lAcMaFHmToQMPCNTURDCU5I9T4syF?usp=drive_link
#### Carcasa
https://drive.google.com/drive/folders/1MDsN1ivSvDB8vBrFrL9AF1wyVTXi7gcy?usp=sharing

## Conclusión del Proyecto

## Autores
Integrantes:
Balderas Melchor José Antonio
Martínez Ramírez Marco Antonio
Ruiz Rivera Juan Diego

## Autoevaluación y coevaluación
Balderas Melchor José Antonio
AutoEvaluación:
CoEvaluación:
Martínez Ramírez Marco Antonio
AutoEvaluación:
CoEvaluación:
Ruiz Rivera Juan Diego
AutoEvaluación:
CoEvaluación:
