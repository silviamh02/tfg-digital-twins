import os
import json
import time
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FUNCIONES ------------------------------------------------------------------------------------

# Función para cargar la configuración desde el archivo JSON
def parse_config_file(config_file_path):
    with open(config_file_path, 'r') as config_file: # Abre el archivo en modo lectura
        config_data = json.load(config_file) # Carga el JSON en un diccionario
    
    # # Extraer las variables necesarias del archivo de configuración
    # topology_path = config_data.get('topology_path')
    # behavior_path = config_data.get('behavior_path')
    # mqtt_broker_ip = config_data.get('mqtt_broker_ip')
    # mqtt_broker_port = config_data.get('mqtt_broker_port')
    
    return config_data # Devuelve el diccionario


