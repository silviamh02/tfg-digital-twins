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


# Función para generar el nombre único del JSON de topología
def generate_unique_filename_topology():
    # Obtener la fecha y hora actual en una estructura de tiempo
    current_time = time.localtime()
    
    # Convertir la estructura de tiempo a un valor EPOCH
    epoch_time = int(time.mktime(current_time))
    
    # Generar el nombre de archivo único utilizando el valor EPOCH
    filename = f"TOPO_{epoch_time}.json"
    
    return filename


# Función para generar el nombre único del JSON de comportamiento
def generate_unique_filename_behavior():
    # Obtener la fecha y hora actual en una estructura de tiempo
    current_time = time.localtime()
    
    # Convertir la estructura de tiempo a un valor EPOCH
    epoch_time = int(time.mktime(current_time))
    
    # Generar el nombre de archivo único utilizando el valor EPOCH
    filename = f"BEHA_{epoch_time}.json"
    
    return filename


# Función para generar JSON de topología
def generate_topology_json(topology_path):
    # Crear el diccionario con los datos de topología
    topology_json = {
        "message": "JSON topology de prueba" # Añadir los datos de la topología más adelante!!!
    }
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_topology()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(topology_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(topology_json, json_file, indent=4)
    
    # Devolver la ruta completa del archivo generado
    return file_path


# Función para generar JSON de comportamiento
def generate_behavior_json(behavior_path):
    # Crear el diccionario con los datos de comportamiento
    behavior_json = {
        "message": "JSON behavior de prueba" # Añadir los datos del comportamiento más adelante!!!
    }
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_behavior()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(behavior_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(behavior_json, json_file, indent=4)
    
    # Devolver la ruta completa del archivo generado
    return file_path

