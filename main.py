from machine import I2C, Pin
import time
from bme280 import BME280
import network
import urequests

# asignación del I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)

# Inicio del sensor BME280
sensor = BME280(i2c=i2c)

# Configuración de WiFi
ssid = 'INFINITUMABF2'
password = '3JHNd4cNaf'

# Para conecta a WiFi
def conecta_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('Conexión WiFi establecida:', wlan.ifconfig())

# URL del canal de ThingSpeak para uso de datos
url_thingspeak = "https://api.thingspeak.com/update?api_key=NDIH4DJ4XISKZPUO"

conecta_wifi(ssid, password)

while True:
    try:
        # Lectura de la temperatura
        temperature, pressure, humidity = sensor.read_compensated_data()
        temperature = temperature / 100  # Convertir a grados Celsius
        print("Temperatura:", temperature, "°C")

        # Enviar datos a ThingSpeak
        response = urequests.get(url_thingspeak + "&field1=" + str(temperature))
        response.close()

        time.sleep(20)  # ThingSpeak permite enviar datos cada 15 segundos
    except OSError as e:
        print('Error al leer el sensor:', e)
