# Proyecto-Final

##  Pulsera de medición de datos biometricos
Es un dispositivo portátil en forma de pulsera diseñado para monitorear en tiempo real las constantes vitales del usuario.

##  Descripción General
Este proyecto integra múltiples sensores y actuadores conectados a través de una red de ESP32, coordinados mediante Node-RED. Incluye visualización gráfica del sistema, control manual desde un dashboard web y almacenamiento de datos históricos en PostgreSQL.

##  Características principales
--Detección de ritmo cardíaco usando el sensor KY-039.
--Medición de temperatura corporal con el sensor MLX90614.
--Visualización de datos en una pantalla OLED 1.8” SPI.
--Activación de alertas sonoras mediante un buzzer pasivo en caso de anomalías.
--Led para la detección de temperatura anormal en el cuerpo humano.
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
|--|--|
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
                         │  • Led rojo                   │
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

## Tabla de Sensor
Sensor | Descripción|Foto
|--|--|--|
KY-039 | Sensor óptico para medir el ritmo cardíaco|![image](https://github.com/user-attachments/assets/fa940f3d-3a87-4fe1-a6e4-16acdffd07af)
MLX90614 | Sensor de temperatura sin contacto infrarrojo|![image](https://github.com/user-attachments/assets/401c46b3-0dcc-4972-b74d-074e2b1f1a54)

	
## Tabla de Actuadores
Actuador | Función| Foto
|--|--|--|
Pantalla OLED | Muestra los valores en tiempo real al usuario|![image](https://github.com/user-attachments/assets/0bf009e3-ee75-4057-946a-0337d6b3d88d)
Buzzer Pasivo | Emite sonido en caso de alerta|![image](https://github.com/user-attachments/assets/7ed74d0b-f35b-49bc-aa8b-1d033708d535)
Led rojo | Led que enciende cuando la temperatura este fuera del rango |![image](https://github.com/user-attachments/assets/1a8042c5-6bd4-441e-bc11-6462eb254dec)

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

![image](https://github.com/user-attachments/assets/5f58b3f5-b314-4abd-b369-3daa135ad183)
![image](https://github.com/user-attachments/assets/819bc65e-c63a-4341-bd20-c526bb4213df)


## Ejemplo de interfaz:
La estructura fue diseñada para ser ligera y cómoda como una pulsera, con espacio para los sensores y pantalla OLED.
![image](https://github.com/user-attachments/assets/99e2e0aa-f90b-4f84-9ba7-156acf12d8fa)

## Diagramas de las Placas
Proyecto en Cirkit Designer
![image](https://github.com/user-attachments/assets/45100d5d-c5d6-4f01-ab9c-61ca21137902)

## Almacenamiento de Datos
Los datos se almacenan en una tabla PostgreSQL estructurada así:

|Tabla||
|--|--|
|id| SERIAL PRIMARY KEY|
|timestamp| TIMESTAMP DEFAULT CURRENT_TIMESTAMP|
|Temperatura| FLOAT|
|ritmo_cardiaco| INTEGER|
|spo2| INTEGER|
|alertas| TEXT[]|

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
#### Link de librerias de la esp32-2432S024R para configurar en arduino
http://pan.jczn1688.com/directlink/1/ESP32%20module/2.4inch_ESP32-2432S024.zip

## Autores
Integrantes:
Balderas Melchor José Antonio//
Martínez Ramírez Marco Antonio//
Ruiz Rivera Juan Diego

## Autoevaluación y coevaluación
Balderas Melchor José Antonio - Autoevaluación
¿Qué hice bien?
Intenté aportar en lo que podía, sobre todo en el montaje físico y estar disponible cuando se necesitaba apoyo. Mantuve la calma en los momentos difíciles y traté de estar presente para el equipo.

¿Qué hice mal?
No entendí bien la idea principal del proyecto al inicio y eso me hizo sentir desconectado. Además, por el cansancio y el calor, no estuve al 100% de concentración, lo que provocó que cometiera errores como dañar un sensor.

¿Qué puedo mejorar?
Debería prepararme mejor antes de llegar al proyecto para no depender tanto de la explicación en el momento. También necesito mejorar mi enfoque y cuidado al manejar componentes delicados.

Por Marco y Diego

¿Qué hizo bien?
Toño trató de mantener una actitud relajada y estuvo presente durante el desarrollo del proyecto. Aportó principalmente en la parte física del armado y, a pesar del cansancio, intentó ayudar en lo que pudo.

¿Qué hizo mal?
Se notó que no comprendía bien el enfoque del proyecto desde el inicio, lo que causó cierta desconexión en los momentos clave. También, por distracción o cansancio, dañó un sensor importante, lo cual afectó la continuidad del trabajo.

¿Qué puede mejorar?
Debería involucrarse más desde el principio para entender bien lo que se va a hacer. También mejorar la concentración al manipular componentes electrónicos, ya que cualquier error puede salir costoso para el equipo.

Martínez Ramírez Marco Antonio - Autoevaluación
¿Qué hice bien?
Me encargué de toda la parte de software y lógica del proyecto, desde la programación hasta la integración con Node-RED y PostgreSQL. Pude establecer la estructura general del sistema para que funcionara correctamente ademas junto con mi compañero Diego en la parte de la logica fue de gran ayuda ya que el sabia mas de los componentes entonces entre los dos nos ayudamos proactivamente en este aspecto.

¿Qué hice mal?
Me frustro con facilidad cuando algo no sale como lo planeo. Hubo momentos donde me desesperé y dejé de pensar con claridad en lugar de buscar soluciones con calma.

¿Qué puedo mejorar?
Quiero trabajar en mi manejo emocional y en no dejar que el estrés me paralice. También me gustaría aprender a delegar más y confiar más en mis compañeros.

Por Toño y Diego

¿Qué hizo bien?
Marco fue el pilar técnico del equipo. configuró junto con Diego de Node-RED, la base de datos y manejó los sensores con gran habilidad.

¿Qué hizo mal?
A veces se desesperaba cuando algo no salía como quería. En lugar de calmarse y buscar otra opción, se frustraba y eso detenía un poco el avance. También tendía a cargar con mucho él solo, sin delegar.

¿Qué puede mejorar?
Le ayudaría mucho trabajar en la gestión del estrés y en aprender a confiar más en los demás. Tiene muchas habilidades, pero si las combina con paciencia y colaboración, el resultado sería aún mejor.

Ruiz Rivera Juan Diego - Autoevaluación
¿Qué hice bien?
Comencé el proyecto con mucha energía, motivación y disposición. Me involucré en el trabajo técnico y traté de colaborar con las pruebas y en solucionar los problemas cuando surgieron.

¿Qué hice mal?
Cuando surgió el problema del sensor, me desanimé bastante y me fue difícil seguir con el mismo enfoque. Dejé que el estrés me afectara y eso me hizo dudar de lo que estaba haciendo.

¿Qué puedo mejorar?
Tengo que aprender a adaptarme mejor a los contratiempos. No todo va a salir perfecto, y debo mantener la calma y seguir buscando soluciones en lugar de frustrarme.

Por Marco y Toño

¿Qué hizo bien?
Diego inició el proyecto con una actitud muy positiva y con muchas ganas. Participó activamente en las primeras fases y se esforzó en adaptarse a los cambios que se presentaron durante el proceso ademas que al final del proyecto fue el que mas se esforzo en el proyecto casi terminandolo el solo ya que algun sensor no queria funcinar y fue lo que mas nos retraso.

¿Qué hizo mal?
Cuando ocurrieron contratiempos como la quema del sensor, su motivación bajó bastante. El estrés lo afectó y eso se notó en cómo interactuaba con los demás y en su concentración.

¿Qué puede mejorar?
Diego podría enfocarse en mantener la calma y seguir adelante a pesar de los errores. La resiliencia y adaptación ante los imprevistos le permitirán avanzar más fácilmente en futuros trabajos en equipo.
