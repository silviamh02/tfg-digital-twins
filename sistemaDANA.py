import os
import json
import time
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FUNCIONES ------------------------------------------------------------------------------------------------------------------------------

# Función para cargar la configuración desde el archivo JSON
def parse_config_file(config_file_path):
    with open(config_file_path, 'r') as config_file: # Abre el archivo en modo lectura
        config_data = json.load(config_file) # Carga el JSON en un diccionario
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


# Función para publicar el archivo JSON detectado en un tema MQTT
def publish_json_file(client, topic, file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            message = json.dumps(data)
            client.publish(topic, message)
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo JSON: {e}")
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {file_path}")


# Función watchdog que monitoriza el directorio y llama a la función de publicación
def watchdog(client, topic, path):
    # Función para manejar los eventos de creación de archivos en el directorio
    def handle_directory_change(event):
        if not event.is_directory:  # Ignorar eventos de creación de directorios
            if event.src_path.endswith('.json'):  # Si el archivo creado es un JSON
                publish_json_file(client, topic, event.src_path)

    # Instanciar un observador de cambios en el sistema de archivos
    observer = Observer()

    # Configurar el manejador de eventos
    event_handler = FileSystemEventHandler()
    event_handler.on_created = handle_directory_change

    # Asignar el manejador de eventos al observador
    observer.schedule(event_handler, path, recursive=False)  # Monitorear solo el directorio de topología

    # Iniciar el observador
    observer.start()

    # Mensaje de confirmación
    print(f"Watchdog está monitoreando el directorio: {path}")

    return observer


# MAIN ------------------------------------------------------------------------------------------------------------------------------

# Parsear el archivo de configuración
config = parse_config_file("config.json")

# Configurar las variables
topology_path = config["topology_path"]
mqtt_broker_ip = config["mqtt_broker_ip"]
mqtt_broker_port = config["mqtt_broker_port"]
mqtt_topic = "topology_de_prueba2"  # Nombre del tema MQTT al que se publicará la topología

# Crear un cliente MQTT
client = mqtt.Client()

# Conectar al broker MQTT
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Configurar Watchdog
observer = watchdog(client, mqtt_topic, topology_path)

# Generar el JSON de topología
generate_topology_json(topology_path)

# Esperar
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()